import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd


class Database:
    """SQLite helper for inventory and sales persistence."""

    DB_PATH = Path("data") / "processed" / "stockify.db"
    INVENTORY_CSV = Path("data") / "processed" / "clean_inventory.csv"
    SALES_CSV = Path("data") / "processed" / "clean_sales.csv"

    def __init__(self):
        self.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_database()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.DB_PATH), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _ensure_database(self) -> None:
        created = not self.DB_PATH.exists()
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS inventory (
                    barcode TEXT PRIMARY KEY,
                    sku TEXT UNIQUE,
                    product_name TEXT NOT NULL,
                    category TEXT,
                    price REAL DEFAULT 0.0,
                    stock INTEGER DEFAULT 0,
                    reorder_point INTEGER DEFAULT 0,
                    supplier_name TEXT,
                    supplier_phone TEXT,
                    unit_cost REAL DEFAULT 0.0,
                    last_purchase_date TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_id TEXT,
                    date TEXT,
                    sku TEXT,
                    product TEXT,
                    quantity INTEGER,
                    revenue REAL,
                    category TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        if created:
            self._import_existing_csvs()

        # Ensure external CSVs remain in sync with the authoritative database structure.
        self._sync_inventory_csv()
        self._sync_sales_csv()

    def _import_existing_csvs(self) -> None:
        if self.INVENTORY_CSV.exists():
            try:
                inventory_df = pd.read_csv(self.INVENTORY_CSV)
                for _, row in inventory_df.iterrows():
                    self.add_inventory_product({
                        "sku": str(row.get("Product ID", "")).strip().upper() or str(row.get("barcode", "")).strip().upper(),
                        "barcode": str(row.get("barcode", "")).strip() or str(row.get("Product ID", "")).strip(),
                        "name": row.get("Product Name", "").strip(),
                        "category": row.get("Category", "").strip(),
                        "price": float(row.get("Selling Price", 0.0) or 0.0),
                        "stock": int(row.get("Quantity On Hand", 0) or 0),
                        "reorder_point": int(row.get("Reorder Point", 0) or 0),
                        "supplier_name": str(row.get("supplier_name", "")).strip() or str(row.get("Supplier Name", "")).strip(),
                        "supplier_phone": str(row.get("supplier_phone", "")).strip() or str(row.get("Supplier Phone", "")).strip(),
                        "unit_cost": float(row.get("Unit Cost", 0.0) or 0.0),
                        "last_purchase_date": str(row.get("Last Purchase Date", "") or "")
                    })
            except Exception:
                pass

        if self.SALES_CSV.exists():
            try:
                sales_df = pd.read_csv(self.SALES_CSV)
                for _, row in sales_df.iterrows():
                    self._insert_sale_row({
                        "transaction_id": str(row.get("transaction_id", "")).strip() or f"TXN-{int(datetime.now().timestamp())}",
                        "date": str(row.get("date", "")).strip(),
                        "sku": str(row.get("product", "")).strip(),
                        "product": str(row.get("product", "")).strip(),
                        "quantity": int(row.get("quantity", 0) or 0),
                        "revenue": float(row.get("revenue", 0.0) or 0.0),
                        "category": str(row.get("category", "")).strip(),
                    })
            except Exception:
                pass

    def _normalize_code(self, code: str) -> str:
        return str(code).strip().upper()

    def get_inventory_item(self, code: str) -> Optional[Dict[str, Any]]:
        normalized = self._normalize_code(code)
        query = "SELECT * FROM inventory WHERE UPPER(barcode) = ? OR UPPER(sku) = ? LIMIT 1"
        with self._connect() as conn:
            row = conn.execute(query, (normalized, normalized)).fetchone()
            if row is None:
                return None
            return self._row_to_inventory_dict(row)

    def add_inventory_product(self, product: Dict[str, Any]) -> bool:
        if not product.get("sku"):
            return False

        barcode = str(product.get("barcode", "")).strip() or str(product.get("sku", "")).strip().upper()
        sku = str(product.get("sku", "")).strip().upper()
        data = {
            "barcode": barcode,
            "sku": sku,
            "product_name": str(product.get("name", "")).strip(),
            "category": str(product.get("category", "")).strip(),
            "price": float(product.get("price", 0.0) or 0.0),
            "stock": int(product.get("stock", 0) or 0),
            "reorder_point": int(product.get("reorder_point", 0) or 0),
            "supplier_name": str(product.get("supplier_name", "")).strip(),
            "supplier_phone": str(product.get("supplier_phone", "")).strip(),
            "unit_cost": float(product.get("unit_cost", 0.0) or 0.0),
            "last_purchase_date": str(product.get("last_purchase_date", "")).strip(),
        }

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO inventory (barcode, sku, product_name, category, price, stock, reorder_point,
                                       supplier_name, supplier_phone, unit_cost, last_purchase_date)
                VALUES (:barcode, :sku, :product_name, :category, :price, :stock, :reorder_point,
                        :supplier_name, :supplier_phone, :unit_cost, :last_purchase_date)
                ON CONFLICT(barcode) DO UPDATE SET
                    sku = excluded.sku,
                    product_name = excluded.product_name,
                    category = excluded.category,
                    price = excluded.price,
                    stock = excluded.stock,
                    reorder_point = excluded.reorder_point,
                    supplier_name = excluded.supplier_name,
                    supplier_phone = excluded.supplier_phone,
                    unit_cost = excluded.unit_cost,
                    last_purchase_date = excluded.last_purchase_date
                """,
                data,
            )
            conn.commit()

        self._sync_inventory_csv()
        return True

    def decrement_stock(self, sku: str, quantity: int = 1) -> None:
        if not sku or quantity <= 0:
            return

        normalized = self._normalize_code(sku)
        with self._connect() as conn:
            row = conn.execute(
                "SELECT stock, sku FROM inventory WHERE UPPER(barcode) = ? OR UPPER(sku) = ? LIMIT 1",
                (normalized, normalized),
            ).fetchone()
            if row is None:
                return

            new_stock = max(0, int(row["stock"] or 0) - quantity)
            conn.execute(
                "UPDATE inventory SET stock = ? WHERE UPPER(barcode) = ? OR UPPER(sku) = ?",
                (new_stock, normalized, normalized),
            )
            conn.commit()

        self._sync_inventory_csv()

    def record_sale(self, items: List[Dict[str, Any]], transaction_id: Optional[str] = None) -> Dict[str, Any]:
        if transaction_id is None:
            transaction_id = f"TXN-{int(datetime.now().timestamp())}"

        date_str = datetime.now().strftime("%Y-%m-%d")
        recorded_items = []

        with self._connect() as conn:
            for item in items:
                quantity = int(item.get("quantity", 1) or 1)
                revenue = round(float(item.get("price", 0.0) or 0.0) * quantity, 2)
                row = {
                    "transaction_id": transaction_id,
                    "date": date_str,
                    "sku": str(item.get("sku", "")).strip(),
                    "product": str(item.get("name", "")).strip(),
                    "quantity": quantity,
                    "revenue": revenue,
                    "category": str(item.get("category", "")).strip(),
                }
                conn.execute(
                    """
                    INSERT INTO sales (transaction_id, date, sku, product, quantity, revenue, category)
                    VALUES (:transaction_id, :date, :sku, :product, :quantity, :revenue, :category)
                    """,
                    row,
                )
                recorded_items.append(row)
            conn.commit()

        self._sync_sales_csv()
        return {
            "transaction_id": transaction_id,
            "date": date_str,
            "total": sum(item["revenue"] for item in recorded_items),
            "items": recorded_items,
        }

    def _insert_sale_row(self, row: Dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO sales (transaction_id, date, sku, product, quantity, revenue, category)
                VALUES (:transaction_id, :date, :sku, :product, :quantity, :revenue, :category)
                """,
                row,
            )
            conn.commit()

    def _sync_inventory_csv(self) -> None:
        try:
            df = self.get_inventory_df()
            if not df.empty:
                df = df.rename(columns={
                    "barcode": "barcode",
                    "sku": "Product ID",
                    "product_name": "Product Name",
                    "category": "Category",
                    "price": "Selling Price",
                    "stock": "Quantity On Hand",
                    "reorder_point": "Reorder Point",
                    "unit_cost": "Unit Cost",
                    "last_purchase_date": "Last Purchase Date",
                    "supplier_name": "supplier_name",
                    "supplier_phone": "supplier_phone",
                })
                columns = [
                    "barcode",
                    "Product ID",
                    "Product Name",
                    "Category",
                    "Quantity On Hand",
                    "Reorder Point",
                    "Unit Cost",
                    "Selling Price",
                    "Last Purchase Date",
                    "supplier_name",
                    "supplier_phone",
                ]
                columns = [c for c in columns if c in df.columns]
                df = df[columns]
                df.to_csv(self.INVENTORY_CSV, index=False)
        except Exception:
            pass

    def _sync_sales_csv(self) -> None:
        try:
            df = self.get_sales_df()
            if not df.empty:
                df.to_csv(self.SALES_CSV, index=False)
        except Exception:
            pass

    def get_inventory_df(self) -> pd.DataFrame:
        with self._connect() as conn:
            df = pd.read_sql_query("SELECT * FROM inventory", conn)
        return df

    def get_sales_df(self) -> pd.DataFrame:
        with self._connect() as conn:
            df = pd.read_sql_query("SELECT * FROM sales", conn)
        return df

    def _row_to_inventory_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        return {
            "barcode": row["barcode"],
            "sku": row["sku"],
            "name": row["product_name"],
            "category": row["category"],
            "price": float(row["price"] or 0.0),
            "stock": int(row["stock"] or 0),
            "reorder_point": int(row["reorder_point"] or 0),
            "supplier_name": row["supplier_name"],
            "supplier_phone": row["supplier_phone"],
            "unit_cost": float(row["unit_cost"] or 0.0),
            "last_purchase_date": row["last_purchase_date"],
        }
