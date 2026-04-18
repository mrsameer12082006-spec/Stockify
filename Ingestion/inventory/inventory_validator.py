from ..schema_validator import validate_schema


def validate_inventory_schema(df):
    """Wrapper around existing validator to validate inventory data."""
    return validate_schema(df)
