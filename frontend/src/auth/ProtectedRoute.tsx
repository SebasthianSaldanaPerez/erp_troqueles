import {
  CircularProgress,
  Box,
} from "@mui/material";

import {
  Navigate,
} from "react-router";

import {
  useAuth,
} from "./AuthContext";


export default function ProtectedRoute({
  children,
}: {
  children: React.ReactNode;
}) {
  const {
    user,
    loading,
  } = useAuth();

  if (loading) {
    return (
      <Box
        sx={{
          minHeight: "100vh",
          display: "grid",
          placeItems: "center",
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  if (!user) {
    return (
      <Navigate
        to="/login"
        replace
      />
    );
  }

  return children;
}