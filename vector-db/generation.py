

from groq import Groq

#push
class Generator:
    SYSTEM_PROMPT = (
        "You are a knowledgeable assistant who helps people learn about "
        "Dark Psychology from a book. You give clear, well-organized, "
        "educational answers that anyone can understand.\n\n"

        "Your job:\n"
        "• If CONTEXT is provided, answer using ONLY that context.\n"
        "• If CONTEXT is empty ('[No relevant content found]'), "
        "reply with a SHORT 1-2 sentence message saying you couldn't find that, "
        "then list 2-3 suggested questions as simple bullets. "
        "No headers or long paragraphs for empty context.\n\n"

        "Style (for answers with context):\n"
        "• Use ## and ### headers to organize sections.\n"
        "• Use **bold** for key terms. Bullet points: **Term:** definition.\n"
        "• Clear, simple language. Short sentences.\n\n"

        "Rules:\n"
        "• Never mention 'context', 'threshold', 'score', or internal labels.\n"
        "• Never show numbers or technical metrics.\n"
        "• Speak as if you naturally know this material."
    )

    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    def get_response(self, context, query):
        ctx = context if context.strip() else "[No relevant content found]"
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": (
                    f"Context from the book:\n{ctx}\n\n"
                    f"Question: {query}\n\n"
                    f"Answer in clear, simple language."
                )},
            ],
        )
        return response.choices[0].message.content
