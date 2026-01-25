const Dashboard = () => {
  return (
    <div className="space-y-8">
      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard title="Playlists" value="12" />
        <StatCard title="Liked Songs" value="89" />
        <StatCard title="Listening Time" value="42 hrs" />
      </div>

      {/* Recent Playlists */}
      <div>
        <h3 className="text-xl font-semibold mb-4">
          Your Playlists
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <PlaylistCard name="Chill Vibes" />
          <PlaylistCard name="Coding Beats" />
          <PlaylistCard name="Workout Mix" />
          <PlaylistCard name="Top Hits" />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

/* ---- Components inside same file ---- */

const StatCard = ({ title, value }) => (
  <div className="bg-zinc-800 rounded-xl p-6 hover:bg-zinc-700 transition">
    <p className="text-gray-400 text-sm">{title}</p>
    <h2 className="text-3xl font-bold mt-2">{value}</h2>
  </div>
);

const PlaylistCard = ({ name }) => (
  <div className="bg-zinc-800 rounded-xl p-4 hover:bg-zinc-700 transition cursor-pointer">
    <div className="h-32 bg-gradient-to-br from-green-500 to-emerald-700 rounded-lg mb-4" />
    <h4 className="font-semibold">{name}</h4>
    <p className="text-sm text-gray-400">Playlist</p>
  </div>
);
