import os

from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from modules.gemini_client import generate_response

DOCS_PATH = "data/medical_docs"
DB_PATH = "data/vector_db"


def load_documents():
    documents = []

    if not os.path.exists(DOCS_PATH):
        os.makedirs(DOCS_PATH)

    for filename in os.listdir(DOCS_PATH):
        if filename.endswith(".txt"):
            file_path = os.path.join(DOCS_PATH, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

            documents.append(
                Document(
                    page_content=text,
                    metadata={"source": filename}
                )
            )

    return documents


def create_vector_db():
    documents = load_documents()

    if not documents:
        return "No medical documents found. Please add .txt files inside data/medical_docs."

    splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.from_documents(chunks, embeddings)

    if not os.path.exists(DB_PATH):
        os.makedirs(DB_PATH)

    db.save_local(DB_PATH)

    return "Medical knowledge base created successfully."


def load_vector_db():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.load_local(
        DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return db


def rag_answer(question):
    db = load_vector_db()

    docs = db.similarity_search(question, k=3)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are HealthLens AI, a safe healthcare assistant.

Use the trusted medical context below to answer the user question.

Trusted Context:
{context}

User Question:
{question}

Answer format:
1. Simple Answer
2. Relevant Medical Information
3. Precautions
4. When to See a Doctor

Rules:
- Use only the provided context where possible.
- Do not give final diagnosis.
- Do not prescribe medicines.
- Keep answer simple.
"""

    answer = generate_response(prompt)

    sources = []

    for doc in docs:
        source = doc.metadata.get("source", "Unknown source")

        if source not in sources:
            sources.append(source)

    source_text = "\n".join(
        [f"- {source}" for source in sources]
    )

    final_answer = f"""
{answer}

---

Sources Used:
{source_text}
"""

    return final_answer