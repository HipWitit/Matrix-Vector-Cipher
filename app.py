import streamlit as st
import re
import os
import streamlit.components.v1 as components

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="Cyfer's Secret Love Language", layout="centered")

# This block pulls the 'Cookie' font and restores the pink/purple theme
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cookie&display=swap" rel="stylesheet">
    <style>
    .stApp { background-color: #E6E1F2 !important; }
    
    /* HIDE LABELS */
    div[data-testid="stWidgetLabel"], label {
        display: none !important;
        height: 0px !important;
    }

    /* INPUT BOXES */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea,
    input::placeholder,
    textarea::placeholder {
        background-color: #FEE2E9 !important;
        color: #B4A7D6 !important; 
        border: 2px solid #B4A7D6 !important;
        font-family: "Courier New", Courier, monospace !important;
        font-size: 18px !important;
        font-weight: bold !important;
        -webkit-text-fill-color: #B4A7D6 !important;
    }

    /* --- COOKIE FONT ON BUTTONS --- */
    div.stButton > button p {
        font-family: 'Cookie', cursive !important;
        font-size: 52px !important; 
        font-weight: normal !important; 
        line-height: 1.0 !important;
        margin: 0 !important;
        padding: 5px 0 !important;
    }

    div.stButton > button {
        background-color: #B4A7D6 !important; 
        color: #FFD4E5 !important;
        border-radius: 20px !important;
        min-height: 90px !important; 
        height: auto !important;     
        border: none !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    .result-box {
        background-color: #FEE2E9; 
        color: #B4A7D6;
        padding: 15px;
        border-radius: 10px;
        font-family: "Courier New", Courier, monospace !important;
        margin-bottom: 10px;
        border: 2px solid #B4A7D6;
        word-wrap: break-word;
    }

    .whisper-text {
        color: #B4A7D6;
        font-family: "Courier New", Courier, monospace !important;
        font-weight: bold;
        font-size: 26px;
        margin-top: 15px;
        border-top: 2px dashed #B4A7D6;
        padding-top: 10px;
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
    st.session_state.hint = ""

# --- 3. UI LAYOUT ---
# Header images
if os.path.exists("CYPHER.png"): st.image("CYPHER.png", use_container_width=True)
if os.path.exists("Lock Lips.png"): st.image("Lock Lips.png", use_container_width=True)

kw = st.text_input("Key", type="password", key="lips", placeholder="SECRET KEY", label_visibility="collapsed").upper().strip()
hint_text = st.text_input("Hint", key="hint", placeholder="KEY HINT (Optional)", label_visibility="collapsed")

if os.path.exists("Kiss Chemistry.png"): st.image("Kiss Chemistry.png", use_container_width=True)
user_input = st.text_area("Message", height=120, key="chem", placeholder="YOUR MESSAGE", label_visibility="collapsed")

output_placeholder = st.empty()

col_main1, col_main2 = st.columns(2)
with col_main1:
    kiss_btn = st.button("Kiss", use_container_width=True)
with col_main2:
    tell_btn = st.button("Tell", use_container_width=True)

st.button("Destroy Chemistry", use_container_width=True, on_click=clear_everything)

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
                
                final_share_msg = f"{emoji_res}\\n\\nHint: {hint_text}" if hint_text else emoji_res
                
                with output_placeholder.container():
                    st.markdown(f'<div class="result-box">{emoji_res}</div>', unsafe_allow_html=True)
                    if hint_text: st.caption(f"Hint: {hint_text}")
                    
                    share_html = f"""
                        <link href="https://fonts.googleapis.com/css2?family=Cookie&display=swap" rel="stylesheet">
                        <button onclick="if(navigator.share){{navigator.share({{title:'Secret Language',text:`{final_share_msg}`}})}}else{{alert('Manual copy required');}}" 
                        style="background-color:#B4A7D6; color:#FFD4E5; border-radius:20px; min-height:90px; height:auto; border:none; width:100%; cursor:pointer; font-family: 'Cookie', cursive; font-size: 52px; padding: 10px;">Share Options ✨</button>
                    """
                    components.html(share_html, height=140)

        if tell_btn:
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
