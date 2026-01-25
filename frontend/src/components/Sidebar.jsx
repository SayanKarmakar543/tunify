import { useNavigate } from "react-router-dom";

const Sidebar = () => {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <aside className="w-64 bg-zinc-950 border-r border-zinc-800 p-6 flex flex-col">
      {/* Logo */}
      <h1 className="text-2xl font-bold text-green-500 mb-10">
        🎵 Tunify
      </h1>

      {/* Navigation */}
      <nav className="flex-1 space-y-2">
        <button
          onClick={() => navigate("/dashboard")}
          className="w-full text-left px-4 py-2 rounded-lg text-gray-300 hover:bg-zinc-800 hover:text-white transition"
        >
          Home
        </button>

        <button className="w-full text-left px-4 py-2 rounded-lg text-gray-300 hover:bg-zinc-800 hover:text-white transition">
          Playlists
        </button>

        <button className="w-full text-left px-4 py-2 rounded-lg text-gray-300 hover:bg-zinc-800 hover:text-white transition">
          Favorites
        </button>

        <button
          onClick={() => navigate("/ai-discovery")}
          className="w-full text-left px-4 py-2 rounded-lg text-gray-300 hover:bg-zinc-800 hover:text-white transition"
        >
          AI Discovery
        </button>

      </nav>

      {/* Logout */}
      <button
        onClick={logout}
        className="mt-6 px-4 py-2 rounded-lg bg-red-500/10 text-red-400 hover:bg-red-500/20 transition"
      >
        Logout
      </button>
    </aside>
  );
};

export default Sidebar;
