import streamlit as st
from llm_file_assistant import run_assistant

# Page config
st.set_page_config(
    page_title="File Assistant",
    page_icon="📄",
    layout="centered"
)

# Title
st.title("📄 File Assistant")
st.caption("Ask me anything about your files")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
if prompt := st.chat_input("Ask something about your files..."):

    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = run_assistant(prompt)
        st.markdown(response)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
