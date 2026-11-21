import { useState } from "react";

import {
  Alert,
  Box,
  Button,
  Paper,
  TextField,
  Typography,
} from "@mui/material";

import { useNavigate } from "react-router";

import { login } from "../../auth/authApi";
import { useAuth } from "../../auth/AuthContext";


export default function LoginPage() {
  const { refreshUser } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] =
    useState("");
  const [error, setError] =
    useState<string | null>(null);
  const [loading, setLoading] =
    useState(false);

  async function handleSubmit(
    event: React.FormEvent,
  ) {
    event.preventDefault();

    setError(null);
    setLoading(true);

    try {
      const token = await login(
        email,
        password,
      );

      localStorage.setItem(
        "access_token",
        token,
      );

      await refreshUser();

      navigate("/");
    } catch {
      setError(
        "Correo o contraseña incorrectos",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "grid",
        placeItems: "center",
        bgcolor: "background.default",
        p: 2,
      }}
    >
      <Paper
        variant="outlined"
        sx={{
          width: "100%",
          maxWidth: 420,
          p: 4,
        }}
      >
        <Typography
          variant="h1"
          sx={{
            fontSize: "1.7rem",
            mb: 1,
          }}
        >
          Troqueles ERP
        </Typography>

        <Typography
          color="text.secondary"
          sx={{ mb: 4 }}
        >
          Inicia sesión para continuar
        </Typography>

        {error && (
          <Alert
            severity="error"
            sx={{ mb: 2 }}
          >
            {error}
          </Alert>
        )}

        <Box
          component="form"
          onSubmit={handleSubmit}
        >
          <TextField
            label="Correo electrónico"
            type="email"
            value={email}
            onChange={(event) =>
              setEmail(event.target.value)
            }
            fullWidth
            required
            sx={{ mb: 2 }}
          />

          <TextField
            label="Contraseña"
            type="password"
            value={password}
            onChange={(event) =>
              setPassword(event.target.value)
            }
            fullWidth
            required
            sx={{ mb: 3 }}
          />

          <Button
            type="submit"
            variant="contained"
            fullWidth
            size="large"
            disabled={loading}
          >
            {loading
              ? "Ingresando..."
              : "Iniciar sesión"}
          </Button>
        </Box>
      </Paper>
    </Box>
  );
}