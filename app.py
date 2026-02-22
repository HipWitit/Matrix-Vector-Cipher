import streamlit as st
import re
import os
from st_copy_to_clipboard import st_copy_to_clipboard

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="Cyfer's Secret Love Language", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #E6E1F2 !important; }
    .stWidgetLabel p { display: none !important; }

    /* Input Boxes */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #FEE2E9 !important;
        color: #5B618A !important; 
        border: 2px solid #B4A7D6 !important;
    }

    /* Standard Buttons (KISS, TELL, DESTROY) */
    div.stButton > button {
        background-color: #B4A7D6 !important; 
        color: #FFD4E5 !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        height: 50px !important;
        border: none !important;
        width: 100% !important;
    }

    /* THE ULTIMATE FIX FOR THE COPY BUTTON */
    /* This targets the "Component Island" and forces the button inside to be purple */
    [data-testid="stCustomComponentV1"] button {
        background-color: #B4A7D6 !important;
        color: #FFD4E5 !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        height: 45px !important;
        border: none !important;
        width: 100% !important;
        box-shadow: none !important;
        cursor: pointer !important;
    }

    /* This removes the red border and white background frame */
    [data-testid="stCustomComponentV1"] iframe {
        border: none !important;
        background-color: transparent !important;
    }

    /* Keeps the button purple even when you hover over it */
    [data-testid="stCustomComponentV1"] button:hover {
        background-color: #A394C7 !important;
        color: #FFD4E5 !important;
        border: none !important;
    }
    
    /* Your Pink Result Box */
    .result-box {
        background-color: #FEE2E9; 
        color: #5B618A;
        padding: 15px;
        border-radius: 10px;
        font-family: monospace;
        margin-bottom: 10px;
        border: 2px solid #B4A7D6;
        word-wrap: break-word;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MATH ENGINE ---
char_to_coord = {
    'Q': (2, 25), 'W': (5, 25), 'E': (8, 25), 'R': (11, 25), 'T': (14, 25), 'Y': (17, 25), 'U': (20, 25), 'I': (23, 25), 'O': (26, 25), 'P': (29, 25),
    'A': (3, 20), 'S': (6, 20), 'D': (9, 20), 'F': (12, 20), 'G': (15, 20), 'H': (18, 20), 'J': (21, 20), 'K': (24, 20), 'L': (27, 20),
    'Z': (4, 15), 'X': (7, 15), 'C': (10, 15), 'V': (13, 15), 'B': (16, 15), 'N': (19, 15), 'M': (22, 15),
    '1': (2, 10), '2': (5, 10), '3': (8, 10), '4': (11, 10), '5': (14, 10), '6': (17, 10), '7': (20, 10), '8': (23, 10), '9': (26, 10), '0': (29, 10),
    '!': (5, 5),  ',': (10, 5), '.': (15, 5), ' ': (20, 5), '?': (25, 5)
}
coord_to_char = {v: k for k, v in char_to_coord.items()}
EMOJI_MAP = {'1': '🦄', '2': '🍼', '3': '🩷', '4': '🧸', '5': '🎀', '6': '🍓', '7': '🌈', '8': '🌸', '9': '💕', '0': '🫐', '-': '🍭'}
REVERSE_EMOJI_MAP = {v: k for k, v in EMOJI_MAP.items()}

def get_matrix_elements(key):
    seed = sum(ord(c) for c in key)
    return (seed % 7 + 2, seed % 5 + 1, seed % 3 + 1, seed % 11 + 2)

def modInverse(n, m=31):
    for x in range(1, m):
        if (((n % m) * (x % m)) % m == 1): return x
    return None

def clear_everything():
    st.session_state.lips = ""
    st.session_state.chem = ""

# --- 4. UI LAYOUT ---
if os.path.exists("CYPHER.png"): st.image("CYPHER.png", use_container_width=True)
if os.path.exists("Lock Lips.png"): st.image("Lock Lips.png", use_container_width=True)

kw = st.text_input("l1", type="password", label_visibility="collapsed", key="lips").upper().strip()

if os.path.exists("Kiss Chemistry.png"): st.image("Kiss Chemistry.png", use_container_width=True)
user_input = st.text_area("l2", height=120, label_visibility="collapsed", key="chem")

output_placeholder = st.empty()

kiss_btn = st.button("KISS", use_container_width=True)
tell_btn = st.button("TELL", use_container_width=True)
st.button

