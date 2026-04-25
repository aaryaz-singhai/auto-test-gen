import os
import time
from openai import OpenAI
import anthropic
from groq import Groq


# --- Clients ---
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

gemini_client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# claude_client = anthropic.Anthropic(
#     api_key=os.getenv("ANTHROPIC_API_KEY")
# )

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# --- Common OpenAI-style caller ---
def call_openai_like(client, model, prompt):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content


# --- Claude caller (different API) ---
def call_claude(prompt):
    response = claude_client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=2000,
        temperature=0.2,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text


# --- Groq caller ---
def call_groq(prompt):
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content


# --- Main function ---
def generate_tests(function_name, function_code, context):
    prompt = f"""
You are a senior Python test engineer.

Write pytest unit tests for the following function.

Requirements:
- Cover edge cases
- Include invalid inputs
- Use pytest
- Keep tests clean and readable
- Return ONLY code, no explanation

Function:
{function_code}

Context:
{context}
"""

    providers = [
        ("OpenAI", lambda: call_openai_like(openai_client, "gpt-4o-mini", prompt)),
        ("Gemini", lambda: call_openai_like(gemini_client, "gemini-2.0-flash", prompt)),
        ("Groq", lambda: call_groq(prompt)),
        # ("Claude", lambda: call_claude(prompt)),
    ]

    last_error = None

    for name, provider in providers:
        for attempt in range(2):  # retry each provider twice
            try:
                return provider()
            except Exception as e:
                last_error = e
                print(f"[WARNING] {name} failed (attempt {attempt + 1}): {e}")
                time.sleep(1)  # small backoff

        print(f"[INFO] Switching from {name} to next provider...")

    raise RuntimeError(f"All providers failed. Last error: {last_error}")