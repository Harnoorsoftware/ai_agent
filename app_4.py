import os
import streamlit as st
import fitz  # PyMuPDF
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()  # Ensure this is loading the correct .env file

# Check if the token is set
token = os.environ.get("GITHUB_TOKEN")

# Debugging: Print all environment variables
print("All Environment Variables:", os.environ)  # Check if GITHUB_TOKEN is present

if not token:
    st.error("GITHUB_TOKEN is not set. Please check your environment variables.")
    st.stop()

# Continue with the rest of your code...


# Azure AI client setup
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-nano"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

# Streamlit UI
st.title("📄 AI Agent - PDF Reader ")
st.markdown("Upload a PDF and ask questions based on its content.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

pdf_text = ""
if uploaded_file:
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            pdf_text = "\n".join([page.get_text() for page in doc])
        st.success("PDF uploaded and processed.")
    except Exception as e:
        st.error(f"Failed to read PDF: {e}")

user_query = st.text_input("Ask a question about the PDF:")

if user_query and pdf_text:
    try:
        system_prompt = "You are a helpful assistant. Answer the question based only on the PDF content provided."
        combined_input = f"PDF Content:\n{pdf_text[:4000]}\n\nQuestion: {user_query}"  # Limit to first 4000 characters

        response = client.complete(
            messages=[
                SystemMessage(content=system_prompt),
                UserMessage(content=combined_input),
            ],
            temperature=0.7,
            top_p=1,
            model=model
        )

        # Check if response has choices
        if response.choices and len(response.choices) > 0:
            st.write("**AI Answer:**", response.choices[0].message.content)
        else:
            st.error("No response from the AI model.")

    except Exception as e:
        st.error(f"Error during inference: {e}")
elif user_query:
    st.warning("Please upload a PDF first.")
