"""Visual styling for the FirstAid AI Streamlit interface."""

import streamlit as st


def apply_styles() -> None:
    """Apply the dark, calm FirstAid AI visual theme."""
    st.markdown(
        """
        <style>
        :root {
            color-scheme: dark;
        }

        .stApp {
            background:
                radial-gradient(ellipse at 50% -18%, rgba(39, 194, 157, 0.13), transparent 48%),
                #0b1110;
            color: #e8f0ed;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stToolbar"] {
            right: 1rem;
        }

        .block-container {
            max-width: 780px;
            padding-top: 2.2rem;
            padding-bottom: 2.5rem;
        }

        h1, h2, h3 {
            color: #f1f7f4 !important;
            letter-spacing: -0.045em !important;
        }

        h1 {
            font-size: clamp(2.1rem, 5vw, 3.15rem) !important;
            line-height: 1.08 !important;
            font-weight: 750 !important;
        }

        p, li, label {
            color: #d5e1dc;
        }

        [data-testid="stCaptionContainer"] p {
            color: #91a49c !important;
            font-size: 0.86rem;
        }

        .fa-brand-row {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            margin: 0.2rem 0 2.6rem;
        }

        .fa-mark {
            width: 2.25rem;
            height: 2.25rem;
            display: grid;
            place-items: center;
            border-radius: 0.8rem;
            color: #06251d;
            background: linear-gradient(145deg, #67e8c1, #25b98e);
            font-size: 1.1rem;
            font-weight: 900;
            box-shadow: 0 7px 24px rgba(37, 185, 142, 0.18);
        }

        .fa-brand-name {
            color: #edf7f2;
            font-size: 0.98rem;
            font-weight: 750;
            letter-spacing: -0.025em;
        }

        .fa-brand-subtitle {
            color: #81968d;
            font-size: 0.7rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .fa-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.38rem 0.7rem;
            border: 1px solid rgba(103, 232, 193, 0.2);
            border-radius: 999px;
            background: rgba(37, 185, 142, 0.08);
            color: #83e8c6;
            font-size: 0.72rem;
            font-weight: 650;
            letter-spacing: 0.055em;
            text-transform: uppercase;
        }

        .fa-eyebrow-dot {
            width: 0.42rem;
            height: 0.42rem;
            border-radius: 50%;
            background: #55d9ad;
            box-shadow: 0 0 0 4px rgba(85, 217, 173, 0.1);
        }

        .fa-intro {
            margin: 1.1rem 0 0.55rem;
            color: #9aada5;
            font-size: 1.02rem;
            line-height: 1.65;
            max-width: 39rem;
        }

        .fa-safety-note {
            display: flex;
            align-items: flex-start;
            gap: 0.65rem;
            margin: 1.3rem 0 1.5rem;
            padding: 0.8rem 0.95rem;
            border: 1px solid rgba(248, 180, 91, 0.2);
            border-radius: 0.9rem;
            background: rgba(248, 180, 91, 0.055);
            color: #d7c4a5;
            font-size: 0.82rem;
            line-height: 1.5;
        }

        .fa-safety-note strong {
            color: #f3ca8e;
        }

        [data-testid="stChatMessage"] {
            border: 1px solid rgba(164, 190, 179, 0.09);
            border-radius: 1.15rem;
            padding: 1rem 1.05rem;
            background: rgba(19, 30, 27, 0.82);
            margin-bottom: 0.8rem;
        }

        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {
            line-height: 1.65;
        }

        [data-testid="stChatMessage"] [data-testid="stChatMessageAvatarUser"] {
            background: #1b3b32;
        }

        [data-testid="stChatMessage"] [data-testid="stChatMessageAvatarAssistant"] {
            background: #174b3d;
        }

        [data-testid="stChatInput"] {
            border: 1px solid rgba(103, 232, 193, 0.22);
            border-radius: 1.05rem;
            background: #111b18;
            box-shadow: 0 12px 36px rgba(0, 0, 0, 0.18);
        }

        [data-testid="stChatInput"]:focus-within {
            border-color: rgba(103, 232, 193, 0.62);
            box-shadow: 0 0 0 3px rgba(37, 185, 142, 0.1);
        }

        [data-testid="stChatInput"] textarea {
            color: #edf7f2 !important;
        }

        [data-testid="stChatInput"] textarea::placeholder {
            color: #789087 !important;
        }

        .stButton > button {
            border: 1px solid rgba(103, 232, 193, 0.28);
            border-radius: 0.85rem;
            background: #174b3d;
            color: #effcf6;
            font-weight: 650;
            transition: background 140ms ease, border-color 140ms ease, transform 140ms ease;
        }

        .stButton > button:hover {
            border-color: #67e8c1;
            background: #1d624e;
            color: #ffffff;
            transform: translateY(-1px);
        }

        [data-testid="stAlert"] {
            border-radius: 0.95rem;
        }

        hr {
            border-color: rgba(164, 190, 179, 0.12) !important;
            margin-top: 2rem !important;
            margin-bottom: 1rem !important;
        }

        footer {
            visibility: hidden;
        }

        @media (max-width: 640px) {
            .block-container {
                padding-top: 1.3rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .fa-brand-row {
                margin-bottom: 2rem;
            }

            [data-testid="stChatMessage"] {
                padding: 0.85rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
