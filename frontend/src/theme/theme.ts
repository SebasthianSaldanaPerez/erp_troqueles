import { createTheme } from "@mui/material/styles";

export const theme = createTheme({
  palette: {
    mode: "light",

    background: {
      default: "#f4f5f7",
      paper: "#ffffff",
    },

    primary: {
      main: "#5f6b76",
    },

    text: {
      primary: "#25282b",
      secondary: "#6b7280",
    },

    divider: "#e3e6e8",

    success: {
      main: "#5f7d68",
    },

    error: {
      main: "#a65d5d",
    },

    warning: {
      main: "#a67c52",
    },
  },

  typography: {
    fontFamily: [
      "Inter",
      "Roboto",
      "Arial",
      "sans-serif",
    ].join(","),

    fontSize: 15,

    h1: {
      fontSize: "2rem",
      fontWeight: 600,
    },

    h2: {
      fontSize: "1.5rem",
      fontWeight: 600,
    },

    h3: {
      fontSize: "1.2rem",
      fontWeight: 600,
    },

    button: {
      textTransform: "none",
      fontWeight: 500,
    },
  },

  shape: {
    borderRadius: 8,
  },

  components: {
    MuiButton: {
      defaultProps: {
        disableElevation: true,
      },
    },

    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: "none",
        },
      },
    },
  },
});