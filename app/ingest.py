from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_PATH = BASE_DIR / "data" / "raw" / "sample_company_rules_jp_fixed.pdf"
CHROMA_DIR = BASE_DIR / "data" / "chroma_db"
COLLECTION_NAME = "company_rules"

def main() -> None:
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"PDFが見つかりません: {PDF_PATH}")
    
    print(f"PDFをロード中: {PDF_PATH}")
    loader = PyPDFLoader(str(PDF_PATH))
    documents = loader.load()
    print(f"読み込みページ数： {len(documents)}")

    print("テキストを分割中...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 100
    )
    split_docs = splitter.split_documents(documents)
    print(f"生成チャンク数： {len(split_docs)}")

    print(f" 埋め込みモデルを準備")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    print("Chromaに保存します")
    vectorstore = Chroma.from_documents(
        documents = split_docs,
        embedding = embeddings,
        persist_directory = str(CHROMA_DIR),
        collection_name = COLLECTION_NAME,
    )

    print("保存完了")
    print(f"保存先： {CHROMA_DIR}")
    print(f"コレクション名： {COLLECTION_NAME}")
    print(f"登録件数（概算）： {len(split_docs)}")

if __name__ == "__main__":
    main()
