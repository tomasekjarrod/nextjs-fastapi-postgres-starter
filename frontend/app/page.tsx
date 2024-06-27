const apiUrl = process.env.NEXT_PUBLIC_API_URL;

export default async function Home() {
  console.log("fetch", `${apiUrl}/users/me`);
  const user: User = await fetch(`${apiUrl}/users/me`).then((res) =>
    res.json()
  );

  return (
    <main className="flex min-h-screen flex-col items-center pt-24">
      Hello, {user.name}!
      <div className="flex flex-row gap-6">
        <div className="flex flex-col gap-2">
          <button
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="button"
          >
            Start new thread
          </button>
          <div className="flex justify-center items-center bg-white shadow-md rounded px-8 pt-6 pb-8 ">
            Thread 1
          </div>
          <div className="flex justify-center items-center bg-white shadow-md rounded px-8 pt-6 pb-8 ">
            Thread 2
          </div>
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
