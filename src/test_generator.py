import os
import time
from openai import OpenAI
import anthropic
from groq import Groq
import ast

def clean_code(code: str) -> str:
    """
    Clean LLM-generated code:
    - Remove markdown ``` blocks
    - Remove leading 'python'
    - Remove stray triple quotes
    """

    # --- Remove markdown fences ---
    if "```" in code:
        parts = code.split("```")
        if len(parts) >= 3:
            code = parts[1]
        else:
            code = parts[0]

    code = code.strip()

    # --- Remove leading 'python' (common LLM artifact) ---
    if code.lower().startswith("python"):
        code = code[len("python"):].strip()

    # --- Remove surrounding triple quotes ---
    if code.startswith('"""') and code.endswith('"""'):
        code = code[3:-3].strip()

    # --- Remove any remaining standalone triple quotes lines ---
    lines = code.splitlines()
    lines = [line for line in lines if line.strip() not in ['"""', "'''"]]

    return "\n".join(lines).strip()


def is_valid_python(code: str) -> bool:
    """
    Check if generated code is syntactically valid.
    """
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


# --- Clients ---
# openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# gemini_client = OpenAI(
#     api_key=os.getenv("GEMINI_API_KEY"),
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

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

STRICT REQUIREMENTS:
- Return ONLY valid Python code
- NO markdown (no ``` blocks)
- NO explanations
- NO incomplete lines
- Code MUST be syntactically correct
- Include imports if needed
- Use pytest
- Cover edge cases and invalid inputs

Function:
{function_code}

Context:
{context}
IMPORTANT:
- The function is located in 'sample.py'
- Always import using:
  from sample import {function_name}
"""

    providers = [
        # ("OpenAI", lambda: call_openai_like(openai_client, "gpt-4o-mini", prompt)),
        # ("Gemini", lambda: call_openai_like(gemini_client, "gemini-2.0-flash", prompt)),
        ("Groq", lambda: call_groq(prompt)),
        # ("Claude", lambda: call_claude(prompt)),
    ]

    last_error = None

    for name, provider in providers:
        for attempt in range(3):  # increased retries
            try:
                raw = provider()
                cleaned = clean_code(raw)

                if is_valid_python(cleaned):
                    return cleaned
                else:
                    print(f"[WARNING] {name} returned invalid syntax (attempt {attempt+1})")

            except Exception as e:
                last_error = e
                print(f"[WARNING] {name} failed (attempt {attempt + 1}): {e}")

            time.sleep(1)

        print(f"[INFO] Switching from {name} to next provider...")

    raise RuntimeError(f"All providers failed or returned invalid code. Last error: {last_error}")