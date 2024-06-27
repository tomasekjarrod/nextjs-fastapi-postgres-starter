"use client";

import { FormEvent, useEffect, useState } from "react";
import { API_URL } from "./constants";

export default function ChatThread({
  threadId,
  userId,
}: {
  threadId: number;
  userId: number;
}) {
  const [messages, setMessages] = useState<Array<ChatThreadMessage>>([]);
  const [input, setInput] = useState("");

  const fetchMessages = async () => {
    const messages = await fetch(
      `${API_URL}/thread_messages?thread_id=${threadId}`
    ).then((res) => res.json());

    setMessages(messages);
  };

  useEffect(() => {
    fetchMessages();
  }, [threadId]);

  const sendMessage = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const message: ChatThreadMessage = {
      content: input,
      sender_id: userId,
      thread_id: threadId,
    };

    // Push message before Promise resolves for better UX
    setMessages((prevValue) => [...prevValue, message]);
    setInput("");

    fetch(`${API_URL}/thread_messages_with_ai`, {
      method: "POST",
      body: JSON.stringify(message),
      headers: { "Content-Type": "application/json" },
    })
      .then((res) => res.json())
      .then((aiMessage) => {
        setMessages((prevValue) => [...prevValue, aiMessage]);
      });
  };

  return (
    <div className="flex flex-col gap-4">
      <div className="h-96 overflow-y-auto p-2 border-b border-gray-200">
        {messages.length === 0 && <p>Send your first message</p>}
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${
              message.sender_id !== null ? "justify-end" : "justify-start"
            } mb-2`}
          >
            <div
              className={`max-w-xs rounded-lg px-4 py-2 ${
                message.sender_id !== null
                  ? "bg-blue-500 text-white"
                  : "bg-gray-200 text-gray-800"
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}
      </div>
      <form onSubmit={sendMessage}>
        <div className="mb-4">
          <label
            className="block text-gray-700 text-sm font-bold mb-2"
            htmlFor="message"
          >
            Message
          </label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="message"
            type="text"
            placeholder="Enter your message"
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
        </div>
        <div className="mb-6 text-center">
          <button
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="submit"
          >
            Submit
          </button>
        </div>
      </form>
    </div>
  );
}
