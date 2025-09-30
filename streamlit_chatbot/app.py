import streamlit as st
import openai
import os

# Set up the OpenAI API key from Codespaces secrets.
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set the title of the app.
st.title("AI Shopping Assistant")

# Use Streamlit's session state to store the chat history.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful and friendly shopping assistant. You help users find products, compare prices, and suggest stores and websites."}
    ]

# Display the chat history.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input using the chat input box.
if prompt := st.chat_input("What are you looking for today?"):
    # Add the user's message to the chat history and display it.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get a response from the AI.
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                ]
            )
            assistant_response = response.choices[0].message.content
            st.markdown(assistant_response)

            # Add the assistant's response to the chat history.
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})

