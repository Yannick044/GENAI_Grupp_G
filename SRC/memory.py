from langchain.memory import ConversationSummaryBufferMemory
from .model import get_chat_llm

def build_memory():
    llm_summary = get_chat_llm(temp=0.1)  # deterministischer für Zusammenfassung
    return ConversationSummaryBufferMemory(
        llm=llm_summary,
        memory_key="chat_history",
        return_messages=True,
        max_token_limit=1000,
    )
