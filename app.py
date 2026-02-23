import streamlit as st
import re
import os
import streamlit.components.v1 as components

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="Cyfer's Secret Love Language", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #E6E1F2 !important; }
    div[data-testid="stWidgetLabel"], label { display: none !important; }

    /* INPUT BOX CUSTOMIZATION */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea,
    input::placeholder, textarea::placeholder {
        background-color: #FEE2E9 !important;
        color: #B4A7D6 !important; 
        border: 2px solid #B4A7D6 !important;
        font-family: "Courier New", Courier, monospace !important;
        font-size: 22px !important;
        font-weight: bold !important;
    }

    /* ENCODED BOX */
    .result-box {
        background-color: #FEE2E9; 
        color: #B4A7D6;
        padding: 20px;
        border-radius: 10px;
        font-family: "Courier New", Courier, monospace !important;
        border: 3px solid #B4A7D6;
        word-wrap: break-word;
        margin-top: 15px;
        font-weight: bold;
        font-size: 20px;
    }

    /* DECODED WHISPER STYLE */
    .whisper-text {
        color: #B4A7D6;
        font-family: "Courier New", Courier, monospace !important;
        font-weight: bold;
        font-size: 32px;
        margin-top: 20px;
        border-top: 3px dashed #B4A7D6;
        padding-top: 15px;
    }
    
    /* STYLING FOR THE GIGANTIC DESTROY BUTTON */
    .stButton > button {
        background-color: #B4A7D6 !important;
        color: #FFD4E5 !important;
        font-size: 50px !important;
        font-weight: 900 !important;
        min-height: 100px !important;
        border-radius: 20px !important;
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
if os.path.exists("CYPHER.png"): st.image("CYPHER.png", width="stretch")
if os.path.exists("Lock Lips.png"): st.image("Lock Lips.png", width="stretch")

kw = st.text_input("Key", type="password", key="lips", placeholder="SECRET KEY").upper().strip()
hint_text = st.text_input("Hint", key="hint", placeholder="KEY HINT (Optional)")

if os.path.exists("Kiss Chemistry.png"): st.image("Kiss Chemistry.png", width="stretch")
user_input = st.text_area("Message", height=120, key="chem", placeholder="YOUR MESSAGE")

# Custom Button Logic via Query Params
params = st.query_params
kiss_clicked = params.get("action") == "kiss"
tell_clicked = params.get("action") == "tell"

# Injecting the Custom HTML Buttons for massive font control
button_html = f"""
    <div style="display: flex; gap: 10px;">
        <a href="/?action=kiss" target="_self" style="flex: 1; text-decoration: none;">
            <button style="width: 100%; background-color: #B4A7D6; color: #FFD4E5; border: none; border-radius: 20px; height: 120px; font-size: 70px; font-weight: 900; cursor: pointer; font-family: sans-serif;">KISS</button>
        </a>
        <a href="/?action=tell" target="_self" style="flex: 1; text-decoration: none;">
            <button style="width: 100%; background-color: #B4A7D6; color: #FFD4E5; border: none; border-radius: 20px; height: 120px; font-size: 70px; font-weight: 900; cursor: pointer; font-family: sans-serif;">TELL</button>
        </a>
    </div>
"""
components.html(button_html, height=140)

if st.button("DESTROY CHEMISTRY", width="stretch"):
    st.query_params.clear()
    st.rerun()

output_placeholder = st.empty()

# --- 4. PROCESSING LOGIC ---
if kw and (kiss_clicked or tell_clicked):
    a, b, c, d = get_matrix_elements(kw)
    det_inv = modInverse((a * d - b * c) % 31)
    
    if det_inv:
        if kiss_clicked:
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
                final_share_msg = f"{emoji_res}\\n\\nHint: {hint_text}" if hint_text else emoji_res
                
                with output_placeholder.container():
                    st.markdown(f'<div class="result-box">{emoji_res}</div>', unsafe_allow_html=True)
                    share_html = f"""<button onclick="navigator.share({{title:'Secret Language',text:`{final_share_msg}`}})" style="background-color:#B4A7D6; color:#FFD4E5; font-weight:900; border-radius:25px; min-height:80px; width:100%; cursor:pointer; font-size: 30px; text-transform: uppercase; border:none;">SHARE OPTIONS ✨</button>"""
                    components.html(share_html, height=100)

        if tell_clicked:
            try:
                clean_input = user_input.split("Hint:")[0].strip()
                clean_msg = "".join(REVERSE_EMOJI_MAP.get(c, c) for c in clean_input)
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
                
                output_placeholder.markdown(f'<div class="whisper-text">Cypher Whispers: {"".join(decoded)}</div>', unsafe_allow_html=True)
            except:
                st.error("Chemistry Error!")
