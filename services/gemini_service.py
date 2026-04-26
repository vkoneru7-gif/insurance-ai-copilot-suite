import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_policy_summary(question: str, grounded_context: str) -> str:
    prompt = f"""
You are an enterprise insurance AI assistant.

Use only provided context.
Be concise.
Do not invent coverage.

Question:
{question}

Context:
{grounded_context}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

    if hasattr(response, "text") and response.text:
        return response.text.strip()

    return "No LLM text returned."