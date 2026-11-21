import { createBrowserRouter } from "react-router";

import PlaceholderPage from "../components/PlaceholderPage";
import AppLayout from "../layout/AppLayout";
import HomePage from "../pages/home/HomePage";
import LoginPage from "../pages/login/LoginPage";
import ProtectedRoute from "../auth/ProtectedRoute";

export const router = createBrowserRouter([
  {
    path: "/login",
    element: <LoginPage />,
  },

  {
    path: "/",
    element: (
      <ProtectedRoute>
        <AppLayout />
      </ProtectedRoute>
      ),
    children: [
      {
        index: true,
        element: <HomePage />,
      },
      {
        path: "customers",
        element: <PlaceholderPage title="Clientes" />,
      },
      {
        path: "suppliers",
        element: <PlaceholderPage title="Proveedores" />,
      },
      {
        path: "quotations",
        element: <PlaceholderPage title="Cotizaciones" />,
      },
      {
        path: "orders",
        element: <PlaceholderPage title="Órdenes" />,
      },
      {
        path: "expenses",
        element: <PlaceholderPage title="Gastos" />,
      },
      {
        path: "invoices",
        element: <PlaceholderPage title="Facturas" />,
      },
      {
        path: "documents",
        element: <PlaceholderPage title="Documentos" />,
      },
      {
        path: "users",
        element: <PlaceholderPage title="Usuarios" />,
      },
    ],
  },
]);