import {
  AppBar,
  Box,
  Divider,
  Drawer,
  IconButton,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Tooltip,
  Typography,
} from "@mui/material";

import {
  AttachMoneyOutlined,
  DescriptionOutlined,
  HomeOutlined,
  Inventory2Outlined,
  LogoutOutlined,
  ManageAccountsOutlined,
  PeopleOutlined,
  ReceiptLongOutlined,
  RequestQuoteOutlined,
  StorefrontOutlined,
} from "@mui/icons-material";

import {
  NavLink,
  Outlet,
  useNavigate,
} from "react-router";

import { useAuth } from "../auth/AuthContext";


const drawerWidth = 240;


const navigation = [
  {
    label: "Inicio",
    path: "/",
    icon: <HomeOutlined />,
  },
  {
    label: "Clientes",
    path: "/customers",
    icon: <PeopleOutlined />,
  },
  {
    label: "Proveedores",
    path: "/suppliers",
    icon: <StorefrontOutlined />,
  },
  {
    label: "Cotizaciones",
    path: "/quotations",
    icon: <RequestQuoteOutlined />,
  },
  {
    label: "Órdenes",
    path: "/orders",
    icon: <Inventory2Outlined />,
  },
  {
    label: "Gastos",
    path: "/expenses",
    icon: <AttachMoneyOutlined />,
  },
  {
    label: "Facturas",
    path: "/invoices",
    icon: <ReceiptLongOutlined />,
  },
  {
    label: "Documentos",
    path: "/documents",
    icon: <DescriptionOutlined />,
  },
  {
    label: "Usuarios",
    path: "/users",
    icon: <ManageAccountsOutlined />,
  },
];


function getRoleLabel(
  role: string | undefined,
) {
  switch (role) {
    case "ADMIN":
      return "Administrador";

    case "OPERATOR":
      return "Operador";

    case "VIEWER":
      return "Consulta";

    default:
      return "";
  }
}


export default function AppLayout() {
  const navigate = useNavigate();

  const {
    user,
    logout,
  } = useAuth();


  function handleLogout() {
    logout();

    navigate(
      "/login",
      {
        replace: true,
      },
    );
  }


  return (
    <Box
      sx={{
        display: "flex",
        minHeight: "100vh",
      }}
    >
      <AppBar
        position="fixed"
        elevation={0}
        sx={{
          zIndex: (theme) =>
            theme.zIndex.drawer + 1,

          bgcolor: "#ffffff",
          color: "text.primary",

          borderBottom: "1px solid",
          borderColor: "divider",
        }}
      >
        <Toolbar>
          <Typography
            variant="h3"
            sx={{
              fontWeight: 700,
            }}
          >
            Troqueles ERP
          </Typography>

          <Box sx={{ flexGrow: 1 }} />

          <Box
            sx={{
              textAlign: "right",
            }}
          >
            <Typography
              sx={{
                fontSize: 14,
                fontWeight: 600,
              }}
            >
              {user?.name}
            </Typography>

            <Typography
              color="text.secondary"
              sx={{
                fontSize: 12,
              }}
            >
              {getRoleLabel(
                user?.role,
              )}
            </Typography>
          </Box>

          <Tooltip
            title="Cerrar sesión"
          >
            <IconButton
              onClick={
                handleLogout
              }
              sx={{
                ml: 2,
              }}
            >
              <LogoutOutlined />
            </IconButton>
          </Tooltip>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,

          "& .MuiDrawer-paper":
            {
              width: drawerWidth,

              boxSizing:
                "border-box",

              bgcolor:
                "#303438",

              color:
                "#ffffff",

              borderRight: 0,
            },
        }}
      >
        <Toolbar />

        <Box
          sx={{
            px: 1.5,
            py: 2,
          }}
        >
          <List disablePadding>
            {navigation.map(
              (item) => (
                <ListItemButton
                  key={
                    item.path
                  }
                  component={
                    NavLink
                  }
                  to={
                    item.path
                  }
                  sx={{
                    borderRadius:
                      1.5,

                    mb: 0.5,

                    color:
                      "#d5d8da",

                    "&:hover": {
                      bgcolor:
                        "rgba(255,255,255,0.08)",
                    },

                    "&.active":
                      {
                        bgcolor:
                          "rgba(255,255,255,0.12)",

                        color:
                          "#ffffff",
                      },
                  }}
                >
                  <ListItemIcon
                    sx={{
                      minWidth:
                        40,

                      color:
                        "inherit",
                    }}
                  >
                    {
                      item.icon
                    }
                  </ListItemIcon>

                  <ListItemText
                    primary={
                      item.label
                    }
                  />
                </ListItemButton>
              ),
            )}
          </List>
        </Box>

        <Box
          sx={{
            flexGrow: 1,
          }}
        />

        <Divider
          sx={{
            borderColor:
              "rgba(255,255,255,0.1)",
          }}
        />

        <Box
          sx={{
            p: 2,
          }}
        >
          <Typography
            sx={{
              fontSize: 12,

              color:
                "#9ca3a8",
            }}
          >
            Troqueles ERP · V1
          </Typography>
        </Box>
      </Drawer>

      <Box
        component="main"
        sx={{
          flexGrow: 1,

          bgcolor:
            "background.default",

          minHeight:
            "100vh",

          p: 3,
        }}
      >
        <Toolbar />

        <Outlet />
      </Box>
    </Box>
  );
}