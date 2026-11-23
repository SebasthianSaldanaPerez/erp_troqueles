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
  Typography,
} from "@mui/material";

import ArrowBackOutlined from "@mui/icons-material/ArrowBackOutlined";

import {
  useNavigate,
  useParams,
} from "react-router";

import Snackbar from "@mui/material/Snackbar";

import {
  deactivateSupplier,
  getSupplier,
  reactivateSupplier,
} from "./suppliersApi";

import { useAuth } from "../../auth/AuthContext";

import type {
  Supplier,
} from "./types";

import EditOutlined from "@mui/icons-material/EditOutlined";

import EditSupplierDialog
  from "./EditSupplierDialog";

export default function SupplierDetailPage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const canEdit =
   user?.role === "ADMIN" ||
   user?.role === "OPERATOR";

  const [
    editDialogOpen,
    setEditDialogOpen,
    ] = useState(false);

  const [updatingStatus, setUpdatingStatus] =
  useState(false);
  
  const [successMessage, setSuccessMessage] =
  useState<string | null>(null);

  const { supplierId } = useParams();

  const [supplier, setSupplier] =
    useState<Supplier | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);


  async function loadSupplier() {
    if (!supplierId) {
      setError(
        "No se proporcionó un proveedor válido.",
      );

      setLoading(false);
      return;
    }

    try {
      setError(null);

      const data =
        await getSupplier(
          supplierId,
        );

      setSupplier(data);

    } catch {
      setError(
        "No se pudo cargar la información del proveedor.",
      );
    } finally {
      setLoading(false);
    }
  }


  useEffect(() => {
    loadSupplier();
  }, [supplierId]);

async function handleStatusChange() {
  if (!supplier) {
    return;
  }

  setUpdatingStatus(true);
  setError(null);

  try {
    if (supplier.status === "ACTIVE") {
      await deactivateSupplier(
        supplier.id,
      );

      setSuccessMessage(
        "Proveedor desactivado correctamente.",
      );
    } else {
      await reactivateSupplier(
        supplier.id,
      );

      setSuccessMessage(
        "Proveedor reactivado correctamente.",
      );
    }

    await loadSupplier();

  } catch (error) {
    if (error instanceof Error) {
      setError(error.message);
    } else {
      setError(
        "No se pudo actualizar el estado del proveedor.",
      );
    }
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


  if (error || !supplier) {
    return (
      <Alert severity="error">
        {error ??
          "Proveedor no encontrado."}
      </Alert>
    );
  }


  return (
    <Box>
      <Button
        startIcon={
          <ArrowBackOutlined />
        }
        color="inherit"
        onClick={() =>
          navigate("/suppliers")
        }
        sx={{ mb: 2 }}
      >
        Volver a proveedores
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
            supplier.status === "ACTIVE"
                ? "Activo"
                : "Inactivo"
            }
            color={
            supplier.status === "ACTIVE"
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
                Editar proveedor
            </Button>
            )}

        {canEdit && (
            <Button
            variant="outlined"
            color={
                supplier.status === "ACTIVE"
                ? "error"
                : "success"
            }
            disabled={updatingStatus}
            onClick={handleStatusChange}
            >
            {updatingStatus
                ? "Actualizando..."
                : supplier.status === "ACTIVE"
                ? "Desactivar proveedor"
                : "Reactivar proveedor"}
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
            label="Nombre"
            value={supplier.name}
          />

          <InfoItem
            label="RFC"
            value={supplier.rfc}
          />

          <InfoItem
            label="Contacto"
            value={
              supplier.contact_name
            }
          />

          <InfoItem
            label="Teléfono"
            value={supplier.phone}
          />

          <InfoItem
            label="Correo"
            value={supplier.email}
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

        {supplier.address ? (
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
              value={
                supplier.address.street
              }
            />

            <InfoItem
              label="Número exterior"
              value={
                supplier.address
                  .exterior_number
              }
            />

            <InfoItem
              label="Número interior"
              value={
                supplier.address
                  .interior_number
              }
            />

            <InfoItem
              label="Colonia"
              value={
                supplier.address
                  .neighborhood
              }
            />

            <InfoItem
              label="Ciudad"
              value={
                supplier.address.city
              }
            />

            <InfoItem
              label="Estado"
              value={
                supplier.address.state
              }
            />

            <InfoItem
              label="Código postal"
              value={
                supplier.address
                  .postal_code
              }
            />

            <InfoItem
              label="País"
              value={
                supplier.address.country
              }
            />
          </Box>
        ) : (
          <Typography
            color="text.secondary"
          >
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
            supplier.notes
              ? "text.primary"
              : "text.secondary"
          }
        >
          {supplier.notes ??
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
        <EditSupplierDialog
        open={editDialogOpen}
        supplier={supplier}
        onClose={() =>
            setEditDialogOpen(false)
        }
        onUpdated={async () => {
            await loadSupplier();

            setSuccessMessage(
            "Proveedor actualizado correctamente.",
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