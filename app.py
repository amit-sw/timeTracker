import streamlit as st

from chat_ui import render_chat
from utils.supabase_client import get_or_create_profile


def _get_user_value(user, key, default=""):
    if hasattr(user, key):
        return getattr(user, key) or default
    if hasattr(user, "get"):
        return user.get(key, default) or default
    return default


def show_login_screen():
    st.sidebar.button("Log in with Google", on_click=st.login)
    st.title("Welcome")
    st.write("Please log in to continue.")


def show_authenticated_screen(user):
    name = _get_user_value(user, "name", "User")
    email = _get_user_value(user, "email", "")
    if email:
        _ensure_profile(email, name)
    else:
        st.sidebar.warning("No email found for this user.")
    st.sidebar.write(f"**{name}**")
    st.sidebar.write(email or "unknown email")
    st.sidebar.button("Log out", on_click=st.logout)
    st.title(f"Welcome back, {name}!")
    st.write("You are logged in. Thanks for stopping by.")
    render_chat()


def _ensure_profile(email, name):
    if st.session_state.get("profile_loaded"):
        return
    try:
        st.session_state["profile"] = get_or_create_profile(email, name)
    except Exception as exc:
        st.sidebar.warning(f"Profile setup failed: {exc}")
    finally:
        st.session_state["profile_loaded"] = True


user = st.user
is_logged_in = bool(user) and getattr(user, "is_logged_in", False)

if is_logged_in:
    show_authenticated_screen(user)
else:
    show_login_screen()
