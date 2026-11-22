import {
  useEffect,
  useState,
} from "react";

import {
  Alert,
  Box,
  Button,
  Chip,
  CircularProgress,
  Divider,
  Paper,
  Snackbar,
  Typography,
} from "@mui/material";

import ArrowBackOutlined from "@mui/icons-material/ArrowBackOutlined";

import {
  useNavigate,
  useParams,
} from "react-router";

import {
  deactivateCustomer,
  getCustomer,
  reactivateCustomer,
} from "./customersApi";

import { useAuth } from "../../auth/AuthContext";

import type { Customer } from "./types";

import EditOutlined from "@mui/icons-material/EditOutlined";

import EditCustomerDialog
  from "./EditCustomerDialog";


export default function CustomerDetailPage() {
  const { user } = useAuth();

  const [
  editDialogOpen,
  setEditDialogOpen,
  ] = useState(false);

  const canEdit =
  user?.role === "ADMIN" ||
  user?.role === "OPERATOR";  

  const navigate = useNavigate();

  const { customerId } = useParams();

  const [customer, setCustomer] =
    useState<Customer | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  const [updatingStatus, setUpdatingStatus] =
  useState(false);

  const [successMessage, setSuccessMessage] =
  useState<string | null>(null);


async function loadCustomer() {
  if (!customerId) {
    setError(
      "No se proporcionó un cliente válido.",
    );
    setLoading(false);
    return;
  }

  try {
    setError(null);

    const data = await getCustomer(
      customerId,
    );

    setCustomer(data);
  } catch {
    setError(
      "No se pudo cargar la información del cliente.",
    );
  } finally {
    setLoading(false);
  }
}


useEffect(() => {
  loadCustomer();
}, [customerId]);

async function handleStatusChange() {
  if (!customer) {
    return;
  }

  setUpdatingStatus(true);
  setError(null);

  try {
    if (customer.status === "ACTIVE") {
      await deactivateCustomer(
        customer.id,
      );

      setSuccessMessage(
        "Cliente desactivado correctamente.",
      );
    } else {
      await reactivateCustomer(
        customer.id,
      );

      setSuccessMessage(
        "Cliente reactivado correctamente.",
      );
    }

    await loadCustomer();

  } catch {
    setError(
      "No se pudo actualizar el estado del cliente.",
    );
  } finally {
    setUpdatingStatus(false);
  }
}


  if (loading) {
    return (
      <Box
        sx={{
          display: "grid",
          placeItems: "center",
          minHeight: 300,
        }}
      >
        <CircularProgress />
      </Box>
    );
  }


  if (error || !customer) {
    return (
      <Alert severity="error">
        {error ?? "Cliente no encontrado."}
      </Alert>
    );
  }


  return (
    <Box>
      <Button
        startIcon={<ArrowBackOutlined />}
        color="inherit"
        onClick={() =>
          navigate("/customers")
        }
        sx={{ mb: 2 }}
      >
        Volver a clientes
      </Button>

      <Box
        sx={{
            display: "flex",
            alignItems: "center",
            gap: 1.5,
            mb: 3,
        }}
        >
        <Chip
            label={
            customer.status === "ACTIVE"
                ? "Activo"
                : "Inactivo"
            }
            color={
            customer.status === "ACTIVE"
                ? "success"
                : "default"
            }
            variant="outlined"
        />

        {canEdit && (
            <Button
                variant="contained"
                startIcon={<EditOutlined />}
                onClick={() =>
                setEditDialogOpen(true)
                }
            >
                Editar cliente
            </Button>
            )}

        {canEdit && (
            <Button
            variant="outlined"
            color={
                customer.status === "ACTIVE"
                ? "error"
                : "success"
            }
            disabled={updatingStatus}
            onClick={handleStatusChange}
            >
            {updatingStatus
                ? "Actualizando..."
                : customer.status === "ACTIVE"
                ? "Desactivar cliente"
                : "Reactivar cliente"}
            </Button>
        )}
        </Box>

      <Paper
        variant="outlined"
        sx={{
          p: 3,
          mb: 3,
        }}
      >
        <Typography variant="h2">
          Información general
        </Typography>

        <Divider sx={{ my: 2 }} />

        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: {
              xs: "1fr",
              md: "repeat(2, 1fr)",
            },
            gap: 3,
          }}
        >
          <InfoItem
            label="Razón social"
            value={customer.business_name}
          />

          <InfoItem
            label="RFC"
            value={customer.rfc}
          />

          <InfoItem
            label="Contacto"
            value={customer.contact_name}
          />

          <InfoItem
            label="Teléfono"
            value={customer.phone}
          />

          <InfoItem
            label="Correo"
            value={customer.email}
          />
        </Box>
      </Paper>

      <Paper
        variant="outlined"
        sx={{
          p: 3,
          mb: 3,
        }}
      >
        <Typography variant="h2">
          Dirección
        </Typography>

        <Divider sx={{ my: 2 }} />

        {customer.address ? (
          <Box
            sx={{
              display: "grid",
              gridTemplateColumns: {
                xs: "1fr",
                md: "repeat(2, 1fr)",
              },
              gap: 3,
            }}
          >
            <InfoItem
              label="Calle"
              value={customer.address.street}
            />

            <InfoItem
              label="Número exterior"
              value={
                customer.address.exterior_number
              }
            />

            <InfoItem
              label="Número interior"
              value={
                customer.address.interior_number
              }
            />

            <InfoItem
              label="Colonia"
              value={
                customer.address.neighborhood
              }
            />

            <InfoItem
              label="Ciudad"
              value={customer.address.city}
            />

            <InfoItem
              label="Estado"
              value={customer.address.state}
            />

            <InfoItem
              label="Código postal"
              value={
                customer.address.postal_code
              }
            />

            <InfoItem
              label="País"
              value={customer.address.country}
            />
          </Box>
        ) : (
          <Typography color="text.secondary">
            No hay dirección registrada.
          </Typography>
        )}
      </Paper>

      <Paper
        variant="outlined"
        sx={{
          p: 3,
        }}
      >
        <Typography variant="h2">
          Notas
        </Typography>

        <Divider sx={{ my: 2 }} />

        <Typography
          color={
            customer.notes
              ? "text.primary"
              : "text.secondary"
          }
        >
          {customer.notes ??
            "No hay notas registradas."}
        </Typography>
      </Paper>
      <Snackbar
        open={Boolean(successMessage)}
        autoHideDuration={3000}
        onClose={() =>
            setSuccessMessage(null)
        }
        message={successMessage}
        />
        <EditCustomerDialog
            open={editDialogOpen}
            customer={customer}
            onClose={() =>
                setEditDialogOpen(false)
            }
            onUpdated={async () => {
                await loadCustomer();

                setSuccessMessage(
                "Cliente actualizado correctamente.",
                );
            }}
            />
    </Box>
  );
}


function InfoItem({
  label,
  value,
}: {
  label: string;
  value: string | null;
}) {
  return (
    <Box>
      <Typography
        color="text.secondary"
        sx={{
          fontSize: 13,
          mb: 0.5,
        }}
      >
        {label}
      </Typography>

      <Typography
        sx={{
          fontWeight: 500,
        }}
      >
        {value ?? "—"}
      </Typography>
    </Box>
  );
}