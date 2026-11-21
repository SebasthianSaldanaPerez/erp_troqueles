import React from "react";
import ReactDOM from "react-dom/client";
import { AuthProvider } from "./auth/AuthContext";

import {
  CssBaseline,
  ThemeProvider,
} from "@mui/material";

import { RouterProvider } from "react-router/dom";

import { router } from "./router/router";
import { theme } from "./theme/theme";

ReactDOM.createRoot(
  document.getElementById("root")!,
).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />

      <AuthProvider>
        <RouterProvider router={router} />
      </AuthProvider>
    </ThemeProvider>
  </React.StrictMode>
);