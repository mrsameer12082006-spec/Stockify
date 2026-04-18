"""
Sales schema definition

Columns:
- product: string - Product name
- date: string (YYYY-MM-DD) - Transaction date
- quantity: int - Units sold
- revenue: float - Revenue from transaction
- category: string - Product category
"""

SALES_SCHEMA = {
    "product": {"dtype": "string", "description": "Product name"},
    "date": {"dtype": "string", "description": "Transaction date (YYYY-MM-DD)"},
    "quantity": {"dtype": "int", "description": "Units sold"},
    "revenue": {"dtype": "float", "description": "Revenue from transaction"},
    "category": {"dtype": "string", "description": "Product category"},
}

def get_columns():
    return [(k, v["dtype"], v["description"]) for k, v in SALES_SCHEMA.items()]
