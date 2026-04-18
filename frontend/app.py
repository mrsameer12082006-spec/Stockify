import sys
import os
from pathlib import Path
_project_root = str(Path(__file__).resolve().parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import streamlit as st
import pandas as pd
from frontend.products import show_products
from analytics.trends import show_trends
from frontend.layout import set_layout
from frontend.navigation import top_navigation
from frontend.home import show_home, show_landing_page
from frontend.upload import show_upload
from frontend.dashboard import show_dashboard
from analytics.insights import show_insights
from decision_support.stock_alerts import show_stock_alerts
from visualization.visualizations import show_visualizations
import sys
from pathlib import Path

# Ensure project root is in path for imports
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from analytics.analytics_runner import run_analytics
from pos.pos_page import show_pos_page


def build_demo_analytics_results(industry_focus: str = "Grocery Stores") -> dict:
    """Create industry-focused demo analytics payload so users can explore context-specific sample data."""
    profile_map = {
        "Grocery Stores": {
            "products": ["Rice 5kg", "Sunflower Oil", "Milk Pack", "Wheat Flour", "Toothpaste", "Detergent"],
            "categories": ["Staples", "Staples", "Dairy", "Staples", "Personal Care", "Home Care"],
            "costs": [220, 115, 36, 165, 42, 88],
            "prices": [290, 165, 52, 235, 72, 132],
            "stocks": [22, 18, 44, 9, 28, 14],
            "reorder": [15, 16, 20, 14, 18, 16],
            "daily_revenue": [8250, 8620, 8010, 9150, 9440, 9720, 10110],
            "daily_qty": [278, 291, 270, 304, 318, 325, 336],
            "daily_txn": [81, 84, 79, 90, 93, 95, 99],
        },
        "Pharmacy": {
            "products": ["Vitamin C", "Pain Relief Tabs", "Protein Powder", "Face Wash", "Antiseptic", "Bandages"],
            "categories": ["Wellness", "Medicine", "Wellness", "Personal Care", "First Aid", "First Aid"],
            "costs": [120, 45, 780, 95, 62, 28],
            "prices": [190, 72, 1150, 149, 98, 46],
            "stocks": [14, 31, 6, 24, 19, 42],
            "reorder": [18, 20, 10, 14, 16, 20],
            "daily_revenue": [10320, 9980, 10650, 11020, 11540, 11830, 12190],
            "daily_qty": [186, 178, 191, 198, 207, 214, 221],
            "daily_txn": [96, 92, 99, 101, 106, 109, 112],
        },
        "Electronics Shops": {
            "products": ["Bluetooth Speaker", "Wireless Mouse", "Keyboard", "Power Bank", "USB-C Cable", "Smartwatch"],
            "categories": ["Audio", "Accessories", "Accessories", "Power", "Accessories", "Wearables"],
            "costs": [1150, 420, 780, 640, 80, 2350],
            "prices": [1799, 699, 1199, 999, 149, 3499],
            "stocks": [8, 35, 11, 14, 62, 5],
            "reorder": [12, 20, 15, 12, 25, 8],
            "daily_revenue": [12450, 11800, 13620, 14210, 15100, 14780, 15990],
            "daily_qty": [320, 301, 347, 366, 382, 374, 401],
            "daily_txn": [94, 88, 101, 106, 112, 109, 118],
        },
        "Fashion Stores": {
            "products": ["Denim Jeans", "Cotton Tee", "Hoodie", "Sneakers", "Casual Shirt", "Cap"],
            "categories": ["Bottomwear", "Topwear", "Topwear", "Footwear", "Topwear", "Accessories"],
            "costs": [780, 220, 460, 1100, 340, 95],
            "prices": [1499, 499, 899, 1999, 799, 249],
            "stocks": [12, 26, 17, 7, 20, 45],
            "reorder": [14, 18, 15, 10, 16, 22],
            "daily_revenue": [9320, 9550, 9980, 10240, 10750, 11120, 11640],
            "daily_qty": [164, 170, 177, 182, 190, 196, 204],
            "daily_txn": [72, 74, 77, 80, 83, 85, 89],
        },
    }

    profile = profile_map.get(industry_focus, profile_map["Grocery Stores"])
    dates = pd.date_range("2026-04-01", periods=7, freq="D")

    daily_trends = pd.DataFrame({
        "date": dates,
        "revenue": profile["daily_revenue"],
        "quantity": profile["daily_qty"],
        "transactions": profile["daily_txn"],
    })

    inventory_df = pd.DataFrame({
        "Product Name": profile["products"],
        "Quantity On Hand": profile["stocks"],
        "Reorder Point": profile["reorder"],
        "Unit Cost": profile["costs"],
        "Selling Price": profile["prices"],
        "Category": profile["categories"],
    })

    demand_rows = []
    for idx, name in enumerate(profile["products"]):
        qty = max(int(profile["daily_qty"][idx % 7] * (0.45 + (idx * 0.07))), 20)
        rev = qty * profile["prices"][idx]
        demand_rows.append({"product": name, "totalQuantity": qty, "revenue": rev})

    product_demand = pd.DataFrame(demand_rows).sort_values("revenue", ascending=False).reset_index(drop=True)
    top_products = product_demand.head(5).copy()

    category_demand = (
        pd.DataFrame(demand_rows)
        .assign(category=profile["categories"])
        .groupby("category", as_index=False)
        .agg(quantity=("totalQuantity", "sum"), revenue=("revenue", "sum"))
        .sort_values("revenue", ascending=False)
        .reset_index(drop=True)
    )

    unique_categories = list(dict.fromkeys(profile["categories"]))
    category_time_series = []
    for d_idx, d in enumerate(dates):
        row = {"date": d.strftime("%Y-%m-%d")}
        for c_idx, cat in enumerate(unique_categories):
            row[cat] = int(profile["daily_revenue"][d_idx] * (0.18 + (c_idx * 0.11)))
        category_time_series.append(row)

    stock_alert_rows = []
    for i, product in enumerate(profile["products"]):
        stock = profile["stocks"][i]
        reorder = profile["reorder"][i]
        cost = profile["costs"][i]
        price = profile["prices"][i]

        if stock <= reorder:
            alert = "Low Stock"
            risk = "High"
            rec = "Reorder immediately to avoid stock-out."
        elif stock >= reorder * 2.2:
            alert = "Overstock"
            risk = "Medium"
            rec = "Reduce next purchase or consider promotional discount."
        else:
            alert = "Healthy"
            risk = "Low"
            rec = "Stock level is optimal."

        margin = round(((price - cost) / price) * 100, 2) if price else 0
        stock_alert_rows.append({
            "Product Name": product,
            "Current Stock": stock,
            "Reorder Point": reorder,
            "Alert Type": alert,
            "Risk Level": risk,
            "Stock Value": round(stock * cost, 2),
            "Potential Revenue": round(stock * price, 2),
            "Profit Margin (%)": margin,
            "Recommendation": rec,
        })

    stock_recommendations = pd.DataFrame(stock_alert_rows)

    return {
        "inventory_df": inventory_df,
        "sales_df": pd.DataFrame(),
        "product_demand": product_demand,
        "category_demand": category_demand,
        "top_products": top_products,
        "daily_trends": daily_trends,
        "category_trends": {"data": category_time_series},
        "category_time_series": category_time_series,
        "kpis": {
            "total_sales_quantity": int(daily_trends["quantity"].sum()),
            "total_products": int(len(inventory_df)),
            "focus_segment": industry_focus,
        },
        "stock_recommendations": stock_recommendations,
    }

# Always run analytics fresh to ensure decision_support data is included
# This runs once per session (Streamlit caches session_state across reruns)
if "analytics_results" not in st.session_state or "stock_recommendations" not in st.session_state.get("analytics_results", {}):
    st.session_state.analytics_results = run_analytics()
# Also re-run if stock_recommendations is empty but inventory data exists
elif st.session_state.analytics_results.get("inventory_df") is not None:
    recs = st.session_state.analytics_results.get("stock_recommendations")
    if recs is None or (hasattr(recs, "empty") and recs.empty):
        st.session_state.analytics_results = run_analytics()

set_layout()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "auth_requested" not in st.session_state:
    st.session_state.auth_requested = False
if "show_how_it_works" not in st.session_state:
    st.session_state.show_how_it_works = False
if "demo_mode_requested" not in st.session_state:
    st.session_state.demo_mode_requested = False
if "users" not in st.session_state:
    st.session_state.users = {"admin": "admin"}
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "signin"


# ---------------- LOGIN PAGE (Antigravity-style) ----------------
def login_page():
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)

    mode = st.session_state.get("auth_mode", "signin")
    signin_active = mode == "signin"
    signup_active = mode == "signup"

    st.markdown(f"""
    <style>
    .auth-brand-wrap {{
        text-align: center;
        animation: fadeInUp 0.6s cubic-bezier(.23, 1, .32, 1);
        margin-bottom: 14px;
    }}
    .auth-title {{
        font-size: 48px;
        font-weight: 700;
        margin-bottom: 4px;
        letter-spacing: -1.8px;
        color: #121317;
    }}
    .auth-sub {{
        color: #7d8590;
        font-size: 14px;
        margin-bottom: 14px;
    }}
    .auth-link-row {{
        text-align: center;
        margin-top: 10px;
        color: #7d8590;
        font-size: 13px;
    }}
    .auth-link-row strong {{
        color: #3279F9;
        font-weight: 600;
    }}
    .forgot-line {{
        color: #6f7eea;
        font-size: 14px;
        margin-top: 2px;
        margin-bottom: 10px;
        text-align: right;
    }}
    .auth-toggle-row {{
        width: 320px;
        margin: 0 auto;
        padding: 5px;
        border-radius: 9999px;
        border: 1px solid rgba(50, 121, 249, 0.14);
        background: rgba(255, 255, 255, 0.96);
        box-shadow: 0 8px 24px rgba(21, 27, 52, 0.08);
    }}
    @keyframes authActivePop {{
        0% {{ transform: scale(0.96); opacity: 0.92; }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}
    @keyframes authFormSwitch {{
        0% {{ opacity: 0; transform: translateY(10px) scale(0.985); }}
        100% {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}
    @keyframes authContentRise {{
        0% {{ opacity: 0; transform: translateY(10px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}
    .st-key-auth_mode_signin_btn button {{
        border-radius: 9999px !important;
        border: none !important;
        height: 42px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        background: {'#151b34' if signin_active else 'transparent'} !important;
        color: {'#FFFFFF' if signin_active else '#9AA0A6'} !important;
        box-shadow: {'0 6px 20px rgba(21, 27, 52, 0.28)' if signin_active else 'none'} !important;
        transition: all 0.36s cubic-bezier(.23, 1, .32, 1) !important;
        animation: {'authActivePop 0.28s cubic-bezier(.23, 1, .32, 1)' if signin_active else 'none'} !important;
        will-change: transform, opacity, box-shadow, background, color;
    }}
    .st-key-auth_mode_signup_btn button {{
        border-radius: 9999px !important;
        border: none !important;
        height: 42px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        background: {'linear-gradient(90deg, #4f8dff, #3279F9)' if signup_active else 'transparent'} !important;
        color: {'#FFFFFF' if signup_active else '#9AA0A6'} !important;
        box-shadow: {'0 6px 20px rgba(50, 121, 249, 0.28)' if signup_active else 'none'} !important;
        transition: all 0.36s cubic-bezier(.23, 1, .32, 1) !important;
        animation: {'authActivePop 0.28s cubic-bezier(.23, 1, .32, 1)' if signup_active else 'none'} !important;
        will-change: transform, opacity, box-shadow, background, color;
    }}
    .st-key-auth_mode_signin_btn button:active,
    .st-key-auth_mode_signup_btn button:active {{
        transform: scale(0.98) !important;
    }}
    .st-key-login_signin_btn button {{
        background: #151b34 !important;
        color: white !important;
        border-radius: 14px !important;
        font-size: 16px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: transform 0.22s ease, box-shadow 0.22s ease, filter 0.22s ease;
    }}
    .st-key-login_signup_btn button {{
        background: linear-gradient(90deg, #4f8dff, #3279F9) !important;
        color: white !important;
        border-radius: 14px !important;
        font-size: 16px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 10px 28px rgba(50, 121, 249, 0.25) !important;
        transition: transform 0.22s ease, box-shadow 0.22s ease, filter 0.22s ease;
    }}
    .st-key-login_signin_btn button:hover,
    .st-key-login_signup_btn button:hover {{
        transform: translateY(-1px) !important;
        filter: brightness(1.02);
    }}
    .st-key-login_signup_btn button:hover {{
        background: linear-gradient(90deg, #3f81ff, #2a6ff2) !important;
    }}
    [data-testid="stVerticalBlockBorderWrapper"] {{
        animation: authFormSwitch 0.42s cubic-bezier(.23, 1, .32, 1);
        will-change: transform, opacity;
    }}
    .auth-title,
    .auth-sub,
    .forgot-line,
    .auth-link-row {{
        opacity: 0;
        animation: authContentRise 0.40s cubic-bezier(.23, 1, .32, 1) forwards;
        will-change: transform, opacity;
    }}
    .auth-title {{ animation-delay: 0.04s; }}
    .auth-sub {{ animation-delay: 0.08s; }}
    .forgot-line {{ animation-delay: 0.22s; }}
    .auth-link-row {{ animation-delay: 0.30s; }}
    .st-key-login_email_input,
    .st-key-login_password_input,
    .st-key-signup_name_input,
    .st-key-signup_email_input,
    .st-key-signup_password_input,
    .st-key-login_signin_btn,
    .st-key-login_signup_btn {{
        opacity: 0;
        animation: authContentRise 0.42s cubic-bezier(.23, 1, .32, 1) forwards;
        will-change: transform, opacity;
    }}
    .st-key-login_email_input,
    .st-key-signup_name_input {{ animation-delay: 0.12s; }}
    .st-key-login_password_input,
    .st-key-signup_email_input {{ animation-delay: 0.18s; }}
    .st-key-signup_password_input {{ animation-delay: 0.24s; }}
    .st-key-login_signin_btn,
    .st-key-login_signup_btn {{ animation-delay: 0.28s; }}
    .auth-hint-link {{
        color: #3279F9;
        font-weight: 600;
    }}
    [data-testid="stTextInput"] input {{
        border-radius: 12px !important;
        min-height: 48px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([0.6, 2.8, 0.6])
    with center:
        st.markdown("""
        <div class="auth-brand-wrap">
            <div style="font-size:52px; margin-bottom:6px; animation: float 4s ease-in-out infinite;">📦</div>
            <div class="hero-title-gradient" style="font-size:64px; margin-bottom:4px; letter-spacing:-2px;">Stockify</div>
            <div class="hero-sub" style="font-size:16px; margin-bottom:10px; color:#5F6368;">
                Smart inventory intelligence for Modern Retailers
            </div>
        </div>
        """, unsafe_allow_html=True)

        _, t_left, t_right, _ = st.columns([2.2, 0.8, 0.8, 2.2], gap="small")
        with t_left:
            if st.button("Sign In", key="auth_mode_signin_btn", use_container_width=True):
                st.session_state.auth_mode = "signin"
                st.rerun()
        with t_right:
            if st.button("Sign Up", key="auth_mode_signup_btn", use_container_width=True):
                st.session_state.auth_mode = "signup"
                st.rerun()

        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

        _, form_col, _ = st.columns([0.5, 2.0, 0.5], gap="small")
        with form_col:
            with st.container(border=True):
                if st.session_state.auth_mode == "signin":
                    st.markdown("<div class='auth-title'>Sign In</div>", unsafe_allow_html=True)
                    st.markdown("<div class='auth-sub'>Welcome back — please sign in.</div>", unsafe_allow_html=True)

                    username = st.text_input("Email", placeholder="admin@stockify.com", key="login_email_input")
                    password = st.text_input("Password", type="password", placeholder="••••••••", key="login_password_input")
                    st.markdown("<div class='forgot-line'>Forgot password?</div>", unsafe_allow_html=True)

                    if st.button("🚀 Sign In", use_container_width=True, key="login_signin_btn"):
                        if username in st.session_state.users and st.session_state.users.get(username) == password:
                            st.session_state.logged_in = True
                            st.session_state.auth_requested = False
                            st.session_state.show_how_it_works = False
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials. Try admin / admin")

                    st.markdown("<div class='auth-link-row'>Don't have an account? <span class='auth-hint-link'>Sign up</span></div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='auth-title'>Sign Up</div>", unsafe_allow_html=True)
                    st.markdown("<div class='auth-sub'>Create your account</div>", unsafe_allow_html=True)

                    _signup_name = st.text_input("Name", placeholder="Name", key="signup_name_input")
                    signup_email = st.text_input("Email", placeholder="example@stockify.com", key="signup_email_input")
                    signup_password = st.text_input("Password", type="password", placeholder="••••••••", key="signup_password_input")

                    if st.button("Create Account", use_container_width=True, key="login_signup_btn"):
                        if not signup_email:
                            st.error("Please enter an email for sign up.")
                        elif not signup_password:
                            st.error("Please enter a password for sign up.")
                        elif signup_email in st.session_state.users:
                            st.warning("This email is already registered. Please sign in.")
                        else:
                            st.session_state.users[signup_email] = signup_password
                            st.success("✅ Account created! Switch to Sign In to continue.")

                    st.markdown("<div class='auth-link-row'>Already have an account? <span class='auth-hint-link'>Sign in</span></div>", unsafe_allow_html=True)

# ---------------- MAIN APP ----------------
if not st.session_state.logged_in:
    if st.session_state.demo_mode_requested:
        selected_focus = st.session_state.get("selected_industry", "Grocery Stores")
        st.session_state.analytics_results = build_demo_analytics_results(selected_focus)
        st.session_state.logged_in = True
        st.session_state.user_role = "demo"
        st.session_state.current_page = "📊 Overview"
        st.session_state.auth_requested = False
        st.session_state.show_how_it_works = False
        st.session_state.demo_mode_requested = False
        st.rerun()

    if st.session_state.auth_requested:
        login_page()
    else:
        show_landing_page()
else:
    page = top_navigation()

    if page == "🏠 Home":
        show_home()
    elif page == "📂 Upload":
        show_upload()
    elif page == "📊 Overview":
        show_dashboard()
    elif page == "📦 Products":
        show_products()
    elif page == "📈 Trends":
        show_trends()
    elif page == "💡 Insights":
        show_insights()
    elif page == "🚨 Alerts":
        show_stock_alerts()
    elif page == "📉 Charts":
        show_visualizations()
    elif page == "💳 POS":
        show_pos_page()

