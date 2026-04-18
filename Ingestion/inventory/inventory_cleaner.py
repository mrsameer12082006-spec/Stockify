from ..data_cleaner import clean_data


def clean_inventory(df):
    """Wrapper around existing cleaner to clean inventory data."""
    return clean_data(df)
