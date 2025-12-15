import streamlit as st
import random
import os

# --- 1. THEME/STYLES FUNCTION (Modified for Black Background and enforced dark theme) ---
def load_theme():
    """Applies custom CSS for black background, buttons, and heart animations, enforcing dark theme."""
    st.markdown("""
    <style>
    /* 1. GLOBAL BLACK BACKGROUND & TEXT COLOR ENFORCEMENT */
    .stApp {
        background-color: #000000; /* Solid Black */
        background: none; /* Ensure no underlying gradients interfere */
        color: white; /* Default text color set to white */
    }

    /* Target specific Streamlit containers to force dark background */
    .main .block-container {
        background-color: #000000; /* Main content area background */
        color: white;
    }
    
    /* Enforce dark colors for Streamlit's internal widgets and text boxes (e.g., sidebars, inputs) */
    div[data-testid="stSidebar"] {
        background-color: #111111; /* Dark sidebar, if present */
        color: white;
    }
    
    div[data-testid="stTextInput"] > div > input {
        background-color: #333333; /* Dark background for text input fields */
        color: white;
        border-color: #555555;
    }

    /* Ensure Streamlit Markdown and headers are white */
    h1, h2, h3, h4, h5, h6, .css-1d3z3gq { /* Targeting common text elements */
        color: white;
    }
    
    /* BIGGER BUTTONS - Base style */
    div.stButton > button {
        font-size: 26px;
        font-weight: bold;
        padding: 18px 55px;
        border-radius: 35px;
        transition: all 0.2s ease-in-out; /* Smooth transitions for size changes */
    }

    /* Center the button container */
    .stButton {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-top: 15px; /* Spacing between buttons */
    }

    /* Heart explosion */
    .explode-heart {
        position: fixed;
        width: 15px;
        height: 15px;
        background: red;
        transform: rotate(45deg);
        animation: explode 1s ease-out forwards;
    }

    .explode-heart::before,
    .explode-heart::after {
        content: "";
        width: 15px;
        height: 15px;
        background: red;
        border-radius: 50%;
        position: absolute;
    }

    .explode-heart::before {
        top: -7px;
        left: 0;
    }

    .explode-heart::after {
        left: -7px;
        top: 0;
    }

    @keyframes explode {
        0% {
            transform: scale(1) rotate(45deg);
            opacity: 1;
        }
        100% {
            transform: scale(2) translateY(-200px) rotate(45deg);
            opacity: 0;
        }
    }

    /* FLOATING HEARTS */
    .heart {
        position: fixed;
        width: 20px;
        height: 20px;
        background-color: #ff004f; /* Bright pink/red */
        transform: rotate(45deg);
        animation: float 8s infinite;
        opacity: 0.5;
        z-index: 0;
    }

    .heart:before,
    .heart:after {
        content: "";
        position: absolute;
        width: 20px;
        height: 20px;
        background-color: #ff004f;
        border-radius: 50%;
    }

    .heart:before {
        top: -10px;
        left: 0;
    }

    .heart:after {
        left: -10px;
        top: 0;
    }

    @keyframes float {
        0% { bottom: -10%; opacity: 0; }
        50% { opacity: 0.5; }
        100% { bottom: 110%; opacity: 0; }
    }
    
    /* Style for the "Dear Mohini" text */
    .apology-text {
        color: #ff9a9e; /* Light pink/salmon color for visibility on black */
        font-size: 18px; /* Small font size */
        text-align: center;
        margin-bottom: 50px;
    }
    
    /* Style for the main question */
    .love-question {
        color: white;
        text-align: center;
        font-size: 80px; /* Big size */
        font-weight: 900;
        margin-bottom: 50px;
    }
    
    /* Success message text color */
    .fade-bounce {
        color: #ff66aa !important; 
    }

    </style>

    <div class="heart" style="left:10%; animation-delay:0s;"></div>
    <div class="heart" style="left:30%; animation-delay:2s;"></div>
    <div class="heart" style="left:50%; animation-delay:4s;"></div>
    <div class="heart" style="left:70%; animation-delay:1s;"></div>
    <div class="heart" style="left:90%; animation-delay:3s;"></div>
    """, unsafe_allow_html=True)


# --- 2. MAIN UI FUNCTION ---
def show_question():
    """Renders the main Streamlit application logic with dynamic button sizing."""

    # Initialize session states
    if "loved" not in st.session_state:
        st.session_state.loved = False
    if "yes_size" not in st.session_state:
        # Base sizes for padding (px) - used for "No" button resizing
        st.session_state.yes_size = 55
    if "no_size" not in st.session_state:
        st.session_state.no_size = 55


    # --- DISPLAY APOLOGY & QUESTION ---
    
    # 2. "Dear Mohini..." (Small font)
    st.markdown(
        """
        <div class="apology-text">
            💌 Dear Mohini,<br>
            I just want to say sorry if I ever hurt you.<br>
            You mean the world to me and I promise to always be better for you. 💖
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 2. "Do you love me?" (Big size)
    st.markdown(
        """
        <h1 class="love-question">
            Do you love me? 💕
        </h1>
        """,
        unsafe_allow_html=True
    )

    # --- BUTTON LOGIC ---
    
    # Custom CSS for button sizing (dynamic based on session state)
    button_style_css = f"""
        <style>
        /* Apply dynamic size to YES button */
        div.stButton > button[key="yes"] {{
            padding-left: {st.session_state.yes_size}px;
            padding-right: {st.session_state.yes_size}px;
        }}
        /* Apply dynamic size to NO button */
        div.stButton > button[key="no"] {{
            padding-left: {st.session_state.no_size}px;
            padding-right: {st.session_state.no_size}px;
        }}
        </style>
    """
    st.markdown(button_style_css, unsafe_allow_html=True)
    
    # Columns for YES & NO buttons (side-by-side)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # YES BUTTON
    with col1:
        if st.button("❤️ YES ❤️", key="yes"):
            st.session_state.loved = True
            # Reset sizes upon success
            st.session_state.yes_size = 55
            st.session_state.no_size = 55
            st.rerun()

    # NO BUTTON
    with col3:
        if st.button("💔 NO 💔", key="no"):
            # If "No" is clicked, "No" gets smaller, "Yes" gets bigger
            st.session_state.no_size = max(15, st.session_state.no_size - 10) # Reduce padding, minimum 15px
            st.session_state.yes_size = st.session_state.yes_size + 15 # Increase padding
            st.rerun() # Rerun to apply new button sizes via the custom CSS

    # --- SUCCESS CONTENT (Hidden until "Yes" is clicked) ---
    if st.session_state.loved:

        # HEART EXPLOSION
        hearts = ""
        for _ in range(30):
            hearts += f"""
            <div class="explode-heart"
            style="
                left:{random.randint(40,60)}%;
                top:{random.randint(40,60)}%;
                animation-delay:{random.random()}s; /* Add random delay for better effect */
            "></div>
            """
        st.markdown(hearts, unsafe_allow_html=True)

        # SUCCESS MESSAGE
        st.markdown(
            """
            <h1 style="
                text-align:center;
                font-size:50px;
                font-weight:900;
                color:#ff004f;
                margin-top:40px;
            ">
                Yayyy! I knew it 😍💖
            </h1>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "<h3 style='text-align:center; color:white;'>Our Memories 💑</h3>",
            unsafe_allow_html=True
        )

        # IMAGE LIST (6 images)
        images = [
            "assets/us1.jpg",
            "assets/us2.jpg",
            "assets/us3.jpg",
            "assets/us4.jpg",
            "assets/us5.jpg",
            "assets/us6.jpg"
        ]

        # SHOW IMAGES IN GRID (2 per row)
        cols = st.columns(2)
        for idx, img in enumerate(images):
            # Check for file existence before attempting to load
            if os.path.exists(img):
                cols[idx % 2].image(
                    img,
                    use_container_width=True
                )
            else:
                 cols[idx % 2].info(f"Image not found: {img}")


        # FINAL LOVE TEXT
        st.markdown(
            """
            <style>
            @keyframes fadeBounce {
                0% {opacity: 0; transform: scale(0.8);}
                50% {opacity: 1; transform: scale(1.2);}
                100% {opacity: 1; transform: scale(1);}
            }
            .fade-bounce {
                animation: fadeBounce 1.5s ease-in-out forwards;
                text-align: center;
                font-size: 40px;
                font-weight: 900;
                color: #ff66aa;
                margin-top: 30px;
            }
            </style>
            <div class="fade-bounce">
                I LOVE YOU TOO 💕
            </div>
            """,
            unsafe_allow_html=True
        )


# --- 3. MAIN APP ENTRY POINT ---
if __name__ == "__main__":
    st.set_page_config(
        page_title="Love Question 💖",
        page_icon="💌",
        layout="centered"
    )

    # Load background & hearts
    load_theme()

    # Show main UI
    show_question()