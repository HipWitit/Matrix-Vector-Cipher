import streamlit as st
import re
from PIL import Image

# 1. Load your new art
img = Image.open("1771559101438.png")

# 2. Setup the page with your custom icon
st.set_page_config(page_title="Matrix Cipher", page_icon=img, layout="centered")

# 3. Put the art in the sidebar (replaces the abacus/header area)
st.sidebar.image(img, use_container_width=True)
st.sidebar.markdown("---")

st.markdown("""
    <style>
    /* 1. Main Background stays Lavender */
    .stApp {
        background-color: #D1D5F9 !important;
        color: #5B618A !important;
    }
    
    /* 2. THE FIX: Change black boxes to Pink */
    /* This targets the input areas for the Key and Message */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #FEE2E9 !important;
        color: #5B618A !important;
        border-radius: 10px !important;
        border: none !important;
    }

     /* 2. Clear Input Wrappers */
    div[data-baseweb="input"] {
        background-color: transparent !important;
        border: none !important;
    }

    /* 3. Global Mint & Periwinkle Fix */
    div[data-testid="stAlert"], 
    .stAlert, 
    div[role="alert"], 
    div[data-testid="stNotification"],
    div[data-testid="stMarkdownContainer"] .stAlert {
        background-color: #B2F2E3 !important;
        color: #5B618A !important;
        border: none !important;
        opacity: 1 !important;
    }
    
    /* Force Periwinkle on all internal text and icons */
    div[data-testid="stAlert"] p, 
    div[data-testid="stAlert"] div,
    div[data-testid="stAlert"] svg {
        color: #5B618A !important;
        fill: #5B618A !important;
    }
 




    .stTabs [data-baseweb="tab"] {
        background-color: #E2E4FF !important;
        border-radius: 10px 10px 0px 0px !important;
        color: #5B618A !important;
    }
    
    /* Buttons: Soft Purple */
    .stButton>button {
        background-color: #C3C9F9 !important;
        color: #5B618A !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)


# 1. YOUR MOD 31 FRIENDLY MAP
char_to_coord = {
    'Q': (2, 25), 'W': (5, 25), 'E': (8, 25), 'R': (11, 25), 'T': (14, 25), 'Y': (17, 25), 'U': (20, 25), 'I': (23, 25), 'O': (26, 25), 'P': (29, 25),
    'A': (3, 20), 'S': (6, 20), 'D': (9, 20), 'F': (12, 20), 'G': (15, 20), 'H': (18, 20), 'J': (21, 20), 'K': (24, 20), 'L': (27, 20),
    'Z': (4, 15), 'X': (7, 15), 'C': (10, 15), 'V': (13, 15), 'B': (16, 15), 'N': (19, 15), 'M': (22, 15),
    '1': (2, 10), '2': (5, 10), '3': (8, 10), '4': (11, 10), '5': (14, 10), '6': (17, 10), '7': (20, 10), '8': (23, 10), '9': (26, 10), '0': (29, 10),
    '!': (5, 5),  ',': (10, 5), '.': (15, 5), ' ': (20, 5), '?': (25, 5)
}
coord_to_char = {v: k for k, v in char_to_coord.items()}

# 2. THE MATRIX BRAIN
def get_matrix_elements(key):
    seed = sum(ord(c) for c in key)
    # These create the a, b, c, d values for the scramble
    return (seed % 7 + 2, seed % 5 + 1, seed % 3 + 1, seed % 11 + 2)

def modInverse(n, m=31):
    for x in range(1, m):
        if (((n % m) * (x % m)) % m == 1): return x
    return None

# 3. APP UI
st.image(img, width=250)
st.title("Cipher's Secret Love Language")

kw = st.text_input("Keys Please", type="password").upper().strip()

if kw:
    a, b, c, d = get_matrix_elements(kw)
    det = (a * d - b * c) % 31
    det_inv = modInverse(det)

    if det_inv is None:
        st.error("Key error: Matrix not invertible. Try another word!")
    else:
        st.success(f"Matrix Active: [[{a},{b}],[{c},{d}]]")
        
        tab1, tab2 = st.tabs(["Kiss""Tell"), 
        
        with tab1:
            msg = st.text_input("Message to Scramble:").upper()
            if msg:
                points = []
                for char in msg:
                    if char in char_to_coord:
                        x, y = char_to_coord[char]
                        # Transform: x' = (ax + by) % 31
                        nx, ny = (a*x + b*y) % 31, (c*x + d*y) % 31
                        points.append((nx, ny))
                
                if points:
                    st.subheader(f"Start: {points[0][0]},{points[0][1]}")
                    moves = [f"({points[i+1][0]-points[i][0]},{points[i+1][1]-points[i][1]})" for i in range(len(points)-1)]
                    st.code(f"{points[0][0]},{points[0][1]} | MOVES: {' '.join(moves)}")

        with tab2:
            st.info("Paste your coordinates here to reverse the matrix scramble.")
            # (Decoding logic goes here similar to your first app)

        with tab2:
            st.header("Reverse the Matrix")
            col1, col2 = st.columns(2)
            with col1:
                start_in = st.text_input("Start Point (x,y):", key="decode_start")
            with col2:
                vector_in = st.text_area("Vectors (e.g. (5,-7)):", key="decode_vectors")

            if st.button("Make Her Meow"):
                try:
                    # 1. Calculate the Inverse Matrix (The Reverse Gear)
                    # Math: 1/det * [[d, -b], [-c, a]]
                    inv_a = (d * det_inv) % 31
                    inv_b = (-b * det_inv) % 31
                    inv_c = (-c * det_inv) % 31
                    inv_d = (a * det_inv) % 31
                    
                    # 2. Parse the start point
                    sx, sy = map(int, start_in.split(','))
                    curr = (sx, sy)
                    
                    # 3. Create a mini-function to unscramble points
                    def untransform(tx, ty):
                        ux = (inv_a * tx + inv_b * ty) % 31
                        uy = (inv_c * tx + inv_d * ty) % 31
                        return ux, uy

                    # 4. Decode the first letter
                    ux, uy = untransform(sx, sy)
                    decoded = [coord_to_char.get((ux, uy), "?")]
                    
                    # 5. Extract and apply all moves
                    moves = re.findall(r"(-?\d+),(-?\d+)", vector_in)
                    for dx, dy in moves:
                        curr = (curr[0] + int(dx), curr[1] + int(dy))
                        ux, uy = untransform(curr[0], curr[1])
                        decoded.append(coord_to_char.get((ux, uy), "?"))
                    
                    st.success(f"Decoded Message: {''.join(decoded)}")
                except Exception as e:
                    st.error("Error: Check your start point and vector format!")
