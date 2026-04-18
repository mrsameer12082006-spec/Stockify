"""
Inventory schema definition (mirrors existing schema_validator REQUIRED_COLUMNS)
"""

INVENTORY_SCHEMA = {
    "Product ID": {"dtype": "string", "description": "Unique product identifier"},
    "Product Name": {"dtype": "string", "description": "Product name"},
    "Category": {"dtype": "string", "description": "Product category"},
    "Quantity On Hand": {"dtype": "int", "description": "Current stock"},
    "Reorder Point": {"dtype": "int", "description": "Reorder threshold"},
    "Unit Cost": {"dtype": "float", "description": "Cost per unit"},
    "Selling Price": {"dtype": "float", "description": "Sale price"},
    "Last Purchase Date": {"dtype": "datetime", "description": "Last purchase date"},
}

def get_columns():
    return [(k, v["dtype"], v["description"]) for k, v in INVENTORY_SCHEMA.items()]
