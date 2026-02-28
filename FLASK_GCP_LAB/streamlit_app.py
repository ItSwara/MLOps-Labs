import streamlit as st
import requests
import time

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Penguin Species Classifier",
    page_icon="🐧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ANTARCTIC THEME CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    /* Background */
    .stApp {
        background: linear-gradient(160deg, #0a1628 0%, #0d2b45 40%, #1a4a6b 70%, #2d6a8a 100%);
        color: #e0f4ff;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #071020 0%, #0d2035 100%);
        border-right: 1px solid #1e4a6b;
    }

    /* Title */
    h1 {
        font-family: 'Orbitron', sans-serif !important;
        color: #a8e6ff !important;
        text-shadow: 0 0 20px rgba(100, 200, 255, 0.5);
        letter-spacing: 2px;
    }

    h2, h3 {
        font-family: 'Inter', sans-serif !important;
        color: #7dd3f0 !important;
    }

    /* Sliders */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #1e6fa0, #4db8e8) !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background-color: #0d2b45 !important;
        border: 1px solid #2d6a8a !important;
        color: #e0f4ff !important;
        border-radius: 8px !important;
    }

    /* Predict Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #1a6fa0 0%, #0d3d5c 100%);
        color: #a8e6ff;
        border: 1px solid #4db8e8;
        border-radius: 12px;
        height: 55px;
        font-family: 'Orbitron', sans-serif;
        font-size: 16px;
        letter-spacing: 2px;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px rgba(77, 184, 232, 0.3);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2485bf 0%, #1a5c85 100%);
        box-shadow: 0 0 25px rgba(77, 184, 232, 0.6);
        transform: translateY(-2px);
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: rgba(13, 43, 69, 0.7);
        border: 1px solid #2d6a8a;
        border-radius: 12px;
        padding: 15px;
        backdrop-filter: blur(10px);
    }

    /* Divider */
    hr {
        border-color: #1e4a6b !important;
    }

    /* Result card */
    .result-card {
        background: rgba(10, 30, 60, 0.8);
        border: 1px solid #4db8e8;
        border-radius: 16px;
        padding: 25px;
        backdrop-filter: blur(15px);
        box-shadow: 0 0 30px rgba(77, 184, 232, 0.2);
    }

    /* Snowflakes */
    .snowflakes {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    .snowflake {
        position: absolute;
        top: -20px;
        color: #a8e6ff;
        font-size: 1em;
        animation: fall linear infinite;
        opacity: 0.6;
    }
    @keyframes fall {
        to { transform: translateY(100vh) rotate(360deg); opacity: 0; }
    }

    /* Walking penguin */
    .penguin-walk {
        font-size: 2.5em;
        display: inline-block;
        animation: waddle 0.5s ease-in-out infinite alternate, walk 3s linear forwards;
    }
    @keyframes waddle {
        from { transform: rotate(-10deg); }
        to   { transform: rotate(10deg); }
    }
    @keyframes walk {
        from { margin-left: 0%; }
        to   { margin-left: 85%; }
    }

    p, label, .stMarkdown {
        color: #c8e8f8 !important;
        font-family: 'Inter', sans-serif !important;
    }
    </style>

    <!-- Snowflakes -->
    <div class="snowflakes">
        <div class="snowflake" style="left:5%;animation-duration:8s;animation-delay:0s;">❄</div>
        <div class="snowflake" style="left:15%;animation-duration:12s;animation-delay:2s;">❅</div>
        <div class="snowflake" style="left:25%;animation-duration:9s;animation-delay:4s;">❆</div>
        <div class="snowflake" style="left:40%;animation-duration:11s;animation-delay:1s;">❄</div>
        <div class="snowflake" style="left:55%;animation-duration:7s;animation-delay:3s;">❅</div>
        <div class="snowflake" style="left:70%;animation-duration:13s;animation-delay:5s;">❆</div>
        <div class="snowflake" style="left:80%;animation-duration:10s;animation-delay:2s;">❄</div>
        <div class="snowflake" style="left:90%;animation-duration:8s;animation-delay:6s;">❅</div>
    </div>
""", unsafe_allow_html=True)

# 3. SIDEBAR
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1598439210625-5067c578f3f6?w=400", caption="Chinstrap Penguin")
    st.markdown("## 🐧 About")
    st.markdown("""
    Identify Palmer Archipelago penguin species from physical measurements using an SVM classifier trained on real Antarctic field data.

    **Species:**
    - 🟠 Adelie
    - 🔵 Chinstrap  
    - 🟢 Gentoo
    """)
    st.write("---")
    st.caption("🧊 Palmer Archipelago · Antarctica")

# 4. HEADER
st.title("🐧 Antarctic Penguin Classifier")
st.markdown("*Enter penguin measurements to identify the species*")
st.write("---")

# 5. INPUTS
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📏 Bill")
    bill_length = st.slider('Bill Length (mm)', 30.0, 60.0, 39.1)
    bill_depth  = st.slider('Bill Depth (mm)',  10.0, 25.0, 18.7)

with col2:
    st.markdown("### 🦭 Body")
    flipper_length = st.slider('Flipper Length (mm)', 170.0, 235.0, 181.0)
    body_mass      = st.slider('Body Mass (g)', 2700.0, 6300.0, 3750.0)

with col3:
    st.markdown("### 🗺️ Location & Sex")
    island = st.selectbox('Island', ['Torgersen', 'Biscoe', 'Dream'])
    sex    = st.selectbox('Sex', ['Male', 'Female'])

st.write("---")

# 6. EFFECT SELECTOR + PREDICT BUTTON
if st.button('🔍  IDENTIFY SPECIES'):

    # ── Animation effects ──────────────────────────────────────────────────────
    fx = st.empty()
    for count in ["3", "2", "1", "🐧"]:
        fx.markdown(f"""
            <p style="text-align:center;font-size:5em;font-family:'Orbitron',sans-serif;
            color:#4db8e8;text-shadow:0 0 30px #4db8e8;
            animation:pop 0.4s ease-out;">
                {count}
            </p>
            <style>
            @keyframes pop {{
                from {{ transform:scale(0.3); opacity:0; }}
                to   {{ transform:scale(1);   opacity:1; }}
            }}
            </style>
        """, unsafe_allow_html=True)
        time.sleep(0.8)
    fx.empty()

    data = {
        'bill_length_mm':    bill_length,
        'bill_depth_mm':     bill_depth,
        'flipper_length_mm': flipper_length,
        'body_mass_g':       body_mass,
        'island':            island,
        'sex':               sex
    }

    try:
        response = requests.post('https://penguin-app-554004998721.us-central1.run.app/predict', json=data)

        if response.status_code == 200:
            result     = response.json()
            prediction = result['prediction']
            confidence = result['confidence']

            images = {
                "Adelie":    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Hope_Bay-2016-Trinity_Peninsula%E2%80%93Ad%C3%A9lie_penguin_%28Pygoscelis_adeliae%29_04.jpg/640px-Hope_Bay-2016-Trinity_Peninsula%E2%80%93Ad%C3%A9lie_penguin_%28Pygoscelis_adeliae%29_04.jpg",
                "Chinstrap": "https://images.unsplash.com/photo-1598439210625-5067c578f3f6?w=400",
                "Gentoo":    "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Brown_Bluff-2016-Tabarin_Peninsula%E2%80%93Gentoo_penguin_%28Pygoscelis_papua%29_03.jpg/640px-Brown_Bluff-2016-Tabarin_Peninsula%E2%80%93Gentoo_penguin_%28Pygoscelis_papua%29_03.jpg"
            }

            species_color = {"Adelie": "#ff8c42", "Chinstrap": "#4db8e8", "Gentoo": "#56d98e"}
            color = species_color.get(prediction, "#a8e6ff")

            st.markdown(f"""
                <div class="result-card">
                    <h2 style="color:{color}; font-family:'Orbitron',sans-serif; text-align:center;">
                        ✦ {prediction} Penguin ✦
                    </h2>
                    <p style="text-align:center; font-size:1.1em; color:#a8e6ff;">
                        Confidence: <strong style="color:{color};">{confidence}%</strong>
                    </p>
                </div>
            """, unsafe_allow_html=True)

            st.write("")
            res_col1, res_col2 = st.columns([1, 2])

            with res_col1:
                st.image(images.get(prediction, images["Adelie"]), width=280)

            with res_col2:
                st.markdown(f"### Measurements")
                st.metric("Bill Length", f"{bill_length} mm")
                st.metric("Bill Depth",  f"{bill_depth} mm")
                st.metric("Flipper",     f"{flipper_length} mm")
                st.metric("Body Mass",   f"{body_mass} g")
                st.markdown(f"**Island:** {island} &nbsp;|&nbsp; **Sex:** {sex}")

        else:
            st.error(f'Server Error: {response.status_code}')

    except requests.exceptions.RequestException:
        st.error('❌ Connection Error: Make sure main.py is running on port 8080.')