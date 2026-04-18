import streamlit as st
import streamlit.components.v1 as components

def set_layout():
    st.set_page_config(
        page_title="Stockify",
        page_icon="📦",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.markdown("""
    <style>
    /* ===== GOOGLE FONTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Product+Sans:wght@400;500;700&display=swap');

    /* ===== ROOT VARIABLES (Antigravity-inspired) ===== */
    :root {
        --bg-primary: #FFFFFF;
        --bg-secondary: #F8F9FC;
        --bg-card: #FFFFFF;
        --bg-card-hover: #FFFFFF;
        --bg-elevated: rgba(255, 255, 255, 0.95);
        --border-subtle: rgba(0, 0, 0, 0.08);
        --border-hover: rgba(50, 121, 249, 0.4);
        --text-primary: #121317;
        --text-secondary: #5F6368;
        --text-muted: #9AA0A6;
        --accent-blue: #3279F9;
        --accent-blue-light: #A8C7FA;
        --accent-blue-dark: #1A5CDB;
        --accent-emerald: #1E8E3E;
        --accent-amber: #F9AB00;
        --accent-rose: #D93025;
        --accent-purple: #7B61FF;
        --grey-900: #2F3034;
        --grey-1000: #212226;
        --grey-1100: #18191D;
        --grey-1200: #121317;
        --grey-100: #E1E6EC;
        --grey-50: #F1F3F4;
        --radius-sm: 8px;
        --radius-md: 16px;
        --radius-lg: 24px;
        --radius-xl: 36px;
        --radius-pill: 9999px;
        --ease-out-quint: cubic-bezier(.23, 1, .32, 1);
        --ease-out-back: cubic-bezier(.34, 1.85, .64, 1);
        --transition: all 0.4s var(--ease-out-quint);
        --font-main: 'Google Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* ===== GLOBAL RESET ===== */
    *, *::before, *::after { box-sizing: border-box; }

    .stApp {
        background: var(--bg-primary) !important;
        color: var(--text-primary);
        font-family: var(--font-main) !important;
    }

    /* Remove Streamlit's default page spacing so the landing hero can start at the very top */
    div[data-testid="stAppViewContainer"] > .main,
    div[data-testid="stAppViewContainer"] > .main > div,
    section.main > div.block-container,
    .block-container {
        padding-top: 0rem !important;
        margin-top: 0rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }

    .block-container > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    /* ===== ANTIGRAVITY GLOW BACKGROUND ===== */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background:
            radial-gradient(ellipse 80% 50% at 50% -10%, rgba(50, 121, 249, 0.08), transparent 70%),
            radial-gradient(ellipse 60% 40% at 80% 20%, rgba(168, 199, 250, 0.06), transparent 60%),
            radial-gradient(ellipse 50% 50% at 20% 80%, rgba(123, 97, 255, 0.04), transparent 60%);
        pointer-events: none;
        z-index: 0;
    }

    /* Hide default sidebar */
    section[data-testid="stSidebar"] { display: none !important; }
    button[data-testid="stSidebarCollapsedControl"] { display: none !important; }

    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: rgba(50, 121, 249, 0.2);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover { background: rgba(50, 121, 249, 0.4); }

    /* ===== KEYFRAME ANIMATIONS (Antigravity style) ===== */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(32px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInScale {
        from { opacity: 0; transform: scale(0.96); }
        to   { opacity: 1; transform: scale(1); }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-24px); }
        to   { opacity: 1; transform: translateX(0); }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50%      { transform: translateY(-10px); }
    }
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(50, 121, 249, 0.3); }
        50%      { box-shadow: 0 0 28px 10px rgba(50, 121, 249, 0.15); }
    }
    @keyframes shimmer {
        0%   { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes blinkCursor {
        0%, 49% { border-right-color: var(--accent-blue); }
        50%, 100% { border-right-color: transparent; }
    }
    @keyframes rotateGlow {
        0%   { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    @keyframes particleDrift {
        0%   { transform: translateY(0) translateX(0) scale(1); opacity: 0; }
        10%  { opacity: 1; }
        90%  { opacity: 1; }
        100% { transform: translateY(-100vh) translateX(50px) scale(0.5); opacity: 0; }
    }
    @keyframes scrollReveal {
        from { opacity: 0; transform: translateY(40px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes heroGlow {
        0%, 100% { filter: blur(60px); opacity: 0.3; }
        50%      { filter: blur(80px); opacity: 0.5; }
    }

    /* ===== SCROLL REVEAL CLASSES ===== */
    .reveal {
        opacity: 0;
        transform: translateY(40px);
        transition: all 0.8s var(--ease-out-quint);
    }
    .reveal.visible {
        opacity: 1;
        transform: translateY(0);
    }

    /* ===== TOP NAV BAR (Antigravity frosted glass) ===== */
    .top-nav {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        padding: 14px 24px;
        margin: -1rem -1rem 2rem -1rem;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        border-bottom: 1px solid rgba(0, 0, 0, 0.06);
        position: sticky;
        top: 0;
        z-index: 999;
        animation: fadeInUp 0.5s var(--ease-out-quint);
    }

    .nav-brand {
        font-size: 22px;
        font-weight: 700;
        background: linear-gradient(135deg, var(--accent-blue-light), var(--accent-blue));
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 4s ease infinite;
        margin-right: 36px;
        letter-spacing: -0.3px;
        font-family: var(--font-main);
    }

    /* ===== GLASSMORPHISM CARD (Antigravity style — clean white) ===== */
    .glass-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg);
        padding: 32px;
        transition: var(--transition);
        animation: fadeInUp 0.7s var(--ease-out-quint) backwards;
        position: relative;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(50, 121, 249, 0.3), rgba(168, 199, 250, 0.2), transparent);
        opacity: 0;
        transition: opacity 0.5s var(--ease-out-quint);
    }
    .glass-card:hover {
        transform: translateY(-8px);
        border-color: var(--border-hover);
        box-shadow:
            0 20px 60px rgba(50, 121, 249, 0.08),
            0 8px 24px rgba(0, 0, 0, 0.06),
            0 0 0 1px rgba(50, 121, 249, 0.1);
    }
    .glass-card:hover::before { opacity: 1; }

    /* ===== METRIC CARD ===== */
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg);
        padding: 28px 22px;
        text-align: center;
        transition: var(--transition);
        animation: fadeInUp 0.7s var(--ease-out-quint) backwards;
        position: relative;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: conic-gradient(from 0deg, transparent, rgba(50, 121, 249, 0.04), transparent 30%);
        animation: rotateGlow 10s linear infinite;
        opacity: 0;
        transition: opacity 0.5s ease;
    }
    .metric-card:hover::before { opacity: 1; }
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow:
            0 24px 64px rgba(50, 121, 249, 0.1),
            0 8px 24px rgba(0, 0, 0, 0.06);
    }
    .metric-card .metric-icon {
        font-size: 36px;
        margin-bottom: 10px;
        display: inline-block;
        animation: float 4s ease-in-out infinite;
    }
    .metric-card .metric-value {
        font-size: 32px;
        font-weight: 700;
        margin: 6px 0;
        letter-spacing: -1px;
        position: relative;
        z-index: 1;
        color: var(--text-primary);
    }
    .metric-card .metric-label {
        font-size: 11px;
        color: var(--text-muted);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        position: relative;
        z-index: 1;
    }

    /* Metric card color variants */
    .metric-blue { border-color: rgba(50, 121, 249, 0.15); }
    .metric-blue .metric-value { color: var(--accent-blue); }
    .metric-blue:hover {
        border-color: rgba(50, 121, 249, 0.4);
        box-shadow: 0 24px 64px rgba(50, 121, 249, 0.1), 0 0 30px rgba(50, 121, 249, 0.06);
    }

    .metric-green { border-color: rgba(30, 142, 62, 0.15); }
    .metric-green .metric-value { color: var(--accent-emerald); }
    .metric-green:hover {
        border-color: rgba(30, 142, 62, 0.4);
        box-shadow: 0 24px 64px rgba(30, 142, 62, 0.08), 0 0 30px rgba(30, 142, 62, 0.05);
    }

    .metric-purple { border-color: rgba(123, 97, 255, 0.15); }
    .metric-purple .metric-value { color: var(--accent-purple); }
    .metric-purple:hover {
        border-color: rgba(123, 97, 255, 0.4);
        box-shadow: 0 24px 64px rgba(123, 97, 255, 0.08), 0 0 30px rgba(123, 97, 255, 0.05);
    }

    .metric-orange { border-color: rgba(249, 171, 0, 0.15); }
    .metric-orange .metric-value { color: var(--accent-amber); }
    .metric-orange:hover {
        border-color: rgba(249, 171, 0, 0.4);
        box-shadow: 0 24px 64px rgba(249, 171, 0, 0.08), 0 0 30px rgba(249, 171, 0, 0.05);
    }

    .metric-red { border-color: rgba(217, 48, 37, 0.15); }
    .metric-red .metric-value { color: var(--accent-rose); }
    .metric-red:hover {
        border-color: rgba(217, 48, 37, 0.4);
        box-shadow: 0 24px 64px rgba(217, 48, 37, 0.08), 0 0 30px rgba(217, 48, 37, 0.05);
    }

    /* ===== HERO SECTION ===== */
    .hero-title {
        font-size: 72px;
        font-weight: 700;
        text-align: center;
        color: var(--text-primary);
        animation: fadeInUp 0.9s var(--ease-out-quint);
        line-height: 1.08;
        margin-bottom: 16px;
        letter-spacing: -2.5px;
        font-family: var(--font-main);
    }

    .hero-title-gradient {
        font-size: 72px;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, var(--accent-blue-light), var(--accent-blue));
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 5s ease infinite, fadeInUp 0.9s var(--ease-out-quint);
        line-height: 1.08;
        margin-bottom: 16px;
        letter-spacing: -2.5px;
        font-family: var(--font-main);
    }

    .hero-sub {
        text-align: center;
        color: var(--text-secondary);
        font-size: 20px;
        font-weight: 400;
        animation: fadeInUp 0.9s var(--ease-out-quint) 0.15s backwards;
        margin-bottom: 40px;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.65;
    }

    /* ===== TYPED CURSOR EFFECT ===== */
    .typed-cursor {
        display: inline-block;
        width: 3px;
        height: 1em;
        background: var(--accent-blue);
        margin-left: 4px;
        animation: blinkCursor 1s step-end infinite;
        vertical-align: text-bottom;
    }

    /* ===== PAGE TITLES ===== */
    .page-title {
        font-size: 42px;
        font-weight: 700;
        color: var(--text-primary);
        animation: fadeInUp 0.6s var(--ease-out-quint);
        margin-bottom: 4px;
        letter-spacing: -1.5px;
        font-family: var(--font-main);
    }
    .page-subtitle {
        color: var(--text-muted);
        font-size: 16px;
        animation: fadeInUp 0.6s var(--ease-out-quint) 0.1s backwards;
        margin-bottom: 36px;
        font-weight: 400;
    }

    /* ===== SECTION HEADERS ===== */
    .section-header {
        font-size: 20px;
        font-weight: 700;
        color: var(--text-primary);
        margin: 40px 0 20px 0;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--border-subtle);
        animation: fadeInUp 0.6s var(--ease-out-quint) backwards;
        position: relative;
    }
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -1px;
        left: 0;
        width: 64px;
        height: 2px;
        background: linear-gradient(90deg, var(--accent-blue), var(--accent-blue-light));
        border-radius: 2px;
    }

    /* ===== CHART CONTAINER ===== */
    .chart-container {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg);
        padding: 24px;
        animation: fadeInScale 0.7s var(--ease-out-quint) backwards;
        transition: var(--transition);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    .chart-container:hover {
        border-color: rgba(50, 121, 249, 0.2);
        box-shadow: 0 8px 32px rgba(50, 121, 249, 0.06);
    }

    /* ===== LOGIN CARD (Antigravity clean white) ===== */
    .login-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-xl);
        padding: 48px 44px;
        animation: fadeInScale 0.8s var(--ease-out-quint);
        box-shadow:
            0 32px 80px rgba(0, 0, 0, 0.06),
            0 8px 24px rgba(50, 121, 249, 0.04);
        position: relative;
        overflow: hidden;
    }
    .login-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-blue-light), var(--accent-blue), var(--accent-blue-light));
        background-size: 200% 100%;
        animation: shimmer 3s ease-in-out infinite;
    }
    .login-title {
        font-size: 32px;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 6px;
        letter-spacing: -0.5px;
        font-family: var(--font-main);
    }
    .login-sub {
        color: var(--text-muted);
        font-size: 15px;
        margin-bottom: 32px;
    }

    /* ===== FEATURE ITEMS ===== */
    .feature-item {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 18px 22px;
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-md);
        margin-bottom: 12px;
        transition: var(--transition);
        animation: fadeInUp 0.6s var(--ease-out-quint) backwards;
        cursor: default;
    }
    .feature-item:hover {
        background: rgba(50, 121, 249, 0.04);
        border-color: rgba(50, 121, 249, 0.2);
        transform: translateX(8px);
        box-shadow: 0 4px 20px rgba(50, 121, 249, 0.06);
    }
    .feature-icon {
        font-size: 22px;
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(50, 121, 249, 0.06);
        border: 1px solid rgba(50, 121, 249, 0.1);
        border-radius: var(--radius-md);
        flex-shrink: 0;
    }
    .feature-text {
        font-size: 15px;
        color: var(--text-secondary);
        font-weight: 500;
    }

    /* ===== UPLOAD ZONE ===== */
    .upload-zone {
        background: var(--bg-card);
        border: 2px dashed rgba(50, 121, 249, 0.2);
        border-radius: var(--radius-lg);
        padding: 28px;
        transition: var(--transition);
        animation: fadeInUp 0.6s var(--ease-out-quint) backwards;
    }
    .upload-zone:hover {
        border-color: rgba(50, 121, 249, 0.5);
        background: rgba(50, 121, 249, 0.02);
        box-shadow: 0 0 40px rgba(50, 121, 249, 0.05);
    }

    /* ===== RECOMMENDATION CARDS ===== */
    .rec-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-md);
        padding: 22px 26px;
        margin-bottom: 12px;
        display: flex;
        align-items: flex-start;
        gap: 16px;
        transition: var(--transition);
        animation: fadeInUp 0.6s var(--ease-out-quint) backwards;
        cursor: default;
    }
    .rec-card:hover {
        background: rgba(50, 121, 249, 0.03);
        border-color: rgba(50, 121, 249, 0.15);
        transform: translateX(6px);
        box-shadow: 0 8px 24px rgba(50, 121, 249, 0.06);
    }
    .rec-icon {
        font-size: 20px;
        flex-shrink: 0;
        width: 42px;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: var(--radius-md);
    }
    .rec-text {
        color: var(--text-secondary);
        font-size: 14px;
        line-height: 1.65;
    }
    .rec-text strong {
        color: var(--text-primary);
        font-weight: 600;
    }

    /* ===== DIVIDER ===== */
    hr {
        border: none;
        border-top: 1px solid var(--border-subtle);
        margin: 28px 0;
    }

    /* ===== STREAMLIT BUTTON OVERRIDES (Antigravity pill style) ===== */
    .stButton > button {
        background: var(--grey-1200) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-pill) !important;
        padding: 12px 32px !important;
        font-weight: 500 !important;
        font-size: 15px !important;
        font-family: var(--font-main) !important;
        transition: var(--transition) !important;
        letter-spacing: 0.2px;
        position: relative;
        overflow: hidden;
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.03) !important;
        background: var(--grey-900) !important;
        box-shadow: 0 12px 36px rgba(18, 19, 23, 0.2), 0 4px 12px rgba(0, 0, 0, 0.1) !important;
    }
    .stButton > button:active {
        transform: scale(0.98) !important;
    }

    /* Input fields */
    .stTextInput > div > div > input {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        font-family: var(--font-main) !important;
        padding: 14px 18px !important;
        transition: var(--transition) !important;
        font-size: 15px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 3px rgba(50, 121, 249, 0.1), 0 0 20px rgba(50, 121, 249, 0.05) !important;
        background: var(--bg-card) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: var(--text-muted) !important;
    }

    /* Labels */
    .stTextInput label, .stFileUploader label, .stSelectbox label {
        color: var(--text-secondary) !important;
        font-family: var(--font-main) !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }

    /* Dataframe */
    .stDataFrame {
        animation: fadeInUp 0.7s var(--ease-out-quint) backwards;
        border-radius: var(--radius-lg) !important;
        overflow: hidden;
    }

    /* Metric overrides */
    [data-testid="stMetric"] {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-md);
        padding: 18px;
        transition: var(--transition);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    [data-testid="stMetric"]:hover {
        border-color: rgba(50, 121, 249, 0.25);
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(50, 121, 249, 0.06);
    }
    [data-testid="stMetricLabel"] {
        color: var(--text-muted) !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 11px !important;
    }
    [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: var(--bg-card);
        border: 2px dashed rgba(50, 121, 249, 0.15);
        border-radius: var(--radius-lg);
        padding: 24px;
        transition: var(--transition);
    }
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(50, 121, 249, 0.4);
        background: rgba(50, 121, 249, 0.02);
        box-shadow: 0 0 30px rgba(50, 121, 249, 0.04);
    }

    /* Tables */
    .stTable {
        animation: fadeInUp 0.7s var(--ease-out-quint) backwards;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        font-weight: 600;
        transition: var(--transition);
        border: 1px solid var(--border-subtle);
    }
    .streamlit-expanderHeader:hover {
        background: rgba(50, 121, 249, 0.04) !important;
        border-color: rgba(50, 121, 249, 0.15);
    }

    /* Alerts */
    .stAlert {
        border-radius: var(--radius-md) !important;
        animation: fadeInUp 0.4s var(--ease-out-quint);
        background: var(--bg-card) !important;
        border: 1px solid var(--border-subtle) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 4px; }
    .stTabs [data-baseweb="tab"] {
        background: var(--bg-card);
        border-radius: var(--radius-pill);
        color: var(--text-secondary);
        border: 1px solid transparent;
        transition: var(--transition);
        font-family: var(--font-main);
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(50, 121, 249, 0.06);
        color: var(--text-primary);
    }
    .stTabs [aria-selected="true"] {
        background: var(--accent-blue) !important;
        color: white !important;
        border-color: var(--accent-blue) !important;
    }

    /* Hide streamlit branding */
    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }
    footer { visibility: hidden; }

    /* ===== STAT BADGE ===== */
    .stat-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: var(--radius-pill);
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    .stat-badge-green {
        background: rgba(30, 142, 62, 0.08);
        color: var(--accent-emerald);
        border: 1px solid rgba(30, 142, 62, 0.15);
    }
    .stat-badge-red {
        background: rgba(217, 48, 37, 0.08);
        color: var(--accent-rose);
        border: 1px solid rgba(217, 48, 37, 0.15);
    }

    /* ===== ANIMATION DELAYS ===== */
    .delay-1 { animation-delay: 0.08s !important; }
    .delay-2 { animation-delay: 0.16s !important; }
    .delay-3 { animation-delay: 0.24s !important; }
    .delay-4 { animation-delay: 0.32s !important; }
    .delay-5 { animation-delay: 0.40s !important; }
    .delay-6 { animation-delay: 0.48s !important; }

    /* ===== GLOW HIGHLIGHT ===== */
    .glow-box {
        position: relative;
    }
    .glow-box::after {
        content: '';
        position: absolute;
        inset: -1px;
        border-radius: var(--radius-lg);
        background: linear-gradient(135deg, var(--accent-blue), var(--accent-blue-light), var(--accent-blue));
        z-index: -1;
        opacity: 0;
        transition: opacity 0.4s ease;
        filter: blur(16px);
    }
    .glow-box:hover::after { opacity: 0.12; }

    /* ===== PARTICLE CANVAS CONTAINER ===== */
    #particle-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
    }

    /* ===== ANTIGRAVITY-STYLE LARGE SECTION TITLE ===== */
    .ag-section-title {
        font-size: 48px;
        font-weight: 700;
        color: var(--text-primary);
        text-align: center;
        letter-spacing: -2px;
        margin-bottom: 16px;
        line-height: 1.1;
        font-family: var(--font-main);
    }

    .ag-section-subtitle {
        font-size: 18px;
        color: var(--text-secondary);
        text-align: center;
        max-width: 560px;
        margin: 0 auto 48px auto;
        line-height: 1.6;
    }

    /* ===== ANTIGRAVITY-STYLE PILL LINK ===== */
    .ag-pill-link {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 10px 24px;
        background: var(--bg-secondary);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-pill);
        color: var(--text-secondary);
        font-size: 14px;
        font-weight: 500;
        text-decoration: none;
        transition: var(--transition);
        cursor: pointer;
    }
    .ag-pill-link:hover {
        background: rgba(50, 121, 249, 0.06);
        border-color: rgba(50, 121, 249, 0.2);
        color: var(--accent-blue);
    }

    </style>
    """, unsafe_allow_html=True)

    # ===== ALL JAVASCRIPT (particles, scroll reveal, cursor glow) =====
    # Using components.html() to properly execute JavaScript
    # (st.markdown strips <script> tags which causes text artifacts)
    components.html("""
    <script>
    (function() {
        const doc = window.parent.document;

        // ===== PARTICLE CANVAS =====
        if (!doc.getElementById('particle-canvas')) {
            const canvas = doc.createElement('canvas');
            canvas.id = 'particle-canvas';
            canvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;';
            doc.body.appendChild(canvas);

            const ctx = canvas.getContext('2d');
            let particles = [];

            function resize() {
                canvas.width = window.parent.innerWidth;
                canvas.height = window.parent.innerHeight;
            }
            resize();
            window.parent.addEventListener('resize', resize);

            class Particle {
                constructor() { this.reset(); }
                reset() {
                    this.x = Math.random() * canvas.width;
                    this.y = Math.random() * canvas.height;
                    this.size = Math.random() * 2.5 + 0.5;
                    this.speedX = (Math.random() - 0.5) * 0.3;
                    this.speedY = (Math.random() - 0.5) * 0.3;
                    this.opacity = Math.random() * 0.4 + 0.1;
                    this.color = Math.random() > 0.5
                        ? 'rgba(50, 121, 249, ' + this.opacity + ')'
                        : 'rgba(168, 199, 250, ' + (this.opacity * 1.5) + ')';
                }
                update() {
                    this.x += this.speedX;
                    this.y += this.speedY;
                    if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
                    if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
                }
                draw() {
                    ctx.beginPath();
                    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                    ctx.fillStyle = this.color;
                    ctx.fill();
                }
            }

            for (let i = 0; i < 60; i++) particles.push(new Particle());

            function connectParticles() {
                for (let i = 0; i < particles.length; i++) {
                    for (let j = i + 1; j < particles.length; j++) {
                        const dx = particles[i].x - particles[j].x;
                        const dy = particles[i].y - particles[j].y;
                        const dist = Math.sqrt(dx * dx + dy * dy);
                        if (dist < 150) {
                            ctx.beginPath();
                            ctx.strokeStyle = 'rgba(50, 121, 249, ' + (0.04 * (1 - dist / 150)) + ')';
                            ctx.lineWidth = 0.5;
                            ctx.moveTo(particles[i].x, particles[i].y);
                            ctx.lineTo(particles[j].x, particles[j].y);
                            ctx.stroke();
                        }
                    }
                }
            }

            function animate() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                particles.forEach(function(p) { p.update(); p.draw(); });
                connectParticles();
                requestAnimationFrame(animate);
            }
            animate();
        }

        // ===== SCROLL REVEAL OBSERVER =====
        if (!doc._scrollRevealInitialized) {
            doc._scrollRevealInitialized = true;
            const observer = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                    }
                });
            }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

            function observeAll() {
                doc.querySelectorAll('.reveal').forEach(function(el) { observer.observe(el); });
            }
            observeAll();

            const mutationObserver = new MutationObserver(function() {
                setTimeout(observeAll, 100);
            });
            mutationObserver.observe(doc.body, { childList: true, subtree: true });
        }

        // ===== CURSOR SPARKLE TRAIL (Stars & Rhombus shapes) =====
        if (!doc.getElementById('sparkle-canvas')) {
            const sparkleCanvas = doc.createElement('canvas');
            sparkleCanvas.id = 'sparkle-canvas';
            sparkleCanvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:1;';
            doc.body.appendChild(sparkleCanvas);

            const sCtx = sparkleCanvas.getContext('2d');
            let sparkles = [];
            let sMouse = { x: window.parent.innerWidth / 2, y: window.parent.innerHeight / 2 };
            let lastMouse = { x: sMouse.x, y: sMouse.y };
            let frameCount = 0;

            function resizeSparkle() {
                sparkleCanvas.width = window.parent.innerWidth;
                sparkleCanvas.height = window.parent.innerHeight;
            }
            resizeSparkle();
            window.parent.addEventListener('resize', resizeSparkle);

            doc.addEventListener('mousemove', function(e) {
                sMouse.x = e.clientX;
                sMouse.y = e.clientY;
            });

            var sparkleColors = [
                [50, 121, 249],   // blue
                [123, 97, 255],   // purple
                [168, 199, 250],  // light blue
                [100, 149, 237],  // cornflower
                [147, 130, 255],  // lavender
                [80, 160, 255],   // sky blue
            ];

            function createSparkle(x, y) {
                var colorArr = sparkleColors[Math.floor(Math.random() * sparkleColors.length)];
                return {
                    x: x + (Math.random() - 0.5) * 20,
                    y: y + (Math.random() - 0.5) * 20,
                    size: Math.random() * 8 + 4,
                    rotation: Math.random() * Math.PI * 2,
                    rotationSpeed: (Math.random() - 0.5) * 0.15,
                    vx: (Math.random() - 0.5) * 1.5,
                    vy: (Math.random() - 0.5) * 1.5 - 0.5,
                    life: 1.0,
                    decay: Math.random() * 0.015 + 0.012,
                    color: colorArr,
                    type: Math.random() > 0.45 ? 'star' : 'rhombus'
                };
            }

            function drawStar(ctx, x, y, size, rotation, color, alpha) {
                ctx.save();
                ctx.translate(x, y);
                ctx.rotate(rotation);
                ctx.beginPath();
                var spikes = 4;
                var outerR = size;
                var innerR = size * 0.4;
                for (var i = 0; i < spikes * 2; i++) {
                    var r = (i % 2 === 0) ? outerR : innerR;
                    var angle = (i * Math.PI) / spikes - Math.PI / 2;
                    if (i === 0) ctx.moveTo(Math.cos(angle) * r, Math.sin(angle) * r);
                    else ctx.lineTo(Math.cos(angle) * r, Math.sin(angle) * r);
                }
                ctx.closePath();
                ctx.fillStyle = 'rgba(' + color[0] + ',' + color[1] + ',' + color[2] + ',' + alpha + ')';
                ctx.shadowColor = 'rgba(' + color[0] + ',' + color[1] + ',' + color[2] + ',' + (alpha * 0.6) + ')';
                ctx.shadowBlur = size * 2;
                ctx.fill();
                ctx.restore();
            }

            function drawRhombus(ctx, x, y, size, rotation, color, alpha) {
                ctx.save();
                ctx.translate(x, y);
                ctx.rotate(rotation);
                ctx.beginPath();
                ctx.moveTo(0, -size);
                ctx.lineTo(size * 0.6, 0);
                ctx.lineTo(0, size);
                ctx.lineTo(-size * 0.6, 0);
                ctx.closePath();
                ctx.fillStyle = 'rgba(' + color[0] + ',' + color[1] + ',' + color[2] + ',' + alpha + ')';
                ctx.shadowColor = 'rgba(' + color[0] + ',' + color[1] + ',' + color[2] + ',' + (alpha * 0.5) + ')';
                ctx.shadowBlur = size * 1.5;
                ctx.fill();
                ctx.restore();
            }

            function animateSparkles() {
                sCtx.clearRect(0, 0, sparkleCanvas.width, sparkleCanvas.height);
                frameCount++;

                // Spawn new sparkles based on mouse movement
                var dx = sMouse.x - lastMouse.x;
                var dy = sMouse.y - lastMouse.y;
                var speed = Math.sqrt(dx * dx + dy * dy);

                if (speed > 2 && frameCount % 2 === 0) {
                    var count = Math.min(Math.floor(speed / 8) + 1, 3);
                    for (var c = 0; c < count; c++) {
                        if (sparkles.length < 50) {
                            sparkles.push(createSparkle(sMouse.x, sMouse.y));
                        }
                    }
                }
                // Also spawn occasional sparkle even when still
                if (frameCount % 12 === 0 && sparkles.length < 50) {
                    sparkles.push(createSparkle(sMouse.x, sMouse.y));
                }

                lastMouse.x = sMouse.x;
                lastMouse.y = sMouse.y;

                // Update and draw
                for (var i = sparkles.length - 1; i >= 0; i--) {
                    var s = sparkles[i];
                    s.x += s.vx;
                    s.y += s.vy;
                    s.vy -= 0.01; // slight upward drift
                    s.rotation += s.rotationSpeed;
                    s.life -= s.decay;
                    s.size *= 0.995;

                    if (s.life <= 0) {
                        sparkles.splice(i, 1);
                        continue;
                    }

                    var alpha = s.life * 0.7;
                    if (s.type === 'star') {
                        drawStar(sCtx, s.x, s.y, s.size, s.rotation, s.color, alpha);
                    } else {
                        drawRhombus(sCtx, s.x, s.y, s.size, s.rotation, s.color, alpha);
                    }
                }

                requestAnimationFrame(animateSparkles);
            }
            animateSparkles();
        }
    })();
    </script>
    """, height=0)

