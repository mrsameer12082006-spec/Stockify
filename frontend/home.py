import streamlit as st
import streamlit.components.v1 as components


def styles():
    st.markdown(
        """
        <style>
        :root {
            --stockify-blue: #3279F9;
            --stockify-blue-dark: #1A5CDB;
            --stockify-blue-light: #A8C7FA;
            --stockify-text: #121317;
            --stockify-subtle: #5F6368;
            --stockify-border: rgba(50, 121, 249, 0.14);
        }

        html, body {
            scroll-behavior: smooth;
        }

        .landing-shell {
            width: 100%;
            min-height: 100vh;
            position: relative;
            overflow: hidden;
        }

        .landing-shell::before {
            content: '';
            position: absolute;
            inset: 0;
            background:
                radial-gradient(circle at 18% 16%, rgba(50, 121, 249, 0.10), transparent 26%),
                radial-gradient(circle at 82% 20%, rgba(168, 199, 250, 0.12), transparent 22%),
                linear-gradient(180deg, rgba(248, 249, 252, 0.65) 0%, rgba(255, 255, 255, 0.95) 55%, rgba(248, 249, 252, 0.88) 100%);
            pointer-events: none;
            z-index: 0;
        }

        .landing-content {
            position: relative;
            z-index: 1;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 0.5rem 0 2rem 0;
        }

        .landing-nav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: clamp(1.5rem, 4vw, 3rem);
        }

        .landing-brand {
            display: inline-flex;
            align-items: center;
            gap: 14px;
            font-family: var(--font-main);
        }

        .landing-brand-badge {
            width: 52px;
            height: 52px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(50, 121, 249, 0.14), rgba(168, 199, 250, 0.22));
            border: 1px solid rgba(50, 121, 249, 0.12);
            box-shadow: 0 12px 32px rgba(50, 121, 249, 0.10);
            font-size: 24px;
        }

        .landing-brand-copy {
            display: flex;
            flex-direction: column;
            line-height: 1.1;
        }

        .landing-brand-title {
            font-size: 22px;
            font-weight: 700;
            color: var(--stockify-text);
            letter-spacing: -0.4px;
        }

        .landing-brand-subtitle {
            font-size: 13px;
            color: var(--stockify-subtle);
            margin-top: 4px;
        }

        .landing-canvas {
            max-width: 1100px;
            margin: 1.2rem auto 2rem auto;
            padding: 20px 28px 30px 28px;
            border-radius: 28px;
            background: linear-gradient(180deg, rgba(251, 253, 255, 0.95) 0%, rgba(255, 255, 255, 0.98) 100%);
            border: 1px solid rgba(50, 121, 249, 0.10);
            box-shadow: 0 28px 70px rgba(26, 92, 219, 0.08), 0 8px 22px rgba(0, 0, 0, 0.04);
        }

        .top-mini-dot {
            width: 8px;
            height: 8px;
            border-radius: 9999px;
            background: rgba(168, 199, 250, 0.7);
            display: inline-block;
            margin-right: 4px;
        }

        .landing-top-links {
            display: flex;
            justify-content: flex-end;
            gap: 12px;
            align-items: center;
            margin-top: 0;
            flex-wrap: nowrap;
        }

        .landing-top-links .nav-link {
            color: #606773;
            font-size: 16px;
            font-weight: 700;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 130px;
            height: 48px;
            border-radius: 9999px;
            border: 1px solid rgba(50, 121, 249, 0.16);
            background: rgba(255, 255, 255, 0.82);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            transition: transform 0.24s cubic-bezier(.23, 1, .32, 1),
                        box-shadow 0.24s ease,
                        color 0.24s ease,
                        border-color 0.24s ease,
                        background 0.24s ease;
            animation: chipPopIn 0.45s cubic-bezier(.23, 1, .32, 1) both;
        }

        .landing-top-links .nav-link:hover {
            color: #FFFFFF;
            border-color: #3279F9;
            background: linear-gradient(135deg, #3279F9 0%, #5A8DFF 100%);
            box-shadow: 0 12px 26px rgba(50, 121, 249, 0.3);
            transform: translateY(-3px) scale(1.02);
        }

        .landing-top-links .nav-link.disabled {
            color: #707784;
            cursor: default;
            pointer-events: none;
        }

        .landing-top-links .nav-link.js-features-link { animation-delay: 0.04s; }
        .landing-top-links .nav-link.docs-link { animation-delay: 0.16s; }

        .landing-top-links .nav-link.disabled {
            animation-delay: 0.1s;
        }

        .landing-nav .stButton > button {
            background: transparent !important;
            color: var(--stockify-blue) !important;
            border: 1px solid rgba(50, 121, 249, 0.20) !important;
            border-radius: 9999px !important;
            padding: 10px 22px !important;
            font-weight: 600 !important;
        }

        .landing-nav .stButton > button:hover {
            background: rgba(50, 121, 249, 0.06) !important;
            border-color: rgba(50, 121, 249, 0.36) !important;
            box-shadow: 0 10px 26px rgba(50, 121, 249, 0.12) !important;
        }

        .st-key-landing_login_nav button {
            min-width: 165px !important;
            max-width: 165px !important;
            width: 165px !important;
            height: 48px !important;
            border-radius: 9999px !important;
            background: #0B0E18 !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(11, 14, 24, 0.95) !important;
            font-size: 16px !important;
            font-weight: 700 !important;
            box-shadow: 0 10px 22px rgba(11, 14, 24, 0.24) !important;
            margin-left: 0 !important;
            transition: transform 0.22s cubic-bezier(.23, 1, .32, 1), box-shadow 0.22s ease !important;
        }

        .st-key-landing_login_nav button:hover {
            transform: translateY(-2px) scale(1.01) !important;
            box-shadow: 0 14px 28px rgba(11, 14, 24, 0.3) !important;
            background: #131827 !important;
        }

        .landing-hero-grid {
            align-items: center;
            gap: clamp(1.5rem, 4vw, 4rem);
        }

        .landing-kicker {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 16px;
            border-radius: 9999px;
            background: rgba(255, 255, 255, 0.76);
            border: 1px solid rgba(50, 121, 249, 0.12);
            color: var(--stockify-blue-dark);
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 22px;
            box-shadow: 0 8px 24px rgba(50, 121, 249, 0.06);
        }

        .landing-title {
            font-size: clamp(50px, 5vw, 64px);
            line-height: 1.04;
            font-weight: 800;
            letter-spacing: -2.5px;
            color: var(--stockify-text);
            margin: 0 0 18px 0;
            max-width: 9.5ch;
        }

        .landing-title .accent {
            color: var(--stockify-blue);
        }

        .landing-subtitle {
            max-width: 620px;
            font-size: 18px;
            line-height: 1.7;
            color: var(--stockify-subtle);
            margin-bottom: 28px;
        }

        .landing-stack {
            width: 100%;
            max-width: 1040px;
            margin: 0 auto;
            text-align: left;
        }

        .landing-stack .landing-subtitle {
            max-width: 520px;
        }

        .landing-cta-buttons {
            max-width: 360px;
            margin: 0;
        }

        .landing-cta-buttons .stButton {
            margin-bottom: 10px;
        }

        /* CTA colors to match reference */
        .st-key-landing_get_started button {
            background: linear-gradient(180deg, #3B82F6 0%, #2F6FE8 100%) !important;
            color: #FFFFFF !important;
            border: 1px solid #2F6FE8 !important;
            border-radius: 9999px !important;
            box-shadow: 0 10px 22px rgba(47, 111, 232, 0.28) !important;
            font-weight: 600 !important;
        }

        .st-key-landing_get_started button:hover {
            background: linear-gradient(180deg, #347AF1 0%, #2A64D9 100%) !important;
            border-color: #2A64D9 !important;
            transform: translateY(-1px) !important;
        }

        .st-key-landing_how_it_works button {
            background: #FFFFFF !important;
            color: #2F6FE8 !important;
            border: 1.5px solid #2F6FE8 !important;
            border-radius: 9999px !important;
            box-shadow: none !important;
            font-weight: 600 !important;
        }

        .st-key-landing_how_it_works button:hover {
            background: rgba(47, 111, 232, 0.06) !important;
            color: #245BD0 !important;
            border-color: #245BD0 !important;
            transform: translateY(-1px) !important;
        }

        .landing-features-stack {
            width: 100%;
            max-width: 100%;
            margin: 22px auto 0 auto;
            text-align: center;
            display: grid;
            gap: 10px;
        }

        #features-section {
            scroll-margin-top: 26px;
        }

        @keyframes sectionGlow {
            0% {
                box-shadow: 0 0 0 rgba(50, 121, 249, 0);
                transform: translateY(0);
            }
            35% {
                box-shadow: 0 0 0 6px rgba(50, 121, 249, 0.12);
                transform: translateY(-2px);
            }
            100% {
                box-shadow: 0 0 0 rgba(50, 121, 249, 0);
                transform: translateY(0);
            }
        }

        .features-focus {
            animation: sectionGlow 0.95s cubic-bezier(.23, 1, .32, 1);
            border-radius: 18px;
        }

        .developers-focus {
            animation: sectionGlow 0.95s cubic-bezier(.23, 1, .32, 1);
            border-radius: 18px;
        }

        .landing-main-hero {
            margin-top: 18px;
        }

        .landing-cta-row {
            margin-top: 6px;
        }

        .landing-cta-row .stButton > button {
            border-radius: 9999px !important;
            padding: 14px 28px !important;
            font-size: 15px !important;
            font-weight: 700 !important;
            transition: all 0.25s ease !important;
        }

        .landing-primary-btn .stButton > button {
            background: linear-gradient(135deg, var(--stockify-blue), var(--stockify-blue-dark)) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 14px 32px rgba(50, 121, 249, 0.24) !important;
        }

        .landing-primary-btn .stButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 18px 40px rgba(50, 121, 249, 0.30) !important;
        }

        .landing-secondary-btn .stButton > button {
            background: transparent !important;
            color: var(--stockify-blue) !important;
            border: 1px solid rgba(50, 121, 249, 0.22) !important;
        }

        .landing-secondary-btn .stButton > button:hover {
            background: rgba(50, 121, 249, 0.05) !important;
            border-color: rgba(50, 121, 249, 0.34) !important;
        }

        .hero-features {
            margin-top: 26px;
        }

        .hero-feature {
            display: flex;
            align-items: center;
            gap: 14px;
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid rgba(50, 121, 249, 0.11);
            border-radius: 18px;
            padding: 14px 16px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        }

        .hero-feature.pill {
            border-radius: 16px;
            justify-content: flex-start;
            padding: 12px 14px;
            min-height: 58px;
            cursor: pointer;
            transition: transform 0.24s cubic-bezier(.23, 1, .32, 1),
                        border-color 0.24s ease,
                        background 0.24s ease,
                        box-shadow 0.24s ease;
            transform: translateY(0) scale(1);
        }

        .hero-feature.pill:hover {
            border-color: #111111;
            background: linear-gradient(135deg, #3279F9 0%, #5A8DFF 100%);
            box-shadow: 0 12px 24px rgba(50, 121, 249, 0.26);
            transform: translateY(-5px) scale(1.02);
        }

        .hero-feature.pill:hover .hero-feature-text {
            color: #FFFFFF;
        }

        .hero-feature.pill:hover .hero-feature-icon {
            background: rgba(255, 255, 255, 0.18);
            border-color: rgba(255, 255, 255, 0.35);
            box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.2);
        }

        .hero-feature-icon {
            width: 42px;
            height: 42px;
            border-radius: 14px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: rgba(50, 121, 249, 0.08);
            border: 1px solid rgba(50, 121, 249, 0.12);
            font-size: 18px;
            flex-shrink: 0;
        }

        .hero-feature-text {
            color: var(--stockify-text);
            font-size: 14px;
            line-height: 1.45;
            font-weight: 500;
        }

        .hero-preview {
            background: rgba(255, 255, 255, 0.86);
            border: 1px solid rgba(50, 121, 249, 0.12);
            border-radius: 32px;
            box-shadow:
                0 30px 80px rgba(50, 121, 249, 0.10),
                0 4px 18px rgba(0, 0, 0, 0.05);
            padding: 22px;
            margin: 0;
            max-width: 100%;
            text-align: left;
        }

        .hero-preview-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 18px;
        }

        .hero-preview-chip {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            border-radius: 9999px;
            background: rgba(50, 121, 249, 0.08);
            color: var(--stockify-blue-dark);
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.2px;
        }

        .hero-preview-metrics {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 14px;
            margin-bottom: 14px;
        }

        .hero-preview-card {
            background: white;
            border: 1px solid rgba(0, 0, 0, 0.06);
            border-radius: 22px;
            padding: 16px;
        }

        .hero-preview-label {
            font-size: 12px;
            color: var(--stockify-subtle);
            margin-bottom: 8px;
        }

        .hero-preview-value {
            font-size: 26px;
            font-weight: 800;
            letter-spacing: -1px;
            color: var(--stockify-text);
        }

        .hero-preview-note {
            margin-top: 8px;
            font-size: 12px;
            color: var(--stockify-subtle);
            line-height: 1.5;
        }

        .hero-preview-list {
            display: grid;
            gap: 12px;
        }

        .hero-preview-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            padding: 14px 16px;
            border-radius: 18px;
            background: linear-gradient(180deg, rgba(248, 249, 252, 0.96), rgba(255, 255, 255, 0.98));
            border: 1px solid rgba(50, 121, 249, 0.08);
        }

        .hero-preview-item strong {
            color: var(--stockify-text);
            font-size: 14px;
        }

        .hero-preview-item span {
            color: var(--stockify-subtle);
            font-size: 12px;
        }

        .landing-trusted {
            margin-top: 22px;
            text-align: center;
        }

        .landing-trusted h4 {
            margin: 0;
            font-size: 26px;
            letter-spacing: -0.6px;
            color: #20252F;
        }

        .landing-chip-row {
            margin-top: 12px;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
        }

        .landing-chip {
            padding: 7px 14px;
            border-radius: 9999px;
            background: rgba(50, 121, 249, 0.06);
            border: 1px solid rgba(50, 121, 249, 0.12);
            color: #5F6368;
            font-size: 12px;
            font-weight: 600;
        }

        @keyframes chipPopIn {
            0% {
                opacity: 0;
                transform: translateY(10px) scale(0.92);
            }
            70% {
                opacity: 1;
                transform: translateY(-2px) scale(1.03);
            }
            100% {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        [class*="st-key-chip_"] button {
            width: 100%;
            border-radius: 9999px !important;
            background: rgba(50, 121, 249, 0.08) !important;
            border: 1px solid rgba(50, 121, 249, 0.18) !important;
            color: #4F5B6D !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            padding: 10px 14px !important;
            transition: all 0.26s ease !important;
            animation: chipPopIn 0.55s cubic-bezier(.23, 1, .32, 1) both;
        }

        [class*="st-key-chip_"] button:hover {
            background: linear-gradient(135deg, #3279F9 0%, #5A8DFF 100%) !important;
            color: #FFFFFF !important;
            border-color: #3279F9 !important;
            box-shadow: 0 10px 24px rgba(50, 121, 249, 0.26) !important;
            transform: translateY(-2px) scale(1.02) !important;
        }

        [class*="st-key-chip_"] button:active {
            transform: scale(0.98) !important;
        }

        .st-key-chip_grocery_stores button { animation-delay: 0.05s; }
        .st-key-chip_pharmacy button { animation-delay: 0.12s; }
        .st-key-chip_electronics_shops button { animation-delay: 0.19s; }
        .st-key-chip_fashion_stores button { animation-delay: 0.26s; }

        .industry-selected-note {
            margin-top: 10px;
            text-align: center;
            color: #4F5B6D;
            font-size: 13px;
        }

        .industry-selected-note strong {
            color: #245BD0;
        }

        .landing-steps {
            margin-top: 24px;
            border-radius: 20px;
            border: 1px solid rgba(50, 121, 249, 0.10);
            background: rgba(255, 255, 255, 0.9);
            padding: 16px;
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
        }

        .landing-step-card {
            border-radius: 16px;
            padding: 10px 12px;
            background: #fff;
            border: 1px solid rgba(0, 0, 0, 0.06);
            transition: transform 0.24s cubic-bezier(.23, 1, .32, 1),
                        box-shadow 0.24s ease,
                        border-color 0.24s ease;
            transform: translateY(0) scale(1);
        }

        .landing-step-card:hover {
            border-color: #111111;
            transform: translateY(-6px) scale(1.025);
            box-shadow: 0 14px 26px rgba(0, 0, 0, 0.14);
        }

        .landing-step-card .num {
            font-size: 11px;
            color: #9AA0A6;
            font-weight: 700;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            margin-bottom: 7px;
        }

        .landing-step-card .ttl {
            font-size: 24px;
            line-height: 1;
            font-weight: 700;
            color: #1A5CDB;
            margin-bottom: 7px;
        }

        .landing-step-card .txt {
            font-size: 12px;
            line-height: 1.55;
            color: #5F6368;
        }

        .developers-section {
            margin-top: 30px;
            padding: 22px 4px 8px 4px;
        }

        .developers-heading {
            text-align: center;
            font-size: 34px;
            font-weight: 700;
            color: #20252F;
            letter-spacing: -0.6px;
            margin: 0;
        }

        .developers-subheading {
            text-align: center;
            margin-top: 6px;
            margin-bottom: 20px;
            color: #7B828F;
            font-size: 15px;
            font-weight: 500;
        }

        .developers-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 14px;
        }

        .developer-card {
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid rgba(50, 121, 249, 0.14);
            border-radius: 18px;
            box-shadow: 0 3px 12px rgba(0, 0, 0, 0.04);
            padding: 16px;
            min-height: 176px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.24s cubic-bezier(.23, 1, .32, 1),
                        box-shadow 0.24s ease,
                        border-color 0.24s ease;
        }

        .developer-card:hover {
            transform: translateY(-5px);
            border-color: rgba(50, 121, 249, 0.28);
            box-shadow: 0 14px 26px rgba(50, 121, 249, 0.16);
        }

        .developer-top {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 10px;
        }

        .developer-avatar {
            width: 48px;
            height: 48px;
            border-radius: 9999px;
            background: linear-gradient(135deg, rgba(50, 121, 249, 0.22) 0%, rgba(168, 199, 250, 0.34) 100%);
            border: 1px solid rgba(50, 121, 249, 0.24);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: #1A5CDB;
            font-size: 18px;
            font-weight: 700;
            flex-shrink: 0;
        }

        .developer-name {
            font-size: 18px;
            font-weight: 700;
            color: #1F2430;
            line-height: 1.2;
            margin: 0;
        }

        .developer-links {
            display: grid;
            gap: 8px;
            margin-top: 6px;
        }

        .developer-link {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: #4F5B6D;
            text-decoration: none;
            font-size: 13px;
            font-weight: 500;
            padding: 7px 10px;
            border-radius: 10px;
            border: 1px solid rgba(50, 121, 249, 0.12);
            background: rgba(50, 121, 249, 0.04);
            transition: all 0.2s ease;
            min-height: 34px;
            word-break: break-all;
        }

        .developer-link:hover {
            color: #1A5CDB;
            background: rgba(50, 121, 249, 0.1);
            border-color: rgba(50, 121, 249, 0.22);
        }

        .developer-link .icon {
            font-size: 13px;
        }

        .hero-how-it-works {
            margin-top: 22px;
            padding: 18px 20px;
            border-radius: 22px;
            background: rgba(255, 255, 255, 0.78);
            border: 1px solid rgba(50, 121, 249, 0.10);
        }

        .hero-how-it-works-title {
            font-size: 14px;
            font-weight: 700;
            color: var(--stockify-text);
            margin-bottom: 12px;
        }

        .hero-how-it-works-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
        }

        .hero-how-step {
            padding: 14px;
            border-radius: 18px;
            background: white;
            border: 1px solid rgba(0, 0, 0, 0.06);
        }

        .hero-how-step b {
            display: block;
            font-size: 13px;
            margin-bottom: 4px;
            color: var(--stockify-blue-dark);
        }

        .hero-how-step p {
            margin: 0;
            font-size: 12px;
            line-height: 1.55;
            color: var(--stockify-subtle);
        }

        .landing-footer-space {
            height: 8px;
        }

        @media (max-width: 1100px) {
            .landing-content { padding-top: 0.5rem; }
            .hero-preview { margin-top: 12px; }
            .landing-canvas { margin: 0.8rem auto 1.5rem auto; }
        }

        @media (max-width: 768px) {
            .landing-nav {
                flex-direction: column;
                align-items: flex-start;
            }

            .landing-title {
                max-width: none;
            }

            .hero-preview-metrics,
            .hero-how-it-works-grid {
                grid-template-columns: 1fr;
            }

            .landing-main-hero {
                display: block;
            }

            .landing-steps {
                grid-template-columns: 1fr;
            }

            .developers-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .landing-top-links {
                gap: 12px;
                justify-content: flex-start;
                flex-wrap: wrap;
            }

            .landing-top-links .nav-link {
                min-width: 112px;
                height: 42px;
                font-size: 14px;
            }

            .st-key-landing_login_nav button {
                width: 135px !important;
                min-width: 135px !important;
                height: 42px !important;
                font-size: 14px !important;
            }
        }

        @media (max-width: 560px) {
            .developers-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def navigation():
    brand_col, links_col, action_col = st.columns([2.7, 2.6, 1.2])

    with brand_col:
        st.markdown(
            """
            <div class="landing-brand">
                <div class="landing-brand-badge">📦</div>
                <div class="landing-brand-copy">
                    <div class="landing-brand-title">Stockify</div>
                    <div class="landing-brand-subtitle">Smart Inventory Intelligence for Modern Retailers</div>
                </div>
            </div>
            <div style="margin-top:6px;">
                <span class="top-mini-dot"></span>
                <span class="top-mini-dot" style="opacity:0.7;"></span>
                <span class="top-mini-dot" style="opacity:0.5;"></span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with links_col:
        st.markdown(
            """
            <div class="landing-top-links">
                <a class="nav-link js-features-link" href="#features-section">Features</a>
                <a class="nav-link docs-link" href="https://docs.streamlit.io/" target="_blank" rel="noopener noreferrer">Docs</a>
                <a class="nav-link js-developers-link" href="#developers-section">Developers</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with action_col:
        if st.button("Login", key="landing_login_nav", use_container_width=True):
            st.session_state.auth_requested = True
            st.rerun()


def _request_auth():
    st.session_state.auth_requested = True
    st.rerun()


def _render_developers_section():
    developers = [
        {
            "name": "Himanchal Raghuvanshi",
            "email": "hcraghuvanshi2007@gmail.com",
            "linkedin": "https://www.linkedin.com/in/hcraghuvanshi",
        },
        {
            "name": "Ayesh Srivastava",
            "email": "ayeshsrivastava@gmail.com",
            "linkedin": "https://www.linkedin.com/in/ayesh-srivastava-780672390",
        },
        {
            "name": "Sameer Mishra",
            "email": "mrsameer12082006@gmail.com",
            "linkedin": "https://www.linkedin.com/in/sameer-mishra2006",
        },
        {
            "name": "Chirag Virdi",
            "email": "virdi.chirag07@gmail.com",
            "linkedin": "https://www.linkedin.com/in/chirag-virdi-a94623366",
        },
        {
            "name": "R. Srikar",
            "email": "srikarr16012008@gmail.com",
            "linkedin": "https://www.linkedin.com/in/srikar-rayaprolu-b64ba627b",
        },
        {
            "name": "Ayush Kumar",
            "email": "ayush.main.16@gmail.com",
            "linkedin": "https://www.linkedin.com/in/ayush-kumar-tech",
        },
    ]

    cards_html = []
    for dev in developers:
        initial = dev["name"].strip()[0].upper() if dev["name"].strip() else "D"
        card = f"""
        <div class="developer-card">
            <div>
                <div class="developer-top">
                    <div class="developer-avatar">{initial}</div>
                    <h4 class="developer-name">{dev['name']}</h4>
                </div>
                <div class="developer-links">
                    <a class="developer-link" href="mailto:{dev['email']}">
                        <span class="icon">✉️</span>
                        <span>{dev['email']}</span>
                    </a>
                    <a class="developer-link" href="{dev['linkedin']}" target="_blank" rel="noopener noreferrer">
                        <span class="icon">🔗</span>
                        <span>LinkedIn Profile</span>
                    </a>
                </div>
            </div>
        </div>
        """
        cards_html.append(card)

    st.markdown(
        f"""
        <div class="developers-section" id="developers-section">
            <h3 class="developers-heading">Developers</h3>
            <div class="developers-subheading">Built by Team Latent Space</div>
            <div class="developers-grid">
                {''.join(cards_html)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero_section():
    left, right = st.columns([1.02, 1.08], gap="large")

    with left:
        st.markdown(
            '<div class="landing-kicker">✨ Smart inventory intelligence for modern retailers</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="landing-title" style="max-width: 8.8ch; line-height:1.02;">
                Turn Sales Data into <span class="accent">Smart Inventory Decisions</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="landing-subtitle">
                Transform retail sales data into clear inventory insights.
                Identify fast-moving and slow-moving products.
                Make smarter stock decisions with simple visual analytics.
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Get Started", key="landing_get_started", use_container_width=True):
                _request_auth()
        with c2:
            if st.button("See How it Works", key="landing_how_it_works", use_container_width=True):
                st.session_state.demo_mode_requested = True
                st.rerun()

    with right:
        st.markdown(
            """
            <div class="hero-preview">
                <div class="hero-preview-top">
                    <div class="hero-preview-chip">📊 Live Decision Support</div>
                    <div class="hero-preview-chip" style="background: rgba(30, 142, 62, 0.08); color: #1E8E3E;">Healthy stock view</div>
                </div>
                <div class="hero-preview-card" style="margin-bottom: 10px;">
                    <div class="hero-preview-label">Fast Movers</div>
                    <div class="hero-preview-value">24 <span style="font-size:13px; color:#1E8E3E; font-weight:700;">✓</span></div>
                    <div class="hero-preview-note">Products with strong demand</div>
                </div>
                <div class="hero-preview-card" style="margin-bottom: 10px;">
                    <div class="hero-preview-label">Low Stock Alerts</div>
                    <div class="hero-preview-value" style="color:#D93025;">8</div>
                    <div class="hero-preview-note">Items need restocking.</div>
                </div>
                <div class="hero-preview-list">
                    <div class="hero-preview-item">
                        <div>
                            <strong>Demand Trends</strong><br>
                            <span>Visualize product demand trends.</span>
                        </div>
                        <div style="color:#3279F9; font-size:17px; font-weight:700;">↗</div>
                    </div>
                    <div class="hero-preview-item">
                        <div>
                            <strong>Reorder Guidance</strong><br>
                            <span>Smart suggestions for optimal stock.</span>
                        </div>
                        <div style="color:#3279F9; font-size:17px; font-weight:700;">🎯</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div id="features-section"></div>', unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown('<div class="hero-feature pill"><div class="hero-feature-icon">📤</div><div class="hero-feature-text">Drag &amp; Drop CSV Upload</div></div>', unsafe_allow_html=True)
    with f2:
        st.markdown('<div class="hero-feature pill"><div class="hero-feature-icon">⚡</div><div class="hero-feature-text">Real-Time Demand Analysis</div></div>', unsafe_allow_html=True)
    with f3:
        st.markdown('<div class="hero-feature pill"><div class="hero-feature-icon">🎯</div><div class="hero-feature-text">Actionable Smart Recommendations</div></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="landing-trusted">
            <h4>Trusted by modern retail teams</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "selected_industry" not in st.session_state:
        st.session_state.selected_industry = "Grocery Stores"

    ic1, ic2, ic3, ic4 = st.columns(4)
    with ic1:
        if st.button("Grocery Stores", key="chip_grocery_stores", use_container_width=True):
            st.session_state.selected_industry = "Grocery Stores"
            st.rerun()
    with ic2:
        if st.button("Pharmacy", key="chip_pharmacy", use_container_width=True):
            st.session_state.selected_industry = "Pharmacy"
            st.rerun()
    with ic3:
        if st.button("Electronics Shops", key="chip_electronics_shops", use_container_width=True):
            st.session_state.selected_industry = "Electronics Shops"
            st.rerun()
    with ic4:
        if st.button("Fashion Stores", key="chip_fashion_stores", use_container_width=True):
            st.session_state.selected_industry = "Fashion Stores"
            st.rerun()

    st.markdown(
        f'<div class="industry-selected-note">Viewing sample focus: <strong>{st.session_state.selected_industry}</strong></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="landing-steps">
            <div class="landing-step-card">
                <div class="num">Step 1</div>
                <div class="ttl">Upload your sales data</div>
                <div class="txt">Easily upload your files in CSV or Excel format.</div>
            </div>
            <div class="landing-step-card">
                <div class="num">Step 2</div>
                <div class="ttl">Analyze demand patterns</div>
                <div class="txt">Stockify identifies demand trends, fast and slow movers.</div>
            </div>
            <div class="landing-step-card">
                <div class="num">Step 3</div>
                <div class="ttl">Get smart recommendations</div>
                <div class="txt">Receive actionable suggestions for better stock planning.</div>
            </div>
            <div class="landing-step-card">
                <div class="num">Step 4</div>
                <div class="ttl">Optimize stock levels</div>
                <div class="txt">Keep inventory aligned with demand and reduce waste.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _render_developers_section()


def show_landing_page():
    styles()

    navigation()

    components.html(
        """
        <script>
        (function () {
            const doc = window.parent.document;

            function removeStrayClosingDivText() {
                const candidates = doc.querySelectorAll('p, div, span');
                candidates.forEach((node) => {
                    const txt = (node.textContent || '').trim();
                    if (txt === '</div>') {
                        // Remove only the stray text node (do NOT remove the whole container)
                        node.remove();
                    }
                });
            }

            removeStrayClosingDivText();

            const links = doc.querySelectorAll('a.js-features-link, a.js-developers-link');

            links.forEach((link) => {
                if (link.dataset.bound === '1') return;
                link.dataset.bound = '1';

                link.addEventListener('click', function (e) {
                    e.preventDefault();
                    const href = link.getAttribute('href') || '';
                    const targetId = href.startsWith('#') ? href.slice(1) : '';
                    if (!targetId) return;

                    const target = doc.getElementById(targetId);
                    if (!target) return;

                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });

                    if (targetId === 'features-section') {
                        const features = target.nextElementSibling;
                        if (features) {
                            features.classList.remove('features-focus');
                            requestAnimationFrame(() => features.classList.add('features-focus'));
                            setTimeout(() => features.classList.remove('features-focus'), 1100);
                        }
                    }

                    if (targetId === 'developers-section') {
                        const developers = target;
                        developers.classList.remove('developers-focus');
                        requestAnimationFrame(() => developers.classList.add('developers-focus'));
                        setTimeout(() => developers.classList.remove('developers-focus'), 1100);
                    }
                });
            });

            const mo = new MutationObserver(() => removeStrayClosingDivText());
            mo.observe(doc.body, { childList: true, subtree: true });
        })();
        </script>
        """,
        height=0,
    )

    st.markdown("<div style='height: 2px;'></div>", unsafe_allow_html=True)
    hero_section()
    st.markdown('<div class="landing-footer-space"></div>', unsafe_allow_html=True)

def show_home():
    # ===== HERO SECTION (Antigravity-style large heading) =====
    st.markdown("""
    <div style="text-align:center; margin-bottom:12px; animation: float 4s ease-in-out infinite;">
        <span style="
            font-size:64px;
            filter: drop-shadow(0 8px 32px rgba(50, 121, 249, 0.15));
        ">📦</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-title" style="font-size:68px; letter-spacing:-3px;">
        Smart Inventory Decisions<br>for Small Retailers
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-sub">
        Stop relying on guesswork. Harness the power of data to optimize stock levels,<br>
        maximize revenue, and eliminate waste.
    </div>
    """, unsafe_allow_html=True)

    # CTA Buttons (Antigravity pill-style)
    col1, col2, col3 = st.columns([1.2, 1.2, 1.2])
    with col2:
        st.markdown("""
        <style>
        div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton > button {
            background: #3279F9 !important;
            color: white !important;
            animation: pulse 3s ease-in-out infinite !important;
            font-size: 16px !important;
            padding: 16px 40px !important;
            border-radius: 9999px !important;
            font-weight: 600 !important;
            letter-spacing: 0.3px !important;
        }
        div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton > button:hover {
            background: #1A5CDB !important;
            box-shadow: 0 12px 40px rgba(50, 121, 249, 0.25) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        if st.button("🚀 Start Analyzing", use_container_width=True):
            st.session_state.current_page = "📂 Upload"
            st.rerun()

    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)

    # Home feature cards (same ones requested from auth area)
    hf1, hf2, hf3 = st.columns(3)
    with hf1:
        st.markdown(
            '<div class="hero-feature pill"><div class="hero-feature-icon">📤</div><div class="hero-feature-text">Drag &amp; Drop CSV Upload</div></div>',
            unsafe_allow_html=True,
        )
    with hf2:
        st.markdown(
            '<div class="hero-feature pill"><div class="hero-feature-icon">⚡</div><div class="hero-feature-text">Real-Time Demand Analysis</div></div>',
            unsafe_allow_html=True,
        )
    with hf3:
        st.markdown(
            '<div class="hero-feature pill"><div class="hero-feature-icon">🎯</div><div class="hero-feature-text">Actionable Smart Recommendations</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:44px'></div>", unsafe_allow_html=True)

    # ===== STATS BAR (Antigravity clean style) =====
    st.markdown("""
    <div style="
        display: flex;
        justify-content: center;
        gap: 48px;
        padding: 28px 32px;
        background: #F8F9FC;
        border-radius: 24px;
        border: 1px solid rgba(0, 0, 0, 0.06);
        animation: fadeInUp 0.7s cubic-bezier(.23, 1, .32, 1) 0.3s backwards;
        margin-bottom: 56px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    ">
        <div style="text-align:center;">
            <div style="font-size:32px; font-weight:700; color:#3279F9; letter-spacing:-1px;">10x</div>
            <div style="font-size:12px; color:#9AA0A6; text-transform:uppercase; letter-spacing:1.5px; font-weight:600; margin-top:4px;">Faster Insights</div>
        </div>
        <div style="width:1px; background:rgba(0,0,0,0.06);"></div>
        <div style="text-align:center;">
            <div style="font-size:32px; font-weight:700; color:#1E8E3E; letter-spacing:-1px;">30%</div>
            <div style="font-size:12px; color:#9AA0A6; text-transform:uppercase; letter-spacing:1.5px; font-weight:600; margin-top:4px;">Less Waste</div>
        </div>
        <div style="width:1px; background:rgba(0,0,0,0.06);"></div>
        <div style="text-align:center;">
            <div style="font-size:32px; font-weight:700; color:#7B61FF; letter-spacing:-1px;">2x</div>
            <div style="font-size:12px; color:#9AA0A6; text-transform:uppercase; letter-spacing:1.5px; font-weight:600; margin-top:4px;">Profit Growth</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ===== THE PROBLEM =====
    st.markdown('<div class="section-header">😰 The Problem</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    problems = [
        ("📦", "Overstocking", "Excess inventory ties up capital and increases waste, eating into your margins.", "rgba(217,48,37,0.06)", "rgba(217,48,37,0.12)"),
        ("🚫", "Stock Shortages", "Running out of key items means lost sales and frustrated customers who won't return.", "rgba(249,171,0,0.06)", "rgba(249,171,0,0.12)"),
        ("📉", "Reduced Profit", "Without data, pricing and ordering decisions consistently leave money on the table.", "rgba(50,121,249,0.06)", "rgba(50,121,249,0.12)"),
    ]

    for i, (col, (icon, title, desc, bg, border_bg)) in enumerate(zip([col1, col2, col3], problems)):
        with col:
            st.markdown(f"""
            <div class="glass-card delay-{i+1}" style="text-align:center; min-height:210px;">
                <div style="
                    font-size:44px; margin-bottom:16px;
                    width:72px; height:72px;
                    display:inline-flex; align-items:center; justify-content:center;
                    background:{bg}; border-radius:20px;
                    border: 1px solid {border_bg};
                ">{icon}</div>
                <div style="font-size:18px; font-weight:700; color:#121317; margin-bottom:10px;">{title}</div>
                <div style="font-size:14px; color:#5F6368; line-height:1.7;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)

    # ===== OUR SOLUTION =====
    st.markdown('<div class="section-header">✨ Our Solution</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    solutions = [
        ("📤", "Easy Upload", "Simply drag & drop your CSV files — inventory and sales data processed in seconds.", "rgba(50,121,249,0.06)", "rgba(50,121,249,0.12)"),
        ("⚡", "Instant Analysis", "Powerful analytics engine calculates KPIs, trends, and demand patterns automatically.", "rgba(123,97,255,0.06)", "rgba(123,97,255,0.12)"),
        ("🎯", "Visual Insights", "Beautiful charts and actionable recommendations to guide your next business move.", "rgba(30,142,62,0.06)", "rgba(30,142,62,0.12)"),
    ]

    for i, (col, (icon, title, desc, bg, border_bg)) in enumerate(zip([col1, col2, col3], solutions)):
        with col:
            st.markdown(f"""
            <div class="glass-card delay-{i+3}" style="text-align:center; min-height:210px;">
                <div style="
                    font-size:44px; margin-bottom:16px;
                    width:72px; height:72px;
                    display:inline-flex; align-items:center; justify-content:center;
                    background:{bg}; border-radius:20px;
                    border: 1px solid {border_bg};
                ">{icon}</div>
                <div style="font-size:18px; font-weight:700; color:#121317; margin-bottom:10px;">{title}</div>
                <div style="font-size:14px; color:#5F6368; line-height:1.7;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)

    # ===== HOW IT WORKS =====
    st.markdown('<div class="section-header">🔄 How It Works</div>', unsafe_allow_html=True)

    steps = [
        ("01", "Upload", "Upload your inventory & sales CSV files", "#3279F9"),
        ("02", "Process", "Auto-validate, clean, and transform data", "#7B61FF"),
        ("03", "Analyze", "KPIs, trends, and demand insights generated", "#1E8E3E"),
        ("04", "Optimize", "Act on data-driven recommendations", "#F9AB00"),
    ]

    cols = st.columns(4)
    for i, (col, (num, title, desc, color)) in enumerate(zip(cols, steps)):
        with col:
            st.markdown(f"""
            <div class="glass-card delay-{i+1}" style="text-align:center; min-height:180px;">
                <div style="
                    font-size:13px; font-weight:700; color: white;
                    margin-bottom:14px;
                    width:40px; height:40px;
                    display:inline-flex; align-items:center; justify-content:center;
                    background: {color}; border-radius: 9999px;
                    letter-spacing: 0.5px;
                ">{num}</div>
                <div style="font-size:17px; font-weight:700; color:#121317; margin-bottom:8px;">{title}</div>
                <div style="font-size:13px; color:#5F6368; line-height:1.65;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
