from typing import Dict


class SupplierLogic:
    """Provide supplier recommendations when inventory is low."""

    def suggest_supplier(self, product: Dict[str, object]) -> Dict[str, object]:
        stock = int(product.get("stock", 0))
        reorder_point = int(product.get("reorder_point", 0))
        supplier_name = product.get("supplier_name", "Local Supplier")
        supplier_phone = product.get("supplier_phone", "N/A")

        message = "This item is within the reorder threshold. Place a restock order soon."
        if stock <= reorder_point:
            message = (
                f"Stock is low. Reorder at least {max(1, reorder_point - stock + 1)} unit(s) to stay above the reorder point."
            )

        return {
            "supplier_name": supplier_name,
            "supplier_phone": supplier_phone,
            "message": message,
            "low_stock": stock <= reorder_point,
        }
