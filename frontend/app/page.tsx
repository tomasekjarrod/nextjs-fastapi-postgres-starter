"use client";

import { useEffect, useState } from "react";
import ChatThread from "./components/chat-thread";
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
    // Set a default thread
    setSelectedThread(threads[0] || null);
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
          <h1 className="font-bold">Threads</h1>
          <hr />
          {threads.length !== 0 &&
            threads.map((thread) => {
              return (
                <div
                  key={thread.id}
                  onClick={() => setSelectedThread(thread)}
                  className={`flex justify-center items-center bg-white shadow-md rounded px-8 pt-6 pb-8 cursor-pointer hover:bg-gray-100
                    ${
                      selectedThread?.id === thread.id
                        ? "bg-blue-200 hover:bg-blue-100"
                        : ""
                    }`}
                >
                  Thread ID ({thread.id})
                </div>
              );
            })}
        </div>
        {selectedThread && user && (
          <div className="bg-white shadow-md rounded p-8">
            <ChatThread threadId={selectedThread.id} userId={user.id} />
          </div>
        )}
      </div>
    </main>
  );
}
