from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def ask_llm(context, question="", task="qa"):

    if task == "qa":
        prompt = f"""
Answer ONLY from context.
If not found, say: Not found.

Context:
{context}

Question:
{question}
"""

    elif task == "summary":
        prompt = f"Summarize clearly:\n{context}"

    elif task == "quiz":
        prompt = f"""
Create 5 MCQs from:
{context}

Format strictly:
Q1: question
A) ...
B) ...
C) ...
D) ...
Answer: X
"""

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )

    return response.choices[0].message.content