"""Ingestion package exports.

Expose convenience pipeline entrypoints for frontend usage.
"""

try:
	from .inventory.inventory_pipeline import process_inventory_file
	from .sales.sales_pipeline import process_sales_file
except Exception:
	# fallback for different import contexts
	from .inventory.inventory_pipeline import process_inventory_file
	from .sales.sales_pipeline import process_sales_file

__all__ = ["process_inventory_file", "process_sales_file"]
