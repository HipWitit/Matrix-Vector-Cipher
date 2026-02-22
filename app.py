import streamlit as st
import re
import os
import base64

# --- 1. CONFIG ---
st.set_page_config(page_title="Cyfer's Secret Love Language", layout="centered")

def get_img_as_base64(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

kiss_b64 = get_img_as_base64("Kiss.png")
tell_b64 = get_img_as_base64("Tell.png")

# --- 2. CSS FOR FULL-IMAGE BUTTONS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #E6E1F2 !important; }}
    
    /* This forces the KISS and TELL buttons to be invisible but fill the whole image area */
    div[data-testid="column"] button {{
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        background-color: transparent !important;
        color: transparent !important;
        border: none !important;
        z-index: 10 !important;
    }}

    .button-wrapper {{
        position: relative;
        width: 100%;
        height: auto;
        margin-bottom: 20px;
        display: flex;
        justify-content: center;
    }}
    
    .button-img {{
        width: 100%;
        border-radius: 15px;
        border: 4px solid #B4A7D6;
        pointer-events: none; /* Let the click pass through to the button */
    }}

    /* Keeps Copy/Destroy buttons looking like your Pydroid app */
    div[data-testid="stVerticalBlock"] > div > button {{
        background-color: #4B3F72 !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. MATH ENGINE ---
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

# --- 4. INTERFACE ---
if os.path.exists("CYPHER.png"):
    st.image("CYPHER.png", use_container_width=True)

kw = st.text_input("Lock Your Lips Here", type="password").upper().strip()
user_input = st.text_area("What's Your Kiss Chemistry?", height=120)

# SIDE-BY-SIDE IMAGE BUTTONS
col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="button-wrapper"><img src="data:image/png;base64,{kiss_b64}" class="button-img">', unsafe_allow_html=True)
    kiss_btn = st.button("K") # Label doesn't matter, it's invisible
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="button-wrapper"><img src="data:image/png;base64,{tell_b64}" class="button-img">', unsafe_allow_html=True)
    tell_btn = st.button("T")
    st.markdown('</div>', unsafe_allow_html=True)

# ACTION BUTTONS
if st.button("COPY SECRET CHEMISTRY", use_container_width=True):
    st.success("Selected! You can now copy the box below.")

if st.button("DESTROY CHEMISTRY", use_container_width=True):
    st.rerun()

# --- 5. PROCESSING ---
if kw and (kiss_btn or tell_btn):
    a, b, c, d = get_matrix_elements(kw)
    det_inv = modInverse((a * d - b * c) % 31)
    
    if det_inv:
        if kiss_btn:
            msg = user_input.upper()
            points = []
            for char in msg:
                if char in char_to_coord:
                    x, y = char_to_coord[char]
                    nx, ny = (a*x + b*y) % 31, (c*x + d*y) % 31
                    points.append((nx, ny))
            if points:
                moves = [f"({points[i+1][0]-points[i][0]},{points[i+1][1]-points[i][1]})" for i in range(len(points)-1)]
                raw_res = f"{points[0][0]},{points[0][1]} | MOVES: {' '.join(moves)}"
                emoji_res = "".join(EMOJI_MAP.get(c, c) for c in raw_res)
                st.code(emoji_res) # This box is scrollable for long stories
        
        if tell_btn:
            try:
                clean_msg = "".join(REVERSE_EMOJI_MAP.get(c, c) for c in user_input)
                inv_a, inv_b = (d * det_inv) % 31, (-b * det_inv) % 31
                inv_c, inv_d = (-c * det_inv) % 31, (a * det_inv) % 31
                header, moves_part = clean_msg.split("|")
                h_nums = re.findall(r"(-?\d+)", header)
                curr_x, curr_y = int(h_nums[0]), int(h_nums[1])
                ux, uy = (inv_a * curr_x + inv_b * curr_y) % 31, (inv_c * curr_x + inv_d * curr_y) % 31
                decoded = [coord_to_char.get((ux, uy), "?")]
                for dx, dy in re.findall(r"(-?\d+),(-?\d+)", moves_part):
                    curr_x, curr_y = curr_x + int(dx), curr_y + int(dy)
                    ux, uy = (inv_a * curr_x + inv_b * curr_y) % 31, (inv_c * curr_x + inv_d * curr_y) % 31
                    decoded.append(coord_to_char.get((ux, uy), "?"))
                st.markdown(f"### Decoded: {''.join(decoded)}")
            except:
                st.error("Chemistry Error!")




