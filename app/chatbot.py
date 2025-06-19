import requests
import os
from dotenv import load_dotenv
load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct"

HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

def ask_career_bot(question, user_resume_summary):
    """Sends a question and context to the LLM via Hugging Face API."""

    prompt = f"""You are an AI career assistant. The user has the following resume data:

{user_resume_summary}

Now, answer their question in a helpful and friendly way.

Question: {question}
Answer:"""

    response = requests.post(
        API_URL,
        headers=HEADERS,
        json={"inputs": prompt, "parameters": {"max_new_tokens": 200}}
    )

    if response.status_code == 200:
        output = response.json()
        return output[0]["generated_text"].split("Answer:")[-1].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"
