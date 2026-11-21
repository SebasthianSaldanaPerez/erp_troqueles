import {
  Paper,
  Typography,
} from "@mui/material";

type Props = {
  title: string;
};

export default function PlaceholderPage({
  title,
}: Props) {
  return (
    <Paper
      variant="outlined"
      sx={{
        p: 3,
      }}
    >
      <Typography variant="h2">
        {title}
      </Typography>

      <Typography
        color="text.secondary"
        sx={{ mt: 1 }}
      >
        Módulo en construcción.
      </Typography>
    </Paper>
  );
}