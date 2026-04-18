import streamlit as st
import pandas as pd
import os

# Setup path for frontend imports
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Frontend layout & page imports
from frontend.layout import set_layout
from frontend.pages.home import show_home as show_home_page
from frontend.pages.upload import show_upload
from frontend.pages.dashboard import show_dashboard
from frontend.pages.products import show_products
from frontend.pages.trends import show_trends
from frontend.pages.insights import show_insights

# Analytics layer imports
from analytics.demand_analysis import aggregate_top_products
from analytics.trend_analysis import aggregate_daily_trends
from analytics.kpi_calculator import compute_kpi_summary

# Decision support imports
from decision_support.stock_alerts import generate_stock_alerts
from decision_support.reorder_logic import generate_reorder_recommendations

# Visualization imports
from visualization.kpi_cards import render_kpi_cards
from visualization.demand_charts import plot_top_products as plot_top_products_viz
from visualization.trend_charts import plot_sales_trend
from visualization.alert_visuals import show_alerts


# -------------------------------------------------
# PAGE CONFIG & THEME
# -------------------------------------------------
set_layout()  # Apply Antigravity theme + CSS injection


# -------------------------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------------------------
def initialize_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    if "users" not in st.session_state:
        st.session_state.users = {"admin": "admin"}


initialize_session_state()


# =================================================
# AUTHENTICATION FUNCTIONS
# =================================================
def handle_sign_in(email, password):
    if email in st.session_state.users and st.session_state.users[email] == password:
        st.session_state.logged_in = True
        st.session_state.user_role = "registered"
        st.success(" Login successful!")
        st.rerun()
    else:
        st.error(" Invalid email or password")


def handle_sign_up(email, password, confirm_password):
    if not email:
        st.error(" Email cannot be empty")
        return
    if not password:
        st.error(" Password cannot be empty")
        return
    if password != confirm_password:
        st.error(" Passwords do not match")
        return
    if email in st.session_state.users:
        st.error(" Email already registered")
        return
    
    st.session_state.users[email] = password
    st.session_state.logged_in = True
    st.session_state.user_role = "registered"
    st.success(" Account created successfully!")
    st.rerun()


def handle_demo_access():
    st.session_state.logged_in = True
    st.session_state.user_role = "demo"
    st.rerun()


# =================================================
# LOGIN PAGE
# =================================================
def login_page():
    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.markdown("##  Stockify")
        st.markdown("### Smart Inventory for Retailers")
        st.markdown("---")
        st.markdown("""
        **Optimize your inventory** with intelligent insights:
        - Real-time stock monitoring
        - Demand forecasting
        - Smart reorder recommendations
        - Data-driven analytics
        """)

    with col2:
        st.markdown("### Authentication")
        
        tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
        
        with tab1:
            st.markdown("**Login to your account**")
            email_signin = st.text_input("Email", key="signin_email")
            password_signin = st.text_input("Password", type="password", key="signin_password")
            
            if st.button("Sign In", use_container_width=True, key="signin_btn"):
                handle_sign_in(email_signin, password_signin)
        
        with tab2:
            st.markdown("**Create a new account**")
            email_signup = st.text_input("Email", key="signup_email")
            password_signup = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
            
            if st.button("Sign Up", use_container_width=True, key="signup_btn"):
                handle_sign_up(email_signup, password_signup, confirm_password)
        
        st.divider()
        st.markdown("**Or try without login**")
        if st.button(" Continue as Demo User", use_container_width=True, key="demo_btn"):
            handle_demo_access()


# =================================================
# SIDEBAR NAVIGATION
# =================================================
def sidebar_navigation():
    st.sidebar.markdown("###  Stockify")
    st.sidebar.markdown("---")
    
    if st.session_state.user_role == "demo":
        st.sidebar.info(" You are using Demo Mode. Some features may be limited.")
    
    page = st.sidebar.radio(
        "Navigation",
        [
            " Home",
            " Upload",
            " Overview",
            " Products",
            " Trends",
            " Insights"
        ]
    )
    
    st.sidebar.markdown("---")
    if st.sidebar.button(" Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.rerun()
    
    return page




# =================================================
# DATA LOADING & PROCESSING
# =================================================
def load_data():
    """Load sales and inventory data with comprehensive error handling."""
    SALES_PATH = "data/processed/clean_sales.csv"
    INVENTORY_PATH = "data/processed/clean_inventory.csv"
    
    sales_df = None
    inventory_df = None
    
    # Ensure data directory exists
    os.makedirs("data/processed", exist_ok=True)
    
    # Load sales data
    try:
        if not os.path.exists(SALES_PATH):
            st.warning(f"ℹ Sales data file not found at {SALES_PATH}")
            return None, None
            
        sales_df = pd.read_csv(SALES_PATH)
        
        if sales_df.empty:
            st.warning("ℹ Sales data is empty. Please upload data first.")
            return None, None
        
        # Validate required columns
        required_sales_cols = {"product", "date", "quantity", "revenue", "category"}
        missing_cols = required_sales_cols - set(sales_df.columns)
        if missing_cols:
            st.error(f" Sales data missing columns: {', '.join(missing_cols)}")
            return None, None
            
        # Basic data type validation
        try:
            sales_df["quantity"] = pd.to_numeric(sales_df["quantity"])
            sales_df["revenue"] = pd.to_numeric(sales_df["revenue"])
        except:
            st.error(" Sales data contains invalid numeric values")
            return None, None
            
    except FileNotFoundError:
        st.warning(f"ℹ Sales data not found at {SALES_PATH}")
        return None, None
    except Exception as e:
        st.error(f" Error loading sales data: {str(e)}")
        return None, None

    # Load inventory data
    try:
        if not os.path.exists(INVENTORY_PATH):
            st.warning(f"ℹ Inventory data file not found at {INVENTORY_PATH}")
            return sales_df, None
            
        inventory_df = pd.read_csv(INVENTORY_PATH)
        
        if inventory_df.empty:
            st.warning("ℹ Inventory data is empty.")
            return sales_df, None
        
        # Validate required columns for inventory
        required_inventory_cols = {
            "Product Name", "Quantity On Hand", "Reorder Point", 
            "Unit Cost", "Selling Price"
        }
        missing_cols = required_inventory_cols - set(inventory_df.columns)
        if missing_cols:
            st.warning(f" Inventory data missing columns: {', '.join(missing_cols)}")
            # Continue anyway - alerts will be handled gracefully
            
    except FileNotFoundError:
        st.info(f"ℹ Inventory data not found at {INVENTORY_PATH}")
        return sales_df, None
    except Exception as e:
        st.warning(f" Error loading inventory data: {str(e)}")
        return sales_df, None
    
    return sales_df, inventory_df


def compute_dashboard_metrics(sales_df: pd.DataFrame) -> dict:
    """Compute key metrics from sales data with safety checks."""
    if sales_df is None or sales_df.empty:
        return {
            "total_revenue": 0,
            "total_quantity": 0,
            "avg_order_value": 0,
            "unique_products": 0
        }
    
    try:
        # Ensure columns exist
        if "revenue" not in sales_df.columns or "quantity" not in sales_df.columns:
            st.warning(" Sales data missing revenue or quantity columns")
            return {
                "total_revenue": 0,
                "total_quantity": 0,
                "avg_order_value": 0,
                "unique_products": 0
            }
        
        # Convert to numeric and handle errors
        revenue = pd.to_numeric(sales_df["revenue"], errors="coerce").fillna(0)
        quantity = pd.to_numeric(sales_df["quantity"], errors="coerce").fillna(0)
        
        total_revenue = revenue.sum()
        total_quantity = int(quantity.sum())
        num_transactions = len(sales_df)
        avg_order_value = total_revenue / num_transactions if num_transactions > 0 else 0
        
        # Handle product column
        unique_products = 0
        if "product" in sales_df.columns:
            unique_products = sales_df["product"].nunique()
        
        return {
            "total_revenue": round(total_revenue, 2),
            "total_quantity": total_quantity,
            "avg_order_value": round(avg_order_value, 2),
            "unique_products": unique_products
        }
    except Exception as e:
        st.warning(f" Error computing metrics: {str(e)}")
        return {
            "total_revenue": 0,
            "total_quantity": 0,
            "avg_order_value": 0,
            "unique_products": 0
        }


# =================================================
# MAIN
# =================================================
if not st.session_state.logged_in:
    login_page()
else:
    page = sidebar_navigation()
    
    # Debug: Show which page was selected (remove after debugging)
    # st.write(f"DEBUG: Selected page = '{page}'")

    try:
        if page == " Home":
            show_home_page()
        elif page == " Upload":
            show_upload()
        elif page == " Overview":
            # Load data and pass metrics to dashboard
            sales_df, inventory_df = load_data()
            metrics = compute_dashboard_metrics(sales_df)
            show_dashboard(metrics=metrics)
        elif page == " Products":
            show_products()
        elif page == " Trends":
            show_trends()
        elif page == " Insights":
            show_insights()
        else:
            st.error(f"❌ Unknown page: {page}")
            st.write("Available pages: Home, Upload, Overview, Products, Trends, Insights")
    except Exception as e:
        import traceback
        st.error(f"❌ Error rendering page: {page}")
        st.error(str(e))
        with st.expander("📋 Error Details"):
            st.code(traceback.format_exc())
