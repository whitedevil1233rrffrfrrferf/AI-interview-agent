from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

VECTOR_PATH = "vectorstore/faiss_index"


def load_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    return docs

def split_docs(docs):
    splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    return chunks

def get_embeddings():
    return OllamaEmbeddings(model="nomic-embed-text")

def create_vectorstore(chunks):
    embeddings = get_embeddings()

    db = FAISS.from_documents(chunks, embeddings)

    db.save_local(VECTOR_PATH)
    return db


def load_vectorstore():
    embeddings = get_embeddings()

    return FAISS.load_local(
        VECTOR_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )


def retrieve_context(query: str, k: int = 4):
    db = load_vectorstore()

    docs = db.similarity_search(query, k=k)

    return "\n".join([d.page_content for d in docs])
