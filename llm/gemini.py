import os
from dotenv import load_dotenv
from google import genai

# Load .env file
load_dotenv()

# Read API key
api_key = os.getenv("GOOGLE_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)


def ask_gemini(context, question):
    prompt = f"""
You are EMMA, an AI Healthcare Receptionist.

Answer ONLY using the medical context below.
If the answer is not in the context, say:
"I don't have enough information to answer that."

Medical Context:
{context}

Patient Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text