import streamlit as st
from azure.ai.openai import ChatCompletionsClient, ChatMessage, ChatRole
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

# Setup
token = st.secrets["GITHUB_TOKEN"]
endpoint = "https://<harnoor-software-ai-agent>.openai.azure.com/"
model = "openai/gpt-4.1-nano"
temperature = 0.7 

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

# Set page config
st.set_page_config(page_title="Viva - AI Assistant")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        ChatMessage(role=ChatRole.SYSTEM, content="You are an assistant named Viva.")
    ]

# Sidebar: settings and theme
with st.sidebar:
    if st.button("Clear chat"):
        st.session_state.chat_history = [
            ChatMessage(role=ChatRole.SYSTEM, content="You are an assistant named Viva.")
        ]
        st.experimental_rerun()

# Title
st.title("Your typical AI agent -> Viva")

# User input
user_query = st.text_input("How can I assist you today?", key="input")

# Handle input
if user_query:
    st.session_state.chat_history.append(ChatMessage(role=ChatRole.USER, content=user_query))
    with st.spinner("Thinking..."):
        try:
            response = client.complete_chat(
                messages=st.session_state.chat_history,
                model=model,
                temperature=temperature,
                top_p=1,
            )
            reply = response.choices[0].message.content
            st.session_state.chat_history.append(
                ChatMessage(role=ChatRole.ASSISTANT, content=reply)
            )
        except HttpResponseError as e:
            if e.status_code == 404:
                st.error("Error: The requested resource was not found. Please check the endpoint.")
            else:
                st.error(f"An error occurred: {e.message}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# Display chat history
for msg in st.session_state.chat_history:
    if msg.role == ChatRole.USER:
        st.markdown(f"**You:** {msg.content}")
    elif msg.role == ChatRole.ASSISTANT:
        st.markdown(f"**Viva:** {msg.content}")
