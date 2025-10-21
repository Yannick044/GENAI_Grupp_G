from langchain.tools import tool

# wird in main.py gesetzt
_vectorstore = None

def set_vectorstore(vs):  # kleiner Setter statt Globals direkt
    global _vectorstore
    _vectorstore = vs

@tool("faq_suche")
def faq_suche(frage: str) -> str:
    """Suche in lokalen FAQ-Docs und gib relevanten Kontext + Quellen zurück."""
    if not _vectorstore:
        return "FAQ-Index nicht geladen."
    retriever = _vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 8, "fetch_k": 24, "lambda_mult": 0.5}
    )
    docs = retriever.get_relevant_documents(frage)
    if not docs:
        return "Keine passenden FAQ-Passagen gefunden."
    ctx = "\n\n".join(d.page_content for d in docs[:6])
    srcs, seen = [], set()
    for d in docs:
        s = d.metadata.get("source")
        if s and s not in seen:
            srcs.append(s); seen.add(s)
        if len(srcs) == 3: break
    return f"Kontext:\n{ctx}\n\nQuellen:\n" + "\n".join(f"- {s}" for s in srcs)

@tool("preis_check")
def preis_check(produkt: str) -> str:
    """Demo-Tool: Preis/Verfügbarkeit (später echte API)."""
    demo = {"macbook": "CHF 2799 (online lagernd)",
            "sony wh-1000xm5": "CHF 299 (Filialen Basel/Zürich)"}
    for k, v in demo.items():
        if k in produkt.lower():
            return f"{produkt.title()}: {v}"
    return "Keine Demo-Preisinfo gefunden."
