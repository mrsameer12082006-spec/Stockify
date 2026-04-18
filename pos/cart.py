from typing import List, Dict


class Cart:
    """Basic cart model for adding, removing, and totaling line items."""

    def __init__(self):
        self.items: List[Dict[str, object]] = []

    def add_item(self, item: Dict[str, object], quantity: int = 1) -> None:
        sku = item.get("sku")
        for existing in self.items:
            if existing.get("sku") == sku:
                existing["quantity"] = int(existing.get("quantity", 1)) + quantity
                return

        self.items.append({
            "sku": item.get("sku"),
            "name": item.get("name"),
            "category": item.get("category"),
            "price": float(item.get("price", 0.0)),
            "quantity": int(quantity),
            "stock": int(item.get("stock", 0)),
            "reorder_point": int(item.get("reorder_point", 0)),
            "supplier_name": item.get("supplier_name"),
            "supplier_phone": item.get("supplier_phone"),
        })

    def remove_item(self, sku: str) -> bool:
        for index, item in enumerate(self.items):
            if item.get("sku") == sku:
                del self.items[index]
                return True
        return False

    def get_total(self) -> float:
        return sum(float(item.get("price", 0)) * int(item.get("quantity", 1)) for item in self.items)

    def clear(self) -> None:
        self.items.clear()
