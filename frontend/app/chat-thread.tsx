"use client";

import { useEffect, useState } from "react";
import { API_URL } from "./constants";

export default function ChatThread({ threadId }: { threadId: number }) {
  const [messages, setMessages] = useState<Array<ThreadMessage>>([]);

  const fetchMessages = async () => {
    const messages = await fetch(
      `${API_URL}/thread_messages?thread_id=${threadId}`
    ).then((res) => res.json());

    setMessages(messages);
  };

  useEffect(() => {
    fetchMessages();
  }, [threadId]);

  return (
    <div className="flex flex-col">
      <form>
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
