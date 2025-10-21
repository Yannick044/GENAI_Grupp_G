from langchain_community.document_loaders import DirectoryLoader, TextLoader, BSHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import faiss, os

def load_local_docs(data_dir: str = "data/faq"):
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir, exist_ok=True)
    # lädt .md und .html (wie in euren Unterrichtsbeispielen)
    md_loader   = DirectoryLoader(data_dir, glob="**/*.md",   loader_cls=TextLoader,   show_progress=True)
    html_loader = DirectoryLoader(data_dir, glob="**/*.html", loader_cls=BSHTMLLoader, show_progress=True)
    docs = md_loader.load() + html_loader.load()
    return docs

def build_vectorstore(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=120)
    splits = splitter.split_documents(docs)
    for d in splits:
        d.metadata["source"] = d.metadata.get("source") or d.metadata.get("file_path")
    emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    dim = len(emb.embed_query("probe"))
    index = faiss.IndexFlatIP(dim)
    vs = FAISS(embedding_function=emb, index=index, normalize_L2=True)
    if splits:
        vs.add_documents(splits)
    return vs
