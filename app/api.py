from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "data" / "chroma_db"
COLLECTION_NAME = "company_rules"

app = FastAPI(title="Local RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    contexts: list[str]


def build_rag_chain(question: str) -> tuple[str, list[str]]:
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(question)

    contexts = [doc.page_content for doc in docs]
    context_text = "\n\n".join(contexts)

    llm = ChatOllama(model="phi3")

    prompt = f"""あなたは就業規則の内容を回答するアシスタントです。
    以下の文脈だけを使って質問に答えてください。
    文脈に書かれていないことは、分からないと答えてください。
    回答は日本語で簡潔かつ分かりやすくしてください。

    [文脈]
    {context_text}

    [質問]
    {question}
    """

    response = llm.invoke(prompt)
    return response.content, contexts


@app.get("/")
def health_check() -> dict[str, str]:
    return {"message": "Local RAG API is running"}


@app.post("/api/query", response_model=QueryResponse)
def query_rag(request: QueryRequest) -> QueryResponse:
    answer, contexts = build_rag_chain(request.question)
    return QueryResponse(
        answer=answer,
        contexts=contexts
        )