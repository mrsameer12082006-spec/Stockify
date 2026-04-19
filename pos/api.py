import json
import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, urlparse

from .database import Database


class BarcodeAPI:
    """POS barcode API service for lookup, scan, and inventory updates."""

    def __init__(self): self.db = Database(); self.pending_sale_by_sku = {}

    def lookup(self, code: str) -> Optional[Dict[str, Any]]:
        if not code:
            return None
        return self.db.get_inventory_item(code)

    def scan_and_sell(self, code: str, quantity: int = 1) -> Optional[Dict[str, Any]]:
        if not code or quantity <= 0:
            return None

        normalized_code = str(code).strip().upper()
        product = self.lookup(code)
        if not product:
            created = self.db.add_inventory_product({
                "sku": normalized_code,
                "barcode": str(code).strip(),
                "name": f"New Item {normalized_code}",
                "category": "Uncategorized",
                "price": 0.0,
                "stock": 0,
                "reorder_point": 0,
                "supplier_name": "Local Supplier",
                "supplier_phone": "N/A",
                "unit_cost": 0.0,
                "last_purchase_date": "",
            })
            if not created:
                return None
            product = self.lookup(code)
            if not product:
                return None

        sku = str(product.get("sku", "") or "").strip().upper()
        if not sku:
            return None

        pending_sale = self.pending_sale_by_sku.get(sku, False)

        # First scan of an item: move to inventory (stock +quantity).
        # Second scan of same item: record sale (stock -quantity and revenue +quantity*price).
        if not pending_sale:
            self.db.increment_stock(sku, quantity)
            updated_product = self.lookup(sku) or product
            self.pending_sale_by_sku[sku] = True
            return {
                "action": "inventory",
                "message": "Added to inventory. Scan the same item again to record a sale.",
                "product": updated_product,
                "quantity": quantity,
                "updated_stock": updated_product.get("stock"),
            }

        sale_item = {
            "sku": sku,
            "name": product["name"],
            "category": product.get("category", ""),
            "price": product.get("price", 0.0),
            "quantity": quantity,
        }

        self.db.record_sale([sale_item])
        self.db.decrement_stock(sku, quantity)
        updated_product = self.lookup(sku)
        self.pending_sale_by_sku[sku] = False

        return {
            "action": "sale",
            "message": "Sale recorded and inventory updated.",
            "product": product,
            "quantity": quantity,
            "updated_stock": updated_product["stock"] if updated_product else None,
            "sale": {
                "sku": sale_item["sku"],
                "product": sale_item["name"],
                "quantity": quantity,
                "revenue": round(sale_item["price"] * quantity, 2),
            },
        }


class _BarcodeApiRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, response: Any) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(json.dumps(response, default=str).encode("utf-8"))

    def _send_html(self, html: str) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path.startswith("/api/"):
            if path == "/api/lookup":
                barcode = query.get("barcode", [""])[0]
                item = self.server.api.lookup(barcode)
                if not item:
                    return self._send_json(404, {"error": "Product not found"})
                return self._send_json(200, item)

            if path == "/api/scan":
                barcode = query.get("barcode", [""])[0]
                quantity_raw = query.get("quantity", ["1"])[0]
                try:
                    quantity = int(quantity_raw or 1)
                except (TypeError, ValueError):
                    return self._send_json(400, {"error": "Invalid quantity"})
                result = self.server.api.scan_and_sell(barcode, quantity)
                if not result:
                    return self._send_json(404, {"error": "Product not found or invalid quantity"})
                return self._send_json(200, result)

            if path == "/api/status":
                return self._send_json(200, {"status": "ok"})

            return self._send_json(404, {"error": "API endpoint not found"})

        if path in ("", "/", "/mobile-scan", "/mobile-scan/", "/scanner", "/scanner/"):
            page = self._get_scanner_page()
            return self._send_html(page)

        # fallback to mobile scanner page for any other non-API path
        page = self._get_scanner_page()
        return self._send_html(page)

    def _get_scanner_page(self) -> str:
        return """
<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='utf-8'/>
  <meta name='viewport' content='width=device-width, initial-scale=1' />
  <title>Stockify Mobile Barcode Scanner</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; padding: 16px; background: #121212; color: #fff; }
    h1 { margin-top: 0; }
    #reader { width: 100%%; max-width: 480px; margin: 0 auto; }
    #output { margin-top: 16px; padding: 12px; background: #1e1e1e; border-radius: 8px; }
    .button { margin-top: 12px; padding: 10px 16px; font-size: 16px; border: none; border-radius: 8px; background: #0a84ff; color: #fff; cursor: pointer; }
  </style>
</head>
<body>
  <h1>Stockify Scanner</h1>
  <p>Point your phone camera at a product barcode. When the scan completes, the inventory will update automatically.</p>
  <div id='reader'></div>
  <div id='output'>Waiting for scan...</div>
  <button id='stop' class='button'>Stop Camera</button>
  <script src='https://unpkg.com/html5-qrcode@2.3.7/minified/html5-qrcode.min.js'></script>
  <script>
    const apiBase = window.location.origin;
    const output = document.getElementById('output');
    const html5QrcodeScanner = new Html5Qrcode('reader');

    function formatCurrency(value) {
      const number = Number(value || 0);
      return '₹' + number.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }

    let scannerRunning = false;
    let scanInFlight = false;
    let lastScanText = '';
    let lastScanTs = 0;
    const SCAN_COOLDOWN_MS = 1200;

    function handleResult(decodedText) {
      scanInFlight = true;
      output.textContent = 'Scanned: ' + decodedText + ' — processing...';
      return fetch(`${apiBase}/api/scan?barcode=${encodeURIComponent(decodedText)}&quantity=1`)
        .then(response => response.json())
        .then(data => {
          if (data.error) {
            output.textContent = 'Error: ' + data.error;
          } else {
            const name = (data.product && data.product.name) ? data.product.name : decodedText;
            const stock = (typeof data.updated_stock === 'number') ? data.updated_stock : 'N/A';
            const message = data.message || '';

            if (data.action === 'sale' && data.sale) {
              output.innerHTML = `${message}<br/><strong>${name}</strong><br/>New stock: ${stock}<br/>Revenue: ${formatCurrency(data.sale.revenue)}`;
            } else {
              output.innerHTML = `${message}<br/><strong>${name}</strong><br/>Current stock: ${stock}`;
            }
          }
        })
        .catch(err => {
          output.textContent = 'Network error: ' + err.message;
        })
        .finally(() => {
          scanInFlight = false;
        });
    }

    function startScanner() {
      Html5Qrcode.getCameras().then(cameras => {
        if (cameras && cameras.length) {
          const cameraId = cameras[cameras.length - 1].id;
          html5QrcodeScanner.start(
            cameraId,
            { fps: 10, qrbox: 250 },
            decodedText => {
              const now = Date.now();
              if (scanInFlight) {
                return;
              }
              if (decodedText === lastScanText && (now - lastScanTs) < SCAN_COOLDOWN_MS) {
                return;
              }
              lastScanText = decodedText;
              lastScanTs = now;
              handleResult(decodedText);
            },
            errorMessage => {
              console.warn(errorMessage);
            }
          ).catch(err => {
            output.textContent = 'Unable to start camera: ' + err;
          }).then(() => {
            scannerRunning = true;
          });
        } else {
          output.textContent = 'No camera found on this device.';
        }
      }).catch(err => {
        output.textContent = 'Camera access denied or unsupported: ' + err;
      });
    }

    document.getElementById('stop').addEventListener('click', () => {
      if (!scannerRunning) {
        output.textContent = 'Camera is not running.';
        return;
      }
      html5QrcodeScanner.stop().then(() => {
        scannerRunning = false;
        output.textContent = 'Camera stopped.';
      }).catch(err => {
        output.textContent = 'Unable to stop camera: ' + err;
      });
    });

    startScanner();
  </script>
</body>
</html>
"""

    def log_message(self, format: str, *args: Any) -> None:
        return


class BarcodeApiServer:
    """Local HTTP server for barcode scanning API endpoints."""

    def __init__(self, host: str = "0.0.0.0", port: int = 8502):
        self.host = host
        self.port = port
        self.server: Optional[HTTPServer] = None
        self.thread: Optional[threading.Thread] = None

    def _get_local_ip(self) -> str:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"

    def get_url(self) -> str:
        host = self.host
        if host == "0.0.0.0":
            host = self._get_local_ip()
        return f"http://{host}:{self.port}"

    def start(self) -> None:
        if self.thread and self.thread.is_alive():
            return

        try:
            self.server = HTTPServer((self.host, self.port), _BarcodeApiRequestHandler)
            self.server.api = BarcodeAPI()
            self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.thread.start()
        except OSError:
            self.server = None
            self.thread = None

    def stop(self) -> None:
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        if self.thread:
            self.thread.join(timeout=1)
        self.server = None
        self.thread = None


_API_SERVER: Optional[BarcodeApiServer] = None
_API_SINGLETON: Optional[BarcodeAPI] = None


def get_api_server() -> BarcodeApiServer:
    global _API_SERVER
    if _API_SERVER is None:
        _API_SERVER = BarcodeApiServer()
    return _API_SERVER


def start_api_server() -> None:
    server = get_api_server()
    server.start()
    global _API_SINGLETON
    if server.server and server.server.api:
        _API_SINGLETON = server.server.api


def get_api() -> BarcodeAPI:
    global _API_SINGLETON
    server = get_api_server()
    if server.server and server.server.api:
        _API_SINGLETON = server.server.api
        return server.server.api
    if _API_SINGLETON is None:
        _API_SINGLETON = BarcodeAPI()
    return _API_SINGLETON
