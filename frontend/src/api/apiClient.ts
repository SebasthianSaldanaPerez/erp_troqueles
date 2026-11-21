const API_URL = "http://127.0.0.1:8000";

export async function apiRequest(
  path: string,
  options: RequestInit = {},
) {
  const token = localStorage.getItem("access_token");

  const headers = new Headers(options.headers);

  if (token) {
    headers.set(
      "Authorization",
      `Bearer ${token}`,
    );
  }

  const response = await fetch(
    `${API_URL}${path}`,
    {
      ...options,
      headers,
    },
  );

  return response;
}