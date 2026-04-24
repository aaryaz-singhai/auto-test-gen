import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_tests(function_name, function_code, context):
    prompt = f"""
You are a senior Python test engineer.

Write pytest unit tests for the following function.

Requirements:
- Cover edge cases
- Include invalid inputs
- Use pytest
- Keep tests clean and readable

Function:
{function_code}

Context:
{context}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content