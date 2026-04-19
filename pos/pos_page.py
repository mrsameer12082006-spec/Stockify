import json

import streamlit as st
import streamlit.components.v1 as components

from .barcode_scanner import BarcodeScanner
from .cart import Cart
from .transaction import Transaction
from .inventory_update import InventoryUpdater
from .product_lookup import ProductLookup
from .supplier_logic import SupplierLogic
from .api import BarcodeAPI, start_api_server, get_api_server, get_api
from utils.helpers import format_currency


def _render_qr_code(size: int = 280) -> None:
    html = f"""
    <div id='qrcode'></div>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js'></script>
    <script>
      const container = document.getElementById('qrcode');
      container.innerHTML = '';
            const target = new URL(window.parent.location.href);
            target.searchParams.set('mobile_scanner', '1');
            target.searchParams.delete('scan_code');
            new QRCode(container, {{
                text: target.toString(),
        width: {size},
        height: {size},
        colorDark: '#000000',
        colorLight: '#ffffff',
        correctLevel: QRCode.CorrectLevel.H
      }});
    </script>
    """
    components.html(html, height=size + 30)


def show_pos_page():
    """Render the point-of-sale page for scanning, cart management, and checkout."""
    try:
        st.title("Point of Sale")
        st.write("Scan products, add items to the cart, and confirm sales in real time.")

        # Initialize session state
        if "pos_cart" not in st.session_state:
            st.session_state.pos_cart = Cart()
        if "pos_last_scan" not in st.session_state:
            st.session_state.pos_last_scan = None
        if "pos_lookup_msg" not in st.session_state:
            st.session_state.pos_lookup_msg = ""
        if "pos_low_stock" not in st.session_state:
            st.session_state.pos_low_stock = None

        # Initialize POS components
        try:
            lookup = ProductLookup()
            supplier_logic = SupplierLogic()
            cart = st.session_state.pos_cart
            scanner = BarcodeScanner()
            api = get_api()
            
            # Safely start API server
            try:
                start_api_server()
                api_server = get_api_server()
                api_url = api_server.get_url() if api_server else "http://localhost:5000"
            except Exception as api_err:
                st.warning(f"API server not available. Mobile scanner disabled.")
                api_url = "http://localhost:5000"
        except Exception as init_err:
            st.error(f"Failed to initialize POS components: {init_err}")
            return

        # Product lookup form
        with st.form(key="pos_scan_form"):
            barcode = st.text_input("Barcode or product code", value="", placeholder="e.g. P001 or 89012345")
            quantity = st.number_input("Quantity", min_value=1, step=1, value=1)
            do_lookup = st.form_submit_button("Lookup Product")
            do_scan = st.form_submit_button("Scan & update inventory")

            if do_lookup or do_scan:
                product = lookup.lookup(barcode)
                if not product:
                    product = scanner.scan(barcode)

                if product:
                    st.session_state.pos_last_scan = product
                    st.session_state.pos_lookup_msg = ""
                    if product["stock"] <= product["reorder_point"]:
                        st.session_state.pos_low_stock = supplier_logic.suggest_supplier(product)
                    else:
                        st.session_state.pos_low_stock = None

                    if do_scan:
                        scan_result = api.scan_and_sell(barcode, quantity)
                        if scan_result:
                            action = scan_result.get("action", "")
                            if action == "inventory":
                                st.success(
                                    f"First scan: {quantity} x {product['name']} added to inventory. "
                                    "Scan again to record sale."
                                )
                            elif action == "sale":
                                st.success(f"Second scan: sale recorded for {quantity} x {product['name']}.")
                            else:
                                st.success(f"Scanned {quantity} x {product['name']}.")

                            st.write(f"Updated stock: {scan_result.get('updated_stock')}")
                            if scan_result.get("sale"):
                                st.write(f"Revenue added: {format_currency(scan_result['sale'].get('revenue', 0))}")
                        else:
                            st.error("Unable to scan and update inventory. Check the barcode and quantity.")
                else:
                    st.session_state.pos_last_scan = None
                    st.session_state.pos_lookup_msg = f"Product not found for code: {barcode}"
                    st.session_state.pos_low_stock = None

        if st.session_state.pos_lookup_msg:
            st.error(st.session_state.pos_lookup_msg)

        # Show product details
        if st.session_state.pos_last_scan:
            product = st.session_state.pos_last_scan
            st.markdown("### Product details")
            st.markdown(
                f"- **Code:** {product['sku']}\n"
                f"- **Name:** {product['name']}\n"
                f"- **Category:** {product['category']}\n"
                f"- **Price:** {format_currency(product['price'])}\n"
                f"- **Stock:** {product['stock']}\n"
                f"- **Reorder Point:** {product['reorder_point']}"
            )

            if st.button("Add to cart"):
                cart.add_item(product, quantity=quantity)
                st.success(f"Added {quantity} x {product['name']} to cart")
                st.session_state.pos_last_scan = None

        # Add new product section
        with st.expander("Add a new product to inventory"):
            new_sku = st.text_input("Product code / SKU", value="", key="new_product_sku")
            new_name = st.text_input("Product name", value="", key="new_product_name")
            new_category = st.text_input("Category", value="", key="new_product_category")
            new_price = st.number_input("Selling price", min_value=0.0, step=0.01, value=0.0, key="new_product_price")
            new_stock = st.number_input("Initial stock", min_value=0, step=1, value=0, key="new_product_stock")
            new_reorder = st.number_input("Reorder point", min_value=0, step=1, value=0, key="new_product_reorder")
            new_supplier = st.text_input("Supplier name", value="", key="new_product_supplier")
            new_phone = st.text_input("Supplier phone", value="", key="new_product_phone")

            if st.button("Save product", key="save_new_product"):
                new_item = {
                    "sku": new_sku.strip().upper(),
                    "name": new_name.strip(),
                    "category": new_category.strip() or "Uncategorized",
                    "price": float(new_price),
                    "stock": int(new_stock),
                    "reorder_point": int(new_reorder),
                    "supplier_name": new_supplier.strip() or "Local Supplier",
                    "supplier_phone": new_phone.strip() or "N/A",
                    "unit_cost": 0.0,
                    "last_purchase_date": ""
                }
                if not new_item["sku"] or not new_item["name"]:
                    st.error("SKU and product name are required.")
                else:
                    if lookup.add_product(new_item):
                        st.success(f"Added product {new_item['name']} to inventory.")
                        st.session_state.pos_last_scan = new_item
                    else:
                        st.error("Failed to add product. Check the SKU.")

        # Cart display
        st.markdown("## Cart")
        if cart.items:
            cart_lines = [
                {
                    "SKU": item["sku"],
                    "Product": item["name"],
                    "Quantity": item["quantity"],
                    "Unit Price": format_currency(item['price']),
                    "Line Total": format_currency(item['quantity'] * item['price'])
                }
                for item in cart.items
            ]
            st.table(cart_lines)
            st.write(f"**Total:** {format_currency(cart.get_total())}")

            if st.button("Confirm sale"):
                transaction = Transaction(cart.items)
                transaction_record = transaction.record_sale()
                inventory = InventoryUpdater()
                inventory.update_stock(cart.items)
                cart.clear()
                st.success("Sale confirmed and inventory updated.")
        else:
            st.info("Cart is empty. Lookup a product to begin.")

        # Low stock warning
        if st.session_state.pos_low_stock:
            low_stock = st.session_state.pos_low_stock
            st.warning("Low stock detected for the selected product.")
            st.write(f"**Supplier:** {low_stock['supplier_name']}")
            st.write(f"**Phone:** {low_stock['supplier_phone']}")

        # Mobile scanner
        with st.expander("Mobile barcode scanner"):
            st.write("Scan this QR code with your phone to open a mobile scanner.")
            try:
                _render_qr_code()
            except Exception as qr_err:
                st.info("QR code rendering unavailable")
            st.write("The QR opens this app in mobile scanner mode.")
            st.code("Same app URL + ?mobile_scanner=1", language="bash")

    except Exception as e:
        st.error(f"POS page error: {str(e)}")
        with st.expander("🔍 Debug Details"):
            import traceback
            st.code(traceback.format_exc(), language="python")
