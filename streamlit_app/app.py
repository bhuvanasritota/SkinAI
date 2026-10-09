import time
import requests
import streamlit as st
from textwrap import dedent


# ============================================================
# CONFIG
# ============================================================

API_URL = "http://127.0.0.1:8000"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SkinAI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "page": "home",
    "token": None,
    "user": None,
    "profile": None,
    "favorites": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL
       ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 5%,
                rgba(244, 114, 182, 0.12),
                transparent 25%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(167, 139, 250, 0.12),
                transparent 25%
            ),
            #fffafd;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* ======================================================
       TEXT
       ====================================================== */

    .brand {
        font-size: 30px;
        font-weight: 850;
        letter-spacing: -1.5px;
        color: #19151d;
    }

    .brand span {
        color: #e85d9e;
    }

    .eyebrow {
        display: inline-block;
        padding: 7px 15px;
        border-radius: 999px;
        background: #fce7f3;
        color: #be185d;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 18px;
    }

    .hero-title {
        font-size: 64px;
        line-height: 1.02;
        font-weight: 850;
        letter-spacing: -3px;
        color: #17131a;
        margin-bottom: 20px;
    }

    .hero-gradient {
        background: linear-gradient(
            90deg,
            #e85d9e,
            #a855f7
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 19px;
        line-height: 1.7;
        color: #756d79;
        max-width: 690px;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 36px;
        font-weight: 800;
        letter-spacing: -1.5px;
        color: #1c1720;
        margin-top: 50px;
        margin-bottom: 8px;
    }

    .section-subtitle {
        color: #756d79;
        font-size: 16px;
        margin-bottom: 25px;
    }

    /* ======================================================
       HERO
       ====================================================== */

    .hero-wrapper {
        padding: 75px 10px 65px 10px;
    }

    .hero-visual {
        min-height: 430px;
        border-radius: 32px;
        background:
            radial-gradient(
                circle at 25% 25%,
                rgba(255,255,255,0.9),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #fce7f3,
                #ede9fe
            );
        border: 1px solid rgba(255,255,255,0.8);
        box-shadow:
            0 30px 80px rgba(160, 100, 150, 0.13);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
    }

    .orb {
        width: 250px;
        height: 250px;
        border-radius: 50%;
        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.9),
                rgba(255,255,255,0.25)
            );
        box-shadow:
            0 25px 60px rgba(168, 85, 247, 0.18);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 95px;
    }

    .floating-card {
        position: absolute;
        background: rgba(255,255,255,0.86);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.9);
        border-radius: 18px;
        padding: 13px 17px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.08);
        font-size: 13px;
        font-weight: 700;
    }

    .floating-one {
        top: 35px;
        left: 30px;
    }

    .floating-two {
        bottom: 45px;
        right: 25px;
    }

    .floating-three {
        bottom: 75px;
        left: 25px;
    }

    /* ======================================================
       FEATURE CARDS
       ====================================================== */

    .feature-card {
        background: rgba(255,255,255,0.82);
        border: 1px solid #f0e9f0;
        border-radius: 24px;
        padding: 27px;
        min-height: 205px;
        box-shadow: 0 12px 35px rgba(35, 20, 40, 0.045);
    }

    .feature-icon {
        font-size: 30px;
        margin-bottom: 18px;
    }

    .feature-title {
        font-size: 20px;
        font-weight: 750;
        color: #211a25;
        margin-bottom: 9px;
    }

    .feature-text {
        color: #776f7b;
        line-height: 1.65;
        font-size: 14px;
    }

    /* ======================================================
       AI SECTION
       ====================================================== */

    .ai-box {
        margin-top: 45px;
        padding: 40px;
        border-radius: 30px;
        background:
            linear-gradient(
                135deg,
                #19151d,
                #29202f
            );
        color: white;
        box-shadow: 0 25px 70px rgba(30, 20, 40, 0.16);
    }

    .ai-title {
        font-size: 36px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .ai-text {
        color: #cfc6d5;
        line-height: 1.7;
    }

    .ai-pill {
        display: inline-block;
        margin: 5px;
        padding: 8px 13px;
        border-radius: 999px;
        background: rgba(255,255,255,0.08);
        color: #f9edf5;
        font-size: 13px;
    }

    /* ======================================================
       AUTH
       ====================================================== */

    .auth-wrapper {
        max-width: 510px;
        margin: 55px auto;
    }

    .auth-header {
        text-align: center;
        margin-bottom: 28px;
    }

    .auth-title {
        font-size: 38px;
        font-weight: 820;
        letter-spacing: -1.5px;
        color: #1b161e;
    }

    .auth-subtitle {
        color: #766e79;
        line-height: 1.6;
    }

    /* ======================================================
       DASHBOARD
       ====================================================== */

    .welcome-title {
        font-size: 42px;
        font-weight: 820;
        letter-spacing: -2px;
        color: #1b161e;
    }

    .stat-card {
        background: white;
        border: 1px solid #f0e9f0;
        border-radius: 22px;
        padding: 22px;
        box-shadow: 0 10px 30px rgba(30, 20, 40, 0.04);
    }

    .stat-label {
        color: #837a87;
        font-size: 13px;
        font-weight: 600;
    }

    .stat-value {
        color: #211a25;
        font-size: 25px;
        font-weight: 800;
        margin-top: 6px;
    }

    .profile-card {
    background: linear-gradient(
        135deg,
        #ffffff,
        #fff5fa
    );
    border: 1px solid #f1e3ed;
    border-radius: 26px;
    padding: 30px;
    box-shadow: 0 15px 45px rgba(50, 20, 50, 0.05);
    color: #211a25;
}

.profile-card h2 {
    color: #211a25 !important;
}

.profile-card p {
    color: #6d6471 !important;
}

    /* ======================================================
       ASSESSMENT
       ====================================================== */

    .assessment-header {
        text-align: center;
        padding: 35px 0;
    }

    .step-label {
        color: #d63384;
        font-size: 13px;
        font-weight: 750;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .assessment-title {
        font-size: 40px;
        font-weight: 820;
        letter-spacing: -1.5px;
        color: #1b161e;
    }

    /* ======================================================
       RECOMMENDATIONS
       ====================================================== */

    .result-card {
        background: white;
        border: 1px solid #eee6ef;
        border-radius: 24px;
        padding: 26px;
        margin-bottom: 18px;
        box-shadow: 0 12px 35px rgba(35, 20, 40, 0.045);
    }

    .match-badge {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        background: #ecfdf3;
        color: #15803d;
        font-size: 12px;
        font-weight: 800;
    }

    .product-name {
        font-size: 24px;
        font-weight: 800;
        color: #211a25;
        margin-top: 12px;
    }

    .reason {
        color: #625967;
        font-size: 14px;
        padding: 4px 0;
    }

    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {
        border-radius: 14px;
        border: 1px solid #eadde8;
        min-height: 45px;
        font-weight: 700;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        border-color: #e85d9e;
        box-shadow: 0 8px 20px rgba(232,93,158,0.12);
    }

    /* ======================================================
       INPUTS
       ====================================================== */

    .stTextInput input,
    .stNumberInput input {
        border-radius: 12px;
    }

    .stSelectbox > div,
    .stMultiSelect > div {
        border-radius: 12px;
    }

    /* ======================================================
       FOOTER
       ====================================================== */

    .footer {
        text-align: center;
        padding: 55px 0 10px;
        color: #918895;
        font-size: 13px;
    }

    /* ======================================================
       MOBILE
       ====================================================== */

    @media (max-width: 768px) {

        .hero-title {
            font-size: 43px;
            letter-spacing: -2px;
        }

        .hero-subtitle {
            font-size: 17px;
        }

        .hero-wrapper {
            padding-top: 35px;
        }

        .hero-visual {
            min-height: 300px;
            margin-top: 25px;
        }

        .section-title {
            font-size: 30px;
        }

        .welcome-title {
            font-size: 34px;
        }

        .assessment-title {
            font-size: 32px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# API HELPERS
# ============================================================

def get_headers():

    if not st.session_state.token:
        return {}

    return {
        "Authorization": (
            f"Bearer {st.session_state.token}"
        )
    }


def signup_user(name, email, password):

    try:

        response = requests.post(
            f"{API_URL}/auth/signup",
            json={
                "name": name,
                "email": email,
                "password": password
            },
            timeout=10
        )

        if response.status_code == 200:
            return True, "Account created successfully."

        try:
            message = response.json().get(
                "detail",
                "Signup failed."
            )
        except Exception:
            message = "Signup failed."

        return False, message

    except requests.exceptions.ConnectionError:

        return False, "FastAPI server is not running."

    except requests.exceptions.RequestException:

        return False, "Could not connect to SkinAI API."


def login_user(email, password):

    try:

        response = requests.post(
            f"{API_URL}/auth/login",
            json={
                "email": email,
                "password": password
            },
            timeout=10
        )

        if response.status_code == 200:

            data = response.json()

            st.session_state.token = data[
                "access_token"
            ]

            st.session_state.user = {
                "user_id": data["user_id"],
                "name": data["name"],
                "email": data["email"]
            }

            st.session_state.page = "dashboard"

            return True, "Login successful."

        try:
            message = response.json().get(
                "detail",
                "Login failed."
            )
        except Exception:
            message = "Login failed."

        return False, message

    except requests.exceptions.ConnectionError:

        return False, "FastAPI server is not running."

    except requests.exceptions.RequestException:

        return False, "Could not connect to SkinAI API."


def logout():

    st.session_state.token = None
    st.session_state.user = None
    st.session_state.profile = None
    st.session_state.page = "home"

    st.rerun()


def load_profile():

    if not st.session_state.token:
        return None

    try:

        response = requests.get(
            f"{API_URL}/profile",
            headers=get_headers(),
            timeout=10
        )

        if response.status_code == 200:

            profile = response.json()

            st.session_state.profile = profile

            return profile

        return None

    except requests.exceptions.RequestException:

        return None


# ============================================================
# TOP NAVIGATION
# ============================================================

if st.session_state.user:

    nav1, nav2, nav3, nav4, nav5 = st.columns(
        [5.5, 1, 1, 1, 1]
    )

    with nav1:

        if st.button(
            "SkinAI ✨",
            key="logo_button"
        ):

            st.session_state.page = "dashboard"
            st.rerun()

    with nav2:

        if st.button("Home"):

            st.session_state.page = "home"
            st.rerun()

    with nav3:

        if st.button("Matches"):

            st.session_state.page = "recommendations"
            st.rerun()

    with nav4:

        if st.button("Profile"):

            st.session_state.page = "profile"
            st.rerun()

    with nav5:

        if st.button("Logout"):

            logout()

else:

    nav1, nav2, nav3, nav4 = st.columns(
        [6, 1.2, 1.2, 1.4]
    )

    with nav1:

        if st.button(
            "SkinAI ✨",
            key="public_logo"
        ):

            st.session_state.page = "home"
            st.rerun()

    with nav2:

        if st.button("How it works"):

            st.session_state.page = "home"
            st.rerun()

    with nav3:

        if st.button("Login"):

            st.session_state.page = "login"
            st.rerun()

    with nav4:

        if st.button("Get Started"):

            st.session_state.page = "signup"
            st.rerun()


st.divider()


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.page == "home":

    left, right = st.columns(
        [1.05, 0.95],
        gap="large"
    )

    with left:

        st.markdown(
            '<div class="hero-wrapper">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="eyebrow">✨ AI-powered skincare discovery</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="hero-title">
                Your skin.<br>
                Your preferences.<br>
                <span class="hero-gradient">
                    Your personalized routine.
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="hero-subtitle">
                Discover skincare products matched to your
                skin type, concerns and preferences —
                powered by an intelligent recommendation engine.
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "✨ Find My Matches",
            use_container_width=True,
            key="hero_start"
        ):

            st.session_state.page = "signup"
            st.rerun()

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    with right:

      st.html(
    """
    <style>
        .hero-visual {
            min-height: 430px;
            border-radius: 32px;
            background:
                radial-gradient(
                    circle at 25% 25%,
                    rgba(255,255,255,0.9),
                    transparent 25%
                ),
                linear-gradient(
                    135deg,
                    #fce7f3,
                    #ede9fe
                );
            border: 1px solid rgba(255,255,255,0.8);
            box-shadow:
                0 30px 80px rgba(160, 100, 150, 0.13);
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }

        .floating-card {
            position: absolute;
            background: linear-gradient(
                135deg,
                #fce7f3,
                #f3e8ff
            );
            border: 1px solid rgba(255,255,255,0.95);
            border-radius: 18px;
            padding: 13px 17px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.08);
            font-size: 13px;
            font-weight: 700;
            color: #211a25;
            z-index: 3;
        }

        .floating-one {
            top: 35px;
            left: 30px;
        }

        .floating-two {
            bottom: 45px;
            right: 25px;
        }

        .floating-three {
            bottom: 75px;
            left: 25px;
        }

        .orb {
            width: 250px;
            height: 250px;
            border-radius: 50%;
            background:
                linear-gradient(
                    135deg,
                    rgba(255,255,255,0.95),
                    rgba(255,255,255,0.35)
                );
            box-shadow:
                0 25px 60px rgba(168, 85, 247, 0.18);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 95px;
            z-index: 1;
        }
    </style>

    <div class="hero-visual">

        <div class="floating-card floating-one">
            ✨ 94% Personalized Match
        </div>

        <div class="floating-card floating-two">
            ✓ Acne match
        </div>

        <div class="floating-card floating-three">
            🧴 Dry skin
        </div>

        <div class="orb">
            🧴
        </div>

    </div>
    """
)

    # --------------------------------------------------------
    # FEATURES
    # --------------------------------------------------------

    st.html(
        """
        <div class="section-title">
            Skincare, but make it personal.
        </div>

        <div class="section-subtitle">
            One profile. Smarter product discovery.
        </div>
        """,
       
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    🧖
                </div>

                <div class="feature-title">
                    Understand your skin
                </div>

                <div class="feature-text">
                    Tell SkinAI about your skin type,
                    concerns and preferences.
                </div>

            </div>
            """,
            
        )

    with col2:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    🧠
                </div>

                <div class="feature-title">
                    Let AI do the matching
                </div>

                <div class="feature-text">
                    Your profile is compared with
                    skincare products using our
                    recommendation engine.
                </div>

            </div>
            """,
            
        )

    with col3:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    ✨
                </div>

                <div class="feature-title">
                    Know why it matches
                </div>

                <div class="feature-text">
                    Every recommendation comes with
                    understandable reasons for the match.
                </div>

            </div>
            """,
          
        )


    # --------------------------------------------------------
    # AI SECTION
    # --------------------------------------------------------

    st.html(
    """
    <div class="ai-box">

        <div class="ai-title">
            Not just recommendations.
        </div>

        <div class="ai-title">
            Recommendations that make sense.
        </div>

        <br>

        <div class="ai-text">
            SkinAI combines your skin profile with
            product information to rank products
            based on how closely they match your needs.
        </div>

        <br>

        <span class="ai-pill">Skin type</span>
        <span class="ai-pill">Skin concerns</span>
        <span class="ai-pill">Feature vectors</span>
        <span class="ai-pill">Cosine similarity</span>
        <span class="ai-pill">Concern matching</span>
        <span class="ai-pill">Explainable results</span>

    </div>
    """
)


    # --------------------------------------------------------
    # CTA
    # --------------------------------------------------------

    st.html(
        """
        <div style="
            text-align:center;
            padding:65px 0 20px;
        ">

            <div class="section-title">
                Ready to meet your matches?
            </div>

            <div class="section-subtitle">
                Your skincare journey starts with one profile.
            </div>

        </div>
        """,
    
    )

    col1, col2, col3 = st.columns([2, 3, 2])

    with col2:

        if st.button(
            "Start my skincare journey ✨",
            use_container_width=True,
            key="bottom_cta"
        ):

            st.session_state.page = "signup"
            st.rerun()

    st.html(
        """
        <div class="footer">
            SkinAI • Personalized skincare discovery
            <br>
            For product discovery only — not medical advice.
        </div>
        """,

    )


# ============================================================
# SIGNUP
# ============================================================

elif st.session_state.page == "signup":

    st.html(
        '<div class="auth-wrapper">'
    )

    st.html(
        """
        <div class="auth-header">

            <div class="eyebrow">
                ✨ Start your journey
            </div>

            <div class="auth-title">
                Create your SkinAI account
            </div>

            <div class="auth-subtitle">
                Your personalized skincare journey starts here.
            </div>

        </div>
        """
    )

    name = st.text_input(
        "Full name",
        placeholder="Your name"
    )

    email = st.text_input(
        "Email",
        placeholder="you@example.com"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Create a password"
    )

    confirm_password = st.text_input(
        "Confirm password",
        type="password",
        placeholder="Repeat your password"
    )

    if st.button(
        "Create my account ✨",
        use_container_width=True
    ):

        if not name or not email or not password:

            st.error(
                "Please fill in all required fields."
            )

        elif password != confirm_password:

            st.error(
                "Passwords do not match."
            )

        else:

            success, message = signup_user(
                name,
                email,
                password
            )

            if success:

                st.success(message)

                st.session_state.page = "login"

                st.info(
                    "Your account is ready. Log in to continue."
                )

            else:

                st.error(message)

    st.divider()

    if st.button(
        "Already have an account? Login",
        use_container_width=True
    ):

        st.session_state.page = "login"
        st.rerun()

# ============================================================
# LOGIN
# ============================================================

elif st.session_state.page == "login":

    st.html(
        '<div class="auth-wrapper">'
    )

    st.html(
        """
        <div class="auth-header">

            <div class="eyebrow">
                👋 Welcome back
            </div>

            <div class="auth-title">
                Your skin journey awaits.
            </div>

            <div class="auth-subtitle">
                Log in to access your personalized matches.
            </div>

        </div>
        """
    )

    email = st.text_input(
        "Email",
        placeholder="you@example.com",
        key="login_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Your password",
        key="login_password"
    )

    if st.button(
        "Login ✨",
        use_container_width=True
    ):

        if not email or not password:

            st.error(
                "Please enter your email and password."
            )

        else:

            success, message = login_user(
                email,
                password
            )

            if success:
                st.rerun()

            else:
                st.error(message)

    st.divider()

    if st.button(
        "New to SkinAI? Create an account",
        use_container_width=True
    ):

        st.session_state.page = "signup"
        st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

elif st.session_state.page == "dashboard":

    user = st.session_state.user

    profile = load_profile()

    st.html(
        """
        <div class="eyebrow">
            ✨ Your SkinAI space
        </div>
        """
    )

    st.html(
        f"""
        <div class="welcome-title">
            Hey, {user["name"]} 👋
        </div>

        <div class="hero-subtitle">
            Ready to discover your next skincare match?
        </div>
        """
    )

    if profile:

        concerns = profile["concerns"]

        col1, col2, col3 = st.columns(3)

        # ----------------------------------------------------
        # STAT CARD 1
        # ----------------------------------------------------

        with col1:

            st.html(
                f"""
                <div class="stat-card">

                    <div class="stat-label">
                        SKIN TYPE
                    </div>

                    <div class="stat-value">
                        {profile["skin_type"]}
                    </div>

                </div>
                """
            )

        # ----------------------------------------------------
        # STAT CARD 2
        # ----------------------------------------------------

        with col2:

            st.html(
                f"""
                <div class="stat-card">

                    <div class="stat-label">
                        CONCERNS
                    </div>

                    <div class="stat-value">
                        {len(concerns)}
                    </div>

                </div>
                """
            )

        # ----------------------------------------------------
        # STAT CARD 3
        # ----------------------------------------------------

        with col3:

            budget = profile.get("budget")

            budget_text = (
                f"₹{budget}"
                if budget
                else "Not set"
            )

            st.html(
                f"""
                <div class="stat-card">

                    <div class="stat-label">
                        BUDGET
                    </div>

                    <div class="stat-value">
                        {budget_text}
                    </div>

                </div>
                """
            )

        # ----------------------------------------------------
        # PROFILE SECTION
        # ----------------------------------------------------

        st.html("<br>")

        st.html(
            """
            <div class="profile-card">

                <div class="eyebrow">
                    Your profile
                </div>

                <h2>
                    Your skin, your preferences.
                </h2>

            </div>
            """
        )

        st.html(
            f"""
            <div class="profile-detail">
                <strong>Skin type:</strong> {profile['skin_type']}
            </div>
            """
        )

        # ----------------------------------------------------
        # RECOMMENDATIONS BUTTON
        # ----------------------------------------------------

        if st.button(
            "✨ Get my personalized matches",
            use_container_width=True
        ):

            st.session_state.page = "recommendations"
            st.rerun()

        # ----------------------------------------------------
        # EDIT PROFILE BUTTON
        # ----------------------------------------------------

        if st.button(
            "Edit my skin profile",
            use_container_width=True
        ):

            st.session_state.page = "assessment"
            st.rerun()

    # ========================================================
    # NO PROFILE
    # ========================================================

    else:

        st.html(
            """
            <div class="profile-card">

                <div class="eyebrow">
                    Your first step
                </div>

                <h2>
                    Let's understand your skin.
                </h2>

                <p>
                    Tell us about your skin type and
                    concerns so SkinAI can find better matches.
                </p>

            </div>
            """
        )

        st.html("<br>")

        if st.button(
            "Start my skin assessment ✨",
            use_container_width=True
        ):

            st.session_state.page = "assessment"
            st.rerun()

# ============================================================
# ASSESSMENT
# ============================================================

elif st.session_state.page == "assessment":

    st.html(
        """
        <div class="assessment-header">

            <div class="step-label">
                Your personalized profile
            </div>

            <div class="assessment-title">
                Let's get to know your skin ✨
            </div>

            <div class="hero-subtitle"
                 style="margin:auto;">
                A few quick questions help us
                understand what you're looking for.
            </div>

        </div>
        """
    )

    st.progress(1.0)

    skin_type = st.selectbox(
        "What's your skin type?",
        [
            "Normal",
            "Dry",
            "Oily",
            "Combination",
            "Sensitive"
        ]
    )

    concerns = st.multiselect(
        "What are your main concerns?",
        [
            "Acne",
            "Pimples",
            "Whitehead/Blackhead",
            "Pores",
            "Pigmentation",
            "Dark Spots",
            "Hydration",
            "Broken barrier",
            "Irritation",
            "Skin soothing",
            "Exfoliation",
            "Sun protection"
        ]
    )

    age_range = st.selectbox(
        "What's your age range?",
        [
            "Under 18",
            "18-24",
            "25-34",
            "35-44",
            "45+"
        ]
    )

    product_preferences = st.text_input(
        "What product textures/preferences do you like?",
        placeholder="Example: Lightweight, gel, fragrance-free"
    )

    budget = st.number_input(
        "What's your skincare budget?",
        min_value=0,
        max_value=100000,
        value=1000,
        step=100
    )

    ingredients_to_avoid = st.text_input(
        "Anything you'd like to avoid?",
        placeholder="Example: Fragrance, Alcohol"
    )

    st.html("<br>")

    if st.button(
        "✨ Analyze my skin profile",
        use_container_width=True
    ):

        if not concerns:

            st.error(
                "Select at least one skincare concern."
            )

        else:

            try:

                response = requests.post(
                    f"{API_URL}/profile",
                    headers=get_headers(),
                    json={
                        "skin_type": skin_type,
                        "concerns": concerns,
                        "age_range": age_range,
                        "product_preferences": (
                            product_preferences
                            if product_preferences
                            else None
                        ),
                        "budget": budget,
                        "ingredients_to_avoid": (
                            ingredients_to_avoid
                            if ingredients_to_avoid
                            else None
                        )
                    },
                    timeout=10
                )

                if response.status_code == 200:

                    st.session_state.page = "analysis"
                    st.rerun()

                else:

                    st.error(
                        response.json().get(
                            "detail",
                            "Could not save your profile."
                        )
                    )

            except requests.exceptions.RequestException:

                st.error(
                    "Could not connect to SkinAI API."
                )


# ============================================================
# AI ANALYSIS
# ============================================================

elif st.session_state.page == "analysis":

    st.html(
        """
        <div style="
            text-align:center;
            padding:100px 10px;
        ">

            <div style="
                font-size:75px;
                margin-bottom:20px;
            ">
                ✨
            </div>

            <div class="assessment-title">
                SkinAI is thinking...
            </div>

            <div class="hero-subtitle"
                 style="margin:auto;">
                We're finding the products that
                best match your profile.
            </div>

        </div>
        """
    )

    progress = st.progress(0)

    status = st.empty()

    steps = [
        "✓ Understanding your skin type",
        "✓ Mapping your skincare concerns",
        "✓ Comparing product features",
        "✓ Ranking your personalized matches",
        "✓ Preparing your recommendations"
    ]

    for i, step in enumerate(steps):

        status.markdown(
            f"""
            <div style="
                text-align:center;
                font-weight:650;
                color:#6d6471;
                margin:12px;
            ">
                {step}
            </div>
            """,
            unsafe_allow_html=True
        )

        progress.progress(
            int(((i + 1) / len(steps)) * 100)
        )

        time.sleep(0.45)

    st.session_state.page = "recommendations"

    st.rerun()
    # ============================================================
# RECOMMENDATIONS
# ============================================================

# ============================================================
# RECOMMENDATIONS
# ============================================================

elif st.session_state.page == "recommendations":

    st.html(
        """
        <div class="eyebrow">
            ✨ Personalized for you
        </div>

        <div class="welcome-title">
            Your skincare matches.
        </div>

        <div class="hero-subtitle">
            Products ranked according to your saved
            skin profile and concerns.
        </div>
        """
    )


    # ========================================================
    # GET RECOMMENDATIONS FROM FASTAPI
    # ========================================================

    try:

        response = requests.get(
            f"{API_URL}/recommendations",
            headers=get_headers(),
            timeout=20
        )


        # ====================================================
        # SUCCESS
        # ====================================================

        if response.status_code == 200:

            data = response.json()

            recommendations = data.get(
                "recommendations",
                []
            )


            # =================================================
            # NO RECOMMENDATIONS
            # =================================================

            if not recommendations:

                st.info(
                    "We couldn't find recommendations "
                    "for your current profile."
                )


            # =================================================
            # SHOW RECOMMENDATIONS
            # =================================================

            else:

                st.success(
                    f"We found {len(recommendations)} "
                    f"personalized matches."
                )


                for index, product in enumerate(
                    recommendations
                ):


                    # =========================================
                    # PRODUCT DATA
                    # =========================================

                    score = (
                        product.get(
                            "final_score",
                            0
                        ) * 100
                    )


                    product_name = product.get(
                        "product",
                        "Unknown product"
                    )


                    skin_type = product.get(
                        "skin_type",
                        "Not specified"
                    )


                    concern = product.get(
                        "concern",
                        "Not specified"
                    )


                    reasons = product.get(
                        "reasons",
                        []
                    )


                    product_image = product.get(
                        "product_pic"
                    )


                    product_url = product.get(
                        "product_url"
                    )


                    # =========================================
                    # PRODUCT CARD
                    # =========================================

                    st.html(
                        f"""
                        <div class="result-card">

                            <div style="
                                display:flex;
                                gap:35px;
                                align-items:flex-start;
                            ">


                                <!-- PRODUCT IMAGE -->

                                <div style="
                                    width:220px;
                                    min-width:220px;
                                    height:260px;

                                    display:flex;
                                    align-items:center;
                                    justify-content:center;

                                    background:#faf7fb;

                                    border-radius:20px;

                                    overflow:hidden;
                                ">

                                    {
                                        f'''
                                        <img
                                            src="{product_image}"
                                            style="
                                                width:100%;
                                                height:100%;
                                                object-fit:contain;
                                                padding:15px;
                                            "
                                        >
                                        '''

                                        if product_image

                                        else

                                        '''
                                        <div style="
                                            color:#999;
                                            font-size:14px;
                                            text-align:center;
                                        ">
                                            Product image unavailable
                                        </div>
                                        '''
                                    }

                                </div>


                                <!-- PRODUCT INFORMATION -->

                                <div style="
                                    flex:1;
                                    padding:5px 0;
                                ">


                                    <!-- MATCH SCORE -->

                                    <div class="match-badge">
                                        {score:.0f}% PERSONALIZED MATCH
                                    </div>


                                    <!-- PRODUCT NAME -->

                                    <div
                                        class="product-name"
                                        style="
                                            margin-top:18px;
                                        "
                                    >
                                        {product_name}
                                    </div>


                                    <!-- PRODUCT INFORMATION -->

                                    <div style="
                                        margin-top:18px;

                                        color:#6d6471;

                                        font-size:15px;

                                        line-height:1.8;
                                    ">

                                        <div>

                                            <strong>
                                                Skin type:
                                            </strong>

                                            {skin_type}

                                        </div>


                                        <div>

                                            <strong>
                                                Concerns:
                                            </strong>

                                            {concern}

                                        </div>

                                    </div>


                                    <!-- WHY THIS MATCH -->

                                    <div style="
                                        margin-top:22px;

                                        font-size:16px;

                                        font-weight:700;
                                    ">

                                        Why this match?

                                    </div>


                                    <div style="
                                        margin-top:10px;

                                        color:#6d6471;

                                        line-height:1.8;
                                    ">

                                        {
                                            "".join(
                                                f"""
                                                <div>
                                                    ✓ {reason}
                                                </div>
                                                """
                                                for reason in reasons
                                            )
                                        }

                                    </div>


                                    <!-- PRODUCT LINK -->

                                    {
                                        f'''
                                        <div style="
                                            margin-top:20px;
                                        ">

                                            <a
                                                href="{product_url}"
                                                target="_blank"
                                                style="
                                                    text-decoration:none;
                                                    font-weight:650;
                                                    color:#c94f9b;
                                                "
                                            >
                                                View product ↗
                                            </a>

                                        </div>
                                        '''

                                        if product_url

                                        else ""
                                    }


                                </div>

                            </div>

                        </div>
                        """
                    )


                    # =========================================
                    # SAVE BUTTON
                    # =========================================

                    if st.button(
                        "♡ Save",
                        key=f"save_{index}"
                    ):

                        if product_name not in (
                            st.session_state.favorites
                        ):

                            st.session_state.favorites.append(
                                product_name
                            )

                            st.success(
                                "Saved to your favorites ❤️"
                            )

                        else:

                            st.info(
                                "Already saved."
                            )


                    st.html("<br>")


        # ====================================================
        # API ERROR
        # ====================================================

        else:

            try:

                detail = response.json().get(
                    "detail",
                    "Could not generate recommendations."
                )

            except Exception:

                detail = (
                    "Could not generate recommendations."
                )


            st.error(detail)


            if st.button(
                "Complete my profile",
                use_container_width=True
            ):

                st.session_state.page = "assessment"

                st.rerun()


    # ========================================================
    # CONNECTION ERROR
    # ========================================================

    except requests.exceptions.RequestException:

        st.error(
            "Could not connect to SkinAI API."
        )


        # ============================================================
# PROFILE
# ============================================================

elif st.session_state.page == "profile":

    user = st.session_state.user

    st.html(
        """
        <div class="eyebrow">
            👤 Account
        </div>

        <div class="welcome-title">
            Your profile.
        </div>
        """
    )

    st.html("<br>")

    st.html(
        f"""
        <div class="profile-card">

            <h2>
                {user["name"]}
            </h2>

            <p>
                {user["email"]}
            </p>

        </div>
        """
    )

    st.html("<br>")

    profile = load_profile()

    if profile:

       st.html(
        """
        <div style="
            color:#211a25;
            margin-top:25px;
            margin-bottom:20px;
        ">

            <div style="
                font-size:26px;
                font-weight:750;
                margin-bottom:20px;
            ">
                Skin profile
            </div>

            <div style="
                font-size:16px;
                line-height:2;
                color:#5f5664;
            ">

                <div>
                    <strong style="color:#211a25;">
                        Skin type:
                    </strong>
                    """ + profile["skin_type"] + """
                </div>

                <div>
                    <strong style="color:#211a25;">
                        Concerns:
                    </strong>
                    """ + ", ".join(profile["concerns"]) + """
                </div>

                <div>
                    <strong style="color:#211a25;">
                        Age range:
                    </strong>
                    """ + (profile.get("age_range") or "Not specified") + """
                </div>

                <div>
                    <strong style="color:#211a25;">
                        Preferences:
                    </strong>
                    """ + (profile.get("product_preferences") or "Not specified") + """
                </div>

                <div>
                    <strong style="color:#211a25;">
                        Budget:
                    </strong>
                    ₹""" + str(profile.get("budget") or 0) + """
                </div>

                <div>
                    <strong style="color:#211a25;">
                        Ingredients to avoid:
                    </strong>
                    """ + (profile.get("ingredients_to_avoid") or "None specified") + """
                </div>

            </div>

        </div>
        """
    )

    st.html("<br>")

    if st.button(
        "Edit skin profile",
        use_container_width=True
    ):

        st.session_state.page = "assessment"
        st.rerun()