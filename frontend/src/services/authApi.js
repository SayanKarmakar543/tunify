const BASE_URL = "http://127.0.0.1:8000/api/v1";

export async function loginUser(username, password) {
  const body = new URLSearchParams({
    grant_type: "password",
    username: username,
    password: password,
    scope: "",
    client_id: "string",
    client_secret: "********",
  });

  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "accept": "application/json",
    },
    body: body.toString(),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Login failed");
  }

  return response.json();
}
