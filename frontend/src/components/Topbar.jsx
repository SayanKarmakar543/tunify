const Topbar = () => {
  const username = localStorage.getItem("username");

  return (
    <header className="h-16 bg-zinc-900 border-b border-zinc-800 flex items-center justify-between px-6">
      <h2 className="text-lg font-semibold text-white">
        Welcome back {username || "Guest"} 🎧
      </h2>

      <div className="flex items-center gap-4">
        <div className="w-9 h-9 rounded-full bg-green-500 flex items-center justify-center text-black font-bold">
          {username ? username[0].toUpperCase() : "U"}
        </div>
      </div>
    </header>
  );
};

export default Topbar;
