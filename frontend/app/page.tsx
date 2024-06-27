"use client";

import { useEffect, useState } from "react";

const apiUrl = process.env.NEXT_PUBLIC_API_URL;

export default function Home() {
  const [user, setUser] = useState<null | User>(null);
  const [threads, setThreads] = useState<Array<Thread>>([]);
  const [selectedThread, setSelectedThread] = useState<Thread | null>(null);

  const fetchUser = async () => {
    const user: User = await fetch(`${apiUrl}/users/me`).then((res) =>
      res.json()
    );

    setUser(user);
  };

  const fetchThreads = async () => {
    const threads: Thread[] = await fetch(`${apiUrl}/threads`).then((res) =>
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
      <p>Hello, {user !== null && <span>{user.name}</span>}</p>
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
      </div>
    </main>
  );
}
