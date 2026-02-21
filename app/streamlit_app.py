import streamlit as st
from backend.services.user_service import register_user, login_user

st.set_page_config(page_title="AI Goal Tracker", layout="wide")

# ===========================
# SESSION STATE INIT
# ===========================
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# ===========================
# AUTH PAGE
# ===========================
if st.session_state.user_id is None:

    st.title("🔐 Login / Register")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user_id = login_user(username, password)

            if user_id:
                st.session_state.user_id = user_id
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Register"):
            user_id = register_user(new_user, new_pass)

            if user_id:
                st.success("Registration successful! Please login.")
            else:
                st.error("Username already exists")

    st.stop()

# ===========================
# AFTER LOGIN
# ===========================
st.title("🚀 AI Goal Tracker")

st.success("You are logged in!")

if st.button("Logout"):
    st.session_state.user_id = None
    st.rerun()

st.info("Use the sidebar to navigate between pages.")