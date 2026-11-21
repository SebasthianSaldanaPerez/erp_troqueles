import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
} from "@mui/material";

export default function HomePage() {
  return (
    <Box>
      <Typography variant="h1" sx={{ mb: 1 }}>
        Bienvenido
      </Typography>

      <Typography
        color="text.secondary"
        sx={{ mb: 4 }}
      >
        Sistema de gestión de Troqueles
      </Typography>

      <Grid container spacing={2}>
        <Grid size={{ xs: 12, md: 4 }}>
          <Card variant="outlined">
            <CardContent>
              <Typography
                color="text.secondary"
                gutterBottom
              >
                Usuario
              </Typography>

              <Typography variant="h3">
                Sebasthian
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, md: 4 }}>
          <Card variant="outlined">
            <CardContent>
              <Typography
                color="text.secondary"
                gutterBottom
              >
                Rol
              </Typography>

              <Typography variant="h3">
                Administrador
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}