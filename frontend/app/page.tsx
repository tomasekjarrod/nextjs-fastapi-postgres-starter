"use client";

import { useEffect, useState } from "react";
import ChatThread from "./chat-thread";
import { API_URL } from "./constants";

export default function Home() {
  const [user, setUser] = useState<null | User>(null);
  const [threads, setThreads] = useState<Array<Thread>>([]);
  const [selectedThread, setSelectedThread] = useState<Thread | null>(null);

  const fetchUser = async () => {
    const user: User = await fetch(`${API_URL}/users/me`).then((res) =>
      res.json()
    );

    setUser(user);
  };

  const fetchThreads = async () => {
    const threads: Thread[] = await fetch(`${API_URL}/threads`).then((res) =>
      res.json()
    );

    setThreads(threads);
  };

  // Fetch user & all threads on init
  useEffect(() => {
    fetchUser();
    fetchThreads();
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center pt-24">
      <h1>Hello, {user !== null && <span>{user.name}</span>}</h1>
      <div className="flex flex-row gap-6">
        <div className="flex flex-col gap-2">
          <button
            className="bg-blue-500 text-white font-bold py-2 px-4 rounded disabled opacity-50"
            type="button"
          >
            Start new thread
          </button>
          {threads.length !== 0 &&
            threads.map((thread) => {
              return (
                <div
                  key={thread.id}
                  onClick={() => setSelectedThread(thread)}
                  className="flex justify-center items-center bg-white shadow-md rounded px-8 pt-6 pb-8 cursor-pointer hover:bg-gray-100"
                >
                  Thread ID ({thread.id})
                </div>
              );
            })}
        </div>

        <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
          {selectedThread && <ChatThread threadId={selectedThread.id} />}
        </div>
      </div>
    </main>
  );
}
