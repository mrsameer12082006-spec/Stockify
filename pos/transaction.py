from datetime import datetime
from typing import List, Dict

from .database import Database


class Transaction:
    """Transaction model to capture checkout details."""

    def __init__(self, items: List[Dict[str, object]]):
        self.items = items
        self.timestamp = datetime.now()
        self.db = Database()

    def compute_total(self) -> float:
        return sum(float(item.get("price", 0)) * int(item.get("quantity", 1)) for item in self.items)

    def record_sale(self) -> Dict[str, object]:
        result = self.db.record_sale(self.items)
        result["timestamp"] = self.timestamp.isoformat()
        return result
