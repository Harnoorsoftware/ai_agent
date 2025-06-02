import streamlit as st
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Use Streamlit secrets instead of .env
token = st.secrets["GITHUB_TOKEN"]

endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-nano"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

st.title("Your typical AI agent -> Viva ")

user_query = st.text_input("How can I assist  you today ?")

if user_query:
    try:
        response = client.complete(
            messages=[
                SystemMessage(""),
                UserMessage(user_query),
            ],
            temperature=1,
            top_p=1,
            model=model
        )
        st.write("**AI:**", response.choices[0].message.content)
    except Exception as e:
        st.error(f"Error: {e}")
