import type { CurrentUser } from "./types";
import { apiRequest } from "../api/apiClient";

const API_URL = "http://127.0.0.1:8000";


export async function login(
  email: string,
  password: string,
): Promise<string> {
  const form = new URLSearchParams();

  form.append("username", email);
  form.append("password", password);

  const response = await fetch(
    `${API_URL}/auth/login`,
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/x-www-form-urlencoded",
      },

      body: form,
    },
  );

  if (!response.ok) {
    throw new Error(
      "Correo o contraseña incorrectos",
    );
  }

  const data = await response.json();

  return data.access_token;
}

export async function getCurrentUser(): Promise<CurrentUser> {
  const response = await apiRequest(
    "/auth/me",
  );

  if (!response.ok) {
    throw new Error(
      "No se pudo obtener el usuario actual",
    );
  }

  return response.json();
}