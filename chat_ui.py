import streamlit as st

from time_entry_flow import handle_user_message_stream


def render_chat():
    st.subheader("Chat")
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for message in st.session_state["messages"]:
        st.chat_message(message["role"]).write(message["content"])

    prompt = st.chat_input("Send a message")
    if not prompt:
        return

    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.spinner("Working on it...", show_time=True):
        with st.chat_message("assistant"):
            profile = st.session_state.get("profile") or {}
            profile_id = profile.get("id")
            stream = handle_user_message_stream(st.session_state["messages"], profile_id)
            response = st.write_stream(stream)

    st.session_state["messages"].append({"role": "assistant", "content": response})
