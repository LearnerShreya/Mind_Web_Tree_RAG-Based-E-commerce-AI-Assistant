import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


def get_llm():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Check your .env file.")

    return ChatGroq(
        api_key=api_key,
        model_name="mixtral-8x7b-32768",
        temperature=0.3
    )



def generate_response(query, docs):
    try:
        # Initialize LLM
        llm = get_llm()

        # Prepare context safely
        if not docs:
            return "No matching products found."

        context = "\n\n".join([
            doc.page_content for doc in docs if doc.page_content
        ])

        if not context.strip():
            return "No useful product information available."

        # Prompt
        prompt = f"""
You are an intelligent e-commerce assistant.

Rules:
- Only use the provided context
- Do NOT hallucinate
- Be concise and helpful
- If no relevant product, say "No matching product found"

Context:
{context}

User Query:
{query}

Answer:
"""

        # Call LLM
        response = llm.invoke(prompt)

        # Safe return
        if hasattr(response, "content"):
            return response.content.strip()

        return "Unable to generate response."

    except Exception as e:
        # Debug print in terminal
        print("❌ LLM ERROR:", str(e))

        # Fallback
        return "⚠️ AI response failed. Showing best available product matches."