from langchain.agents import initialize_agent, AgentType
from langchain.prompts import ChatPromptTemplate


from .config import TEMPERATURE
from .model import get_chat_llm
from .prompts import SAFE_SYSTEM_PROMPT
from .safeguards import input_guard, output_guard
from .memory import build_memory
from .rag import load_local_docs, build_vectorstore
from .tools import faq_suche, preis_check, set_vectorstore

def build_agent():
    # RAG vorbereiten
    docs = load_local_docs("data/faq")
    vs = build_vectorstore(docs)
    set_vectorstore(vs)

    llm = get_chat_llm(temp=TEMPERATURE)
    memory = build_memory()
    tools = [faq_suche, preis_check]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=False,
    )
    # Safeguard-Systemprompt einsetzen (wie im Unterricht)
    agent.agent.llm_chain.prompt = ChatPromptTemplate.from_messages([
        ("system", SAFE_SYSTEM_PROMPT),
        ("human", "{input}"),
        ("ai", "{agent_scratchpad}")
    ])
    return agent

def ask(agent, user_msg: str) -> str:
    ok, reason = input_guard(user_msg)
    if not ok:
        return reason
    try:
        out = agent.run(user_msg)
    except Exception as e:
        out = f"Fehler: {e}"
    return output_guard(out)

if __name__ == "__main__":
    agent = build_agent()
    print("MediaMarkt FAQ Agent – tippe 'q' zum Beenden.")
    while True:
        q = input("> ")
        if q.strip().lower() in {"q", "quit", "exit"}:
            break
        print(ask(agent, q), "\n")
