const BASE_URL = "http://localhost:8000/api";

export async function fetchPlaylists() {
  const res = await fetch(`${BASE_URL}/playlists`);
  return res.json();
}
