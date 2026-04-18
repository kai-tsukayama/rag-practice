from pathlib import Path
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "data" / "chroma_db"
COLLECTION_NAME = "company_rules"

def main() -> None:
    question = "有給休暇について教えてください。"

    print("埋め込みモデルを準備")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    print("Chromaに接続")
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )

    print("Retrieverを作成")
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    print("関連文書を検索")
    docs = retriever.invoke(question)

    if not docs:
        print("関連文書が見つかりませんでした。")
        return

    context = "\n\n".join([doc.page_content for doc in docs])

    print("回答生成モデルを準備")
    llm = ChatOllama(model="phi3")

    prompt = f"""あなたは就業規則の内容を回答するアシスタントです。
    以下の文脈だけを使って質問に答えてください。
    文脈に書かれていないことは、分からないと答えてください。

    [文脈]
    {context}

    [質問]
    {question}
    """

    print("回答を生成")
    response = llm.invoke(prompt)

    print("\n=== 質問 ===")
    print(question)

    print("\n=== 検索結果 ===")
    for i, doc in enumerate(docs, start=1):
        print(f"\n--- chunk {i} ---")
        print(doc.page_content)

    print("\n=== 回答 ===")
    print(response.content)


if __name__ == "__main__":
    main()