# rag-practice

LangChain + Chroma + Ollama を用いて、RAG（Retrieval-Augmented Generation）の基本構成を学習・検証するために作成したプロジェクトです。

本リポジトリは、RAGの基礎理解を目的として、以下の流れを一通り体験できるように構成しています。

- PDFを読み込む
- テキストをチャンクに分割する
- 埋め込みを生成する
- ベクトルDBに保存する
- 類似文書を検索する
- LLMに文脈を渡して回答を生成する
- API化する
- フロントエンドから質問できる形にする

## 完成系スクショ
<img width="1916" height="862" alt="スクリーンショット 2026-04-19 013630" src="https://github.com/user-attachments/assets/ec476707-143b-4bb3-b995-9fe3dea159c6" />

## 分かったこと
LLMが最終的に出した回答には、日本語の文章がどこかおかしいところが多く見られた。
この結果から、回答生成用に使用するLLMごとで回答精度が変わり、これは最終的なプロダクトの品質にも直結するところだと感じた。

## このプロジェクトの位置づけ

このプロジェクトは、実運用を前提とした完成品というよりも、**RAGの仕組みを理解しながら実装するための学習用プロジェクト**です。

そのため、以下のような目的を意識しています。

- LangChain を使ったRAG実装の流れを理解する
- Chroma を使ったベクトル検索の基本を学ぶ
- Ollama を使ったローカルLLM活用を試す
- Python バックエンドと Next.js フロントエンドの接続を確認する
- ローカル環境で完結する最小構成のRAGアプリを作る

## 使用技術

### バックエンド
- Python
- FastAPI
- LangChain
- Chroma
- Ollama

### フロントエンド
- Next.js
- TypeScript
- Tailwind CSS

### モデル
- 生成モデル: `phi3`
- 埋め込みモデル: `nomic-embed-text`

## 構成概要

```text
rag-practice/
├─ app/
│  ├─ ingest.py
│  ├─ query.py
│  └─ api.py
├─ data/
│  ├─ raw/
│  └─ chroma_db/
├─ frontend/
└─ requirements.txt
