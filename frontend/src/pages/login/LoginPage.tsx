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
import {
  Visibility,
  VisibilityOff,
} from "@mui/icons-material";

import {
  IconButton,
  InputAdornment,
} from "@mui/material";


export default function LoginPage() {
  const { refreshUser } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] =
    useState("");
    const [showPassword, setShowPassword] =
  useState(false);
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
            type={showPassword ? "text" : "password"}
            value={password}
            onChange={(event) =>
              setPassword(event.target.value)
            }
            fullWidth
            required
            sx={{ mb: 3 }}
            slotProps={{
              input: {
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      onClick={() =>
                        setShowPassword(
                          (current) => !current,
                        )
                      }
                      edge="end"
                      aria-label={
                        showPassword
                          ? "Ocultar contraseña"
                          : "Mostrar contraseña"
                      }
                    >
                      {showPassword
                        ? <VisibilityOff />
                        : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              },
            }}
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