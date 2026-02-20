import streamlit as st
import re

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
st.title("🧮 Matrix Vector Cipher")
kw = st.text_input("Enter Secret Key", type="password").upper().strip()

if kw:
    a, b, c, d = get_matrix_elements(kw)
    det = (a * d - b * c) % 31
    det_inv = modInverse(det)

    if det_inv is None:
        st.error("Key error: Matrix not invertible. Try another word!")
    else:
        st.success(f"Matrix Active: [[{a},{b}],[{c},{d}]]")
        
        tab1, tab2 = st.tabs(["Encode", "Decode"])
        
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

