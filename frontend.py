import streamlit as st
import requests

# Set up the page layout
st.set_page_config(page_title="TechGear AI Support", page_icon="🤖")
st.title("🤖 TechGear Private AI Agent")
st.caption("Powered by local Llama 3.2. No data leaves your machine.")

# Initialize an empty chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# The chat input box at the bottom of the screen
if prompt := st.chat_input("Ask a question about our policies..."):
    
    # 1. Display the user's message on the screen
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Send the question to your FastAPI backend
    with st.spinner("Searching company documents..."):
        try:
            # We are sending the data exactly like we did on the FastAPI testing page!
            response = requests.post("http://127.0.0.1:8000/ask", json={"question": prompt})
            
            if response.status_code == 200:
                answer = response.json()["answer"]
            else:
                answer = "⚠️ Error: Backend returned a bad response."
        except requests.exceptions.ConnectionError:
            answer = "⚠️ Error: Could not connect. Is your FastAPI server running in the other terminal?"

    # 3. Display the AI's answer on the screen
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})