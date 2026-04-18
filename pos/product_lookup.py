from typing import Optional, Dict

from .database import Database


class ProductLookup:
    """Lookup products from inventory by barcode or product code."""

    SAMPLE_CATALOG = {
        "P001": {
            "sku": "P001",
            "name": "Coffee Beans",
            "category": "Beverages",
            "price": 5.99,
            "stock": 120,
            "reorder_point": 30,
            "supplier_name": "Brew Supply Co.",
            "supplier_phone": "+91 98765 43210"
        },
        "P002": {
            "sku": "P002",
            "name": "Green Tea",
            "category": "Beverages",
            "price": 3.99,
            "stock": 80,
            "reorder_point": 20,
            "supplier_name": "Leaf Traders",
            "supplier_phone": "+91 91234 56789"
        },
    }

    def __init__(self):
        self.db = Database()

    def lookup(self, code: str) -> Optional[Dict[str, object]]:
        if not code:
            return None

        product = self.db.get_inventory_item(code)
        if product:
            return product

        normalized = str(code).strip().upper()
        return self.SAMPLE_CATALOG.get(normalized)

    def add_product(self, product: Dict[str, object]) -> bool:
        return self.db.add_inventory_product(product)
