import os

from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END

api_key = os.getenv("GEMINI_API_KEY")

print("Gemini key loaded:", bool(api_key))
print("Gemini key length:", len(api_key) if api_key else 0)

class ChatState(TypedDict):
    message: str
    response: str


if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is missing. Check your .env file."
    )
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0,
    google_api_key=api_key,
)


def chatbot_node(state: ChatState):

    message = state["message"]

    result = llm.invoke(message)

    content = result.content

    # Gemini/LangChain may return structured content
    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, dict):
                if item.get("type") == "text":
                    text_parts.append(
                        item.get("text", "")
                    )

        content = "\n".join(text_parts)

    return {
        "response": content
    }


builder = StateGraph(ChatState)

builder.add_node("chatbot", chatbot_node)

builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile()


