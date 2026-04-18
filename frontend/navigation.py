import streamlit as st

def top_navigation():
    """Render an Antigravity-style frosted glass top navigation bar."""

    if "current_page" not in st.session_state:
        st.session_state.current_page = "🏠 Home"

    pages = [
        ("🏠", "Home"),
        ("📂", "Upload"),
        ("💳", "POS"),
        ("📊", "Overview"),
        ("📦", "Products"),
        ("📈", "Trends"),
        ("💡", "Insights"),
        ("🚨", "Alerts"),
        ("📉", "Charts"),
    ]

    # Build columns: brand + pages + logout
    # Use container with custom CSS for horizontal scrollable nav
    st.markdown("""
    <style>
    .nav-row { display:flex; align-items:center; gap:6px; padding:8px 0; flex-wrap:nowrap; }
    .nav-row .stButton > button { min-width:0 !important; white-space:nowrap !important; }
    </style>
    """, unsafe_allow_html=True)

    cols = st.columns([1.3] + [1] * len(pages) + [1])

    # Brand
    with cols[0]:
        st.markdown(
            "<div class='nav-brand'>📦 Stockify</div>",
            unsafe_allow_html=True,
        )

    # Nav buttons — icon-only for compact layout
    for i, (icon, label) in enumerate(pages):
        full_label = f"{icon} {label}"
        col_index = i + 2  # 1-indexed for CSS nth-child

        with cols[i + 1]:
            is_active = st.session_state.current_page == full_label

            if is_active:
                st.markdown(f"""
                <style>
                div[data-testid="stHorizontalBlock"] > div:nth-child({col_index}) .stButton > button {{
                    background: #3279F9 !important;
                    color: white !important;
                    border-radius: 9999px !important;
                    box-shadow: 0 4px 16px rgba(50, 121, 249, 0.2) !important;
                    border: none !important;
                    font-weight: 600 !important;
                    font-size: 12px !important;
                    padding: 8px 6px !important;
                }}
                </style>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <style>
                div[data-testid="stHorizontalBlock"] > div:nth-child({col_index}) .stButton > button {{
                    background: transparent !important;
                    border: 1px solid rgba(0, 0, 0, 0.06) !important;
                    color: #5F6368 !important;
                    border-radius: 9999px !important;
                    font-size: 12px !important;
                    padding: 8px 6px !important;
                }}
                div[data-testid="stHorizontalBlock"] > div:nth-child({col_index}) .stButton > button:hover {{
                    background: rgba(50, 121, 249, 0.06) !important;
                    border-color: rgba(50, 121, 249, 0.15) !important;
                    color: #3279F9 !important;
                    box-shadow: 0 4px 16px rgba(50, 121, 249, 0.08) !important;
                }}
                </style>
                """, unsafe_allow_html=True)

            # Use just icon for button label
            if st.button(f"{icon}", key=f"nav_{label}", use_container_width=True, help=label):
                st.session_state.current_page = full_label
                st.rerun()

    # Logout button (red accent, pill style)
    logout_col_index = len(pages) + 2
    with cols[-1]:
        st.markdown(f"""
        <style>
        div[data-testid="stHorizontalBlock"] > div:nth-child({logout_col_index}) .stButton > button {{
            background: rgba(217, 48, 37, 0.06) !important;
            border: 1px solid rgba(217, 48, 37, 0.12) !important;
            color: #D93025 !important;
            border-radius: 9999px !important;
            font-size: 12px !important;
            padding: 8px 6px !important;
        }}
        div[data-testid="stHorizontalBlock"] > div:nth-child({logout_col_index}) .stButton > button:hover {{
            background: rgba(217, 48, 37, 0.12) !important;
            border-color: rgba(217, 48, 37, 0.25) !important;
            box-shadow: 0 4px 16px rgba(217, 48, 37, 0.1) !important;
        }}
        </style>
        """, unsafe_allow_html=True)
        if st.button("🚪", key="nav_logout", use_container_width=True, help="Logout"):
            st.session_state.logged_in = False
            st.session_state.current_page = "🏠 Home"
            st.session_state.auth_requested = False
            st.session_state.show_how_it_works = False
            st.rerun()

    # Separator
    st.markdown(
        "<hr style='margin: 8px 0 32px 0; border-top: 1px solid rgba(0, 0, 0, 0.05);'>",
        unsafe_allow_html=True,
    )

    return st.session_state.current_page
