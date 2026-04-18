from typing import List, Dict

from .database import Database


class InventoryUpdater:
    """Inventory update helper for POS stock adjustments."""

    def __init__(self):
        self.db = Database()

    def update_stock(self, items: List[Dict[str, object]]) -> None:
        for item in items:
            sku = str(item.get("sku", "")).strip()
            quantity = int(item.get("quantity", 1))
            if sku and quantity > 0:
                self.db.decrement_stock(sku, quantity)
