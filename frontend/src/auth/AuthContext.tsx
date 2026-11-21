import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";

import {
  getCurrentUser,
} from "./authApi";

import type {
  CurrentUser,
} from "./types";


type AuthContextValue = {
  user: CurrentUser | null;
  loading: boolean;
  refreshUser: () => Promise<void>;
  logout: () => void;
};


const AuthContext =
  createContext<AuthContextValue | null>(null);


export function AuthProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [user, setUser] =
    useState<CurrentUser | null>(null);

  const [loading, setLoading] =
    useState(true);


  async function refreshUser() {
    const token =
      localStorage.getItem("access_token");

    if (!token) {
      setUser(null);
      setLoading(false);
      return;
    }

    try {
      const currentUser =
        await getCurrentUser();

      setUser(currentUser);
    } catch {
      localStorage.removeItem(
        "access_token",
      );

      setUser(null);
    } finally {
      setLoading(false);
    }
  }


  function logout() {
    localStorage.removeItem(
      "access_token",
    );

    setUser(null);
  }


  useEffect(() => {
    refreshUser();
  }, []);


  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        refreshUser,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}


export function useAuth() {
  const context =
    useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useAuth must be used inside AuthProvider",
    );
  }

  return context;
}