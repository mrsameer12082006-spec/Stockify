from typing import Optional, Dict

from .api import BarcodeAPI


class BarcodeScanner:
    """Barcode scanner simulator for POS workflows, backed by the barcode API."""

    def __init__(self):
        self.api = BarcodeAPI()

    def scan(self, barcode: str) -> Optional[Dict[str, object]]:
        """Return product metadata for a scanned barcode or SKU."""
        if not barcode:
            return None
        return self.api.lookup(barcode)
