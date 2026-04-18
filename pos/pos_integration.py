"""
POS Integration Layer - bridges POS transactions with analytics system.

Ensures that when transactions occur in POS, they:
1. Update the database
2. Sync to CSV files
3. Make data available to analytics
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class POSIntegration:
    """Handles integration between POS system and analytics."""
    
    SALES_CSV = Path("data") / "processed" / "clean_sales.csv"
    INVENTORY_CSV = Path("data") / "processed" / "clean_inventory.csv"
    
    @staticmethod
    def ensure_data_synced() -> bool:
        """
        Verify that POS data has been synced to CSV files.
        This is called after significant POS operations.
        
        Returns:
            True if sync is complete, False otherwise
        """
        try:
            # Check if sales CSV exists and has data
            if POSIntegration.SALES_CSV.exists():
                df = pd.read_csv(POSIntegration.SALES_CSV)
                return len(df) > 0
            return False
        except Exception as e:
            print(f"Warning: Could not verify POS data sync: {e}")
            return False
    
    @staticmethod
    def record_pos_sale(items: List[Dict], transaction_id: Optional[str] = None) -> Dict:
        """
        Record a POS sale to the sales CSV.
        
        Args:
            items: List of cart items with sku, name, quantity, revenue, category
            transaction_id: Unique transaction identifier
            
        Returns:
            Dictionary with transaction info including timestamp and items count
        """
        try:
            if not items:
                return {"success": False, "message": "No items in transaction"}
            
            # Generate transaction ID if not provided
            if not transaction_id:
                transaction_id = f"POS-{int(datetime.now().timestamp())}"
            
            # Load existing sales
            sales_records = []
            if POSIntegration.SALES_CSV.exists():
                try:
                    existing_df = pd.read_csv(POSIntegration.SALES_CSV)
                    sales_records = existing_df.to_dict('records')
                except Exception as e:
                    print(f"Warning: Could not load existing sales: {e}")
                    sales_records = []
            
            # Add new transactions
            for item in items:
                sale_record = {
                    "product": item.get("name", item.get("sku", "Unknown")),
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "quantity": int(item.get("quantity", 1)),
                    "revenue": float(item.get("price", 0)) * int(item.get("quantity", 1)),
                    "category": item.get("category", "Uncategorized"),
                    "transaction_id": transaction_id
                }
                sales_records.append(sale_record)
            
            # Write back to CSV
            sales_df = pd.DataFrame(sales_records)
            POSIntegration.SALES_CSV.parent.mkdir(parents=True, exist_ok=True)
            sales_df.to_csv(POSIntegration.SALES_CSV, index=False)
            
            return {
                "success": True,
                "message": f"Recorded POS sale with {len(items)} items",
                "transaction_id": transaction_id,
                "items_count": len(items),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"success": False, "message": f"Error recording POS sale: {str(e)}"}
    
    @staticmethod
    def update_pos_inventory(sku: str, quantity: int) -> Dict:
        """
        Update inventory after a POS transaction.
        Decrements stock from clean_inventory.csv.
        
        Args:
            sku: Product SKU
            quantity: Quantity to decrement
            
        Returns:
            Dictionary with update status
        """
        try:
            if not POSIntegration.INVENTORY_CSV.exists():
                return {"success": False, "message": "Inventory CSV not found"}
            
            # Load inventory
            inventory_df = pd.read_csv(POSIntegration.INVENTORY_CSV)
            
            # Find product
            product_mask = inventory_df["Product ID"] == sku
            if not product_mask.any():
                return {"success": False, "message": f"Product {sku} not found in inventory"}
            
            # Update stock
            current_stock = int(inventory_df.loc[product_mask, "Quantity On Hand"].iloc[0])
            new_stock = max(0, current_stock - quantity)
            
            inventory_df.loc[product_mask, "Quantity On Hand"] = new_stock
            
            # Save back
            POSIntegration.INVENTORY_CSV.parent.mkdir(parents=True, exist_ok=True)
            inventory_df.to_csv(POSIntegration.INVENTORY_CSV, index=False)
            
            return {
                "success": True,
                "message": f"Updated {sku} inventory",
                "sku": sku,
                "previous_stock": current_stock,
                "new_stock": new_stock
            }
        except Exception as e:
            return {"success": False, "message": f"Error updating inventory: {str(e)}"}
    
    @staticmethod
    def trigger_analytics_refresh():
        """
        Signal that POS data has changed and analytics should be refreshed.
        This is used by the frontend to know when to re-run analytics.
        """
        # In Streamlit, we can use session state to trigger refreshes
        import streamlit as st
        if "pos_data_updated" not in st.session_state:
            st.session_state.pos_data_updated = False
        st.session_state.pos_data_updated = True
        st.session_state.analytics_results = None  # Reset analytics cache
