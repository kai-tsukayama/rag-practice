"use client";

import { useState } from "react";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function Home() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: input }),
      });

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.answer },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "エラーが発生しました" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex h-screen flex-col bg-[#fffdf7]">
      {/* Header */}
      <header className="border-b border-amber-100 bg-white/70 backdrop-blur px-6 py-4">
        <h1 className="text-lg font-semibold text-gray-800">
          Local RAG Chat
        </h1>
        <p className="text-xs text-gray-400">
          就業規則に質問できます
        </p>
      </header>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto px-6 py-6">
        <div className="mx-auto max-w-3xl space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-gray-400 mt-20">
              質問を入力してください
            </div>
          )}

          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${
                msg.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`
                  max-w-[70%] rounded-2xl px-4 py-3 text-sm leading-relaxed
                  ${
                    msg.role === "user"
                      ? "bg-blue-500 text-white"
                      : "bg-[#f6f3ea] text-gray-800 border border-amber-100"
                  }
                `}
              >
                {msg.content}
              </div>
            </div>
          ))}

          {loading && (
            <div className="text-sm text-amber-400">
              生成中...
            </div>
          )}
        </div>
      </div>

      {/* Input Area */}
      <div className="border-t border-amber-100 bg-white/80 backdrop-blur px-6 py-4">
        <div className="mx-auto flex max-w-3xl gap-3">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="質問を入力..."
            className="flex-1 rounded-xl border border-amber-200 bg-white px-4 py-3 text-sm outline-none focus:border-blue-400"
          />
          <button
            onClick={sendMessage}
            className="rounded-xl bg-blue-500 px-5 py-3 text-sm font-medium text-white hover:bg-blue-600"
          >
            送信
          </button>
        </div>
      </div>
    </main>
  );
}