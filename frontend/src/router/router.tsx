import { createBrowserRouter } from "react-router";

import PlaceholderPage from "../components/PlaceholderPage";
import AppLayout from "../layout/AppLayout";
import HomePage from "../pages/home/HomePage";
import LoginPage from "../pages/login/LoginPage";
import ProtectedRoute from "../auth/ProtectedRoute";
import AdminRoute from "../auth/AdminRoute";
import CustomersPage from "../pages/customers/CustomersPage";
import CustomerDetailPage
  from "../pages/customers/CustomerDetailPage";
import SuppliersPage
  from "../pages/suppliers/SuppliersPage";
import SupplierDetailPage
  from "../pages/suppliers/SupplierDetailPage";
  

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
        element: <CustomersPage />,
      },
      {
        path: "customers/:customerId",
        element: <CustomerDetailPage />,
      },
      {
        path: "suppliers",
        element: <SuppliersPage />,
      },
      {
        path: "suppliers/:supplierId",
        element: <SupplierDetailPage />,
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
        element: (<AdminRoute>
          <PlaceholderPage title="Usuarios" />
        </AdminRoute>),
      },
    ],
  },
]);