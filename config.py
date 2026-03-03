"""Competitive Torpedoes - App configuration and constants."""
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

SOCI_GREEN = "#43D9A2"
COMPETITOR_GRAY = "#C0C0C0"
BENCHMARK_BLUE = "#5CC8E8"
SUCCESS = "#22c55e"
ERROR = "#ef4444"

PLATFORMS = [
    "Yext", "Birdeye", "Chatmeter",
    "Reputation.com", "Uberall", "RioSEO"
]

AI_SYSTEM_PROMPT = (
    "You are a local marketing analytics expert helping a SOCi sales rep "
    "prepare talking points. You receive data comparing SOCi top 50 brands "
    "(by LVI score) against a competitor platform top 50. Give 3-4 concise, "
    "compelling talking points highlighting SOCi strengths. If SOCi trails, "
    "acknowledge briefly but frame constructively. Use specific numbers from "
    "the data. 1-2 sentences each. Format as bullet points. No markdown headers."
)

TOP_N = 50
