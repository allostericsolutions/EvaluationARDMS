import openai
import streamlit as st

def configure_openai():
    OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", None)
    if not OPENAI_API_KEY:
        st.error("Please add your OpenAI API key to the Streamlit secrets.toml file.")
        st.stop()
    openai.api_key = OPENAI_API_KEY
    return openai

def load_prompt_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            prompt = file.read().strip()
        return prompt
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        st.stop()

def interact_with_chatbot(user_input, prompt):
    openai_client = configure_openai()
    messages = [{"role": "system", "content": prompt}, {"role": "user", "content": user_input}]
    
    response = openai_client.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=150,
        temperature=0.7,
    )
    chatbot_response = response.choices[0].message["content"].strip()
    return chatbot_response

def chatbot_interface():
    st.title("Medical Chatbot")

    prompt = load_prompt_from_file("Prompts/chatbot.txt")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    user_input_temp = st.text_input("You: ", key="input", placeholder="Write your question here...")

    # El spinner se coloca fuera del if
    with st.spinner("Chatbot is typing..."):
        if user_input_temp and not st.session_state.submitted:
            # Define user_input dentro del if
            st.session_state.user_input = user_input_temp  
            response = interact_with_chatbot(st.session_state.user_input, prompt)
            st.session_state.chat_history.append({"user": st.session_state.user_input, "bot": response})
            st.session_state.submitted = True

    if st.session_state.chat_history:
        for chat in st.session_state.chat_history:
            st.write(f"You: {chat['user']}")
            st.write(f"Bot: {chat['bot']}")

if __name__ == "__main__":
    chatbot_interface()
