import openai
import streamlit as st

def configure_openai():
    OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", None)
    if not OPENAI_API_KEY:
        st.error("Please add your OpenAI API key to the Streamlit secrets.toml file.")
        st.stop()
    openai.api_key = OPENAI_API_KEY
    return openai.OpenAI()

def interact_with_chatbot(prompt):
    client = configure_openai()
    response = client.chat.completions.create(
        model="gpt-4",  # Usaremos un modelo adecuado para el chatbot
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,  # Limitar los tokens para mantener las respuestas concisas
        temperature=0.7,  # Ajustar la creatividad de la respuesta
    )
    chatbot_response = response.choices[0].message.content.strip()
    return chatbot_response

def chatbot_interface():
    st.title("Medical Chatbot")
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("You: ", key="input", placeholder="Write your question here...")

    if st.button("Send"):
        if user_input:
            with st.spinner("Chatbot is typing..."):
                response = interact_with_chatbot(user_input)
                st.session_state.chat_history.append({"user": user_input, "bot": response})
    
    if st.session_state.chat_history:
        for chat in st.session_state.chat_history:
            st.write(f"You: {chat['user']}")
            st.write(f"Bot: {chat['bot']}")
