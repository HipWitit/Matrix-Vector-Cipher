import streamlit as st
import re
import os

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="Cyfer's Secret Love Language", layout="centered")

st.markdown("""
    <style>
    /* Background */
    .stApp { background-color: #E6E1F2 !important; }
    
    /* Labels: Lavender #B4A7D6 and Bold */
    .stWidgetLabel p {
        color: #B4A7D6 !important; 
        font-weight: bold !important;
        font-size: 18px !important;
    }

    /* Input Boxes */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #FEE2E9 !important;
        color: #5B618A !important; 
        border: 2px solid #B4A7D6 !important;
    }

    /* Buttons: Lavender Background #B4A7D6 with Clear White Font */
    div.stButton > button {
        background-color: #B4A7D6 !important; 
        color: #FFD4E5 !important; /* pink text for perfect contrast */
        font-weight: bold !important;
        border-radius: 15px !important;
        height: 50px !important;
        border: none !important;
    }
    
    /* Hover state */
    div.stButton > button:hover {
        background-color: #9E8FC2 !important;
        color: white !important;
    }
    
    /* The Output Code Box */
    code {
        color: #B4A7D6 !important;
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

# --- 3. UI LAYOUT ---
if os.path.exists("CYPHER.png"):
    st.image("CYPHER.png", use_container_width=True)

kw = st.text_input("Lock Your Lips Here", type="password").upper().strip()
user_input = st.text_area("What's Your Kiss Chemistry?", height=120)

# Layout matching your recent screenshots
kiss_btn = st.button("KISS", use_container_width=True)
tell_btn = st.button("TELL", use_container_width=True)
destroy_btn = st.button("DESTROY CHEMISTRY", use_container_width=True)

# --- 4. PROCESSING LOGIC ---
if kw and (kiss_btn or tell_btn):
    a, b, c, d = get_matrix_elements(kw)
    det_inv = modInverse((a * d - b * c) % 31)
    
    if det_inv:
        if kiss_btn:
            points = []
            for char in user_input.upper():
                if char in char_to_coord:
                    x, y = char_to_coord[char]
                    nx, ny = (a*x + b*y) % 31, (c*x + d*y) % 31
                    points.append((nx, ny))
            if points:
                moves = [f"({points[i+1][0]-points[i][0]},{points[i+1][1]-points[i][1]})" for i in range(len(points)-1)]
                raw_res = f"{points[0][0]},{points[0][1]} | MOVES: {' '.join(moves)}"
                emoji_res = "".join(EMOJI_MAP.get(c, c) for c in raw_res)
                st.code(emoji_res) 

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
                # Results in Lavender
                st.markdown(f"### <span style='color:#B4A7D6'>Decoded: {''.join(decoded)}</span>", unsafe_allow_html=True)
            except:
                st.error("Chemistry Error!")

if destroy_btn:
    st.rerun()









