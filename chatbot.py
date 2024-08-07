import openai
import streamlit as st

def configure_openai():
    OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", None)
    if not OPENAI_API_KEY:
        st.error("Please add your OpenAI API key to the Streamlit secrets.toml file.")
        st.stop()
    openai.api_key = OPENAI_API_KEY
    return openai.OpenAI()

def load_prompt_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            prompt = file.read().strip()
        return prompt
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        st.stop()

def interact_with_chatbot(user_input, prompt):
    client = configure_openai()
    messages = [{"role": "system", "content": prompt}, {"role": "user", "content": user_input}]
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=150,
        temperature=0.7,
    )
    chatbot_response = response.choices[0].message.content.strip()
    return chatbot_response

def chatbot_interface():
    st.title("Waves")

    # Load prompt from file
    prompt = load_prompt_from_file("Prompts/chatbot.txt")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

    user_input = st.text_input("You: ", key="input", placeholder="Write your question here...")

    # Check if there was a change in text input
    if user_input:
        st.session_state.user_input = user_input

    user_input = st.session_state.user_input

    if st.session_state.user_input and st.button("Submit", key="submit_button"):
        with st.spinner("Chatbot is typing..."):
            response = interact_with_chatbot(user_input, prompt)
            st.session_state.chat_history.append({"user": user_input, "bot": response})

        # Clear the input field after sending the message
        st.session_state.user_input = ""
        st.experimental_rerun()  # This is safe after a button press

    if st.session_state.chat_history:
        for chat in st.session_state.chat_history:
            st.write(f"You: {chat['user']}")
            st.write(f"Bot: {chat['bot']}")

if __name__ == "__main__":
    chatbot_interface()
