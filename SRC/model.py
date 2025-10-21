from langchain_openai import ChatOpenAI
from .config import BASE_URL, API_KEY, MODEL, TEMPERATURE

def get_chat_llm(temp: float | None = None) -> ChatOpenAI:
    return ChatOpenAI(
        base_url=BASE_URL,
        api_key=API_KEY,
        model=MODEL,
        temperature=TEMPATURE if (temp is None) else temp,
    )

# Tippfehler fix:
TEMPATURE = TEMPERATURE
