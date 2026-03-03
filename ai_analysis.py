"""Competitive Torpedoes - OpenAI-powered chart analysis."""
from openai import OpenAI
from config import OPENAI_API_KEY, AI_SYSTEM_PROMPT
import json

_client = None

def get_client():
    global _client
    if _client is None and OPENAI_API_KEY:
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def analyze_section(section_title: str, data_context: dict, competitor: str,
                    conversation: list | None = None) -> str:
    client = get_client()
    if client is None:
        return "OpenAI API key not configured. Add OPENAI_API_KEY to your .env file."

    if conversation is None:
        conversation = []

    if not conversation:
        user_msg = (
            f"Analyze this {section_title} data comparing SOCi vs {competitor} "
            f"(top 50 brands each by LVI score). Give me sales-ready talking points."
            f"\n\nData:\n{json.dumps(data_context, indent=2)}"
        )
        conversation = [{"role": "user", "content": user_msg}]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": AI_SYSTEM_PROMPT},
                *conversation,
            ],
            max_tokens=1000,
            temperature=0.7,
        )
        return response.choices[0].message.content or "No response generated."
    except Exception as e:
        return f"Analysis error: {str(e)}"
