import { useEffect, useState } from "react";

import {
  Alert,
  Box,
  Button,
  Chip,
  CircularProgress,
  Divider,
  IconButton,
  Paper,
  Snackbar,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";

import ArrowBackOutlined from "@mui/icons-material/ArrowBackOutlined";
import DescriptionOutlined from "@mui/icons-material/DescriptionOutlined";

import {
  useNavigate,
  useParams,
} from "react-router";

import { getCustomer } from "../customers/customersApi";

import {
  getOrder,
  type OrderDetail,
} from "./ordersApi";


import EditOutlined from "@mui/icons-material/EditOutlined";

import ReviseOrderItemDialog from "./ReviseOrderItemDialog";

import type { OrderItem } from "./ordersApi";

import { useAuth } from "../../auth/AuthContext";

import OrderRevisionsSection from "./OrderRevisionsSection";

export default function OrderDetailPage() {
    
  const navigate = useNavigate();
  
  const { orderId } = useParams();

  const [order, setOrder] =
    useState<OrderDetail | null>(null);

  const [customerName, setCustomerName] =
    useState("");

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  const [customerError, setCustomerError] =
    useState(false);
 
  const { user } = useAuth();

    const [selectedItem, setSelectedItem] =
    useState<OrderItem | null>(null);

    const [successMessage, setSuccessMessage] =
    useState<string | null>(null);

    const [refreshError, setRefreshError] =
    useState<string | null>(null);

    const canEdit =
    user?.role === "ADMIN" ||
    user?.role === "OPERATOR";

    const canRevise =
    canEdit &&
    (order?.status === "CREATED" ||
        order?.status === "IN_PROGRESS");

  useEffect(() => {
    let cancelled = false;

    async function loadOrder() {
      if (!orderId) {
        setError(
          "No se proporcionó una orden válida.",
        );
        setLoading(false);
        return;
      }

      setLoading(true);
      setError(null);
      setCustomerError(false);
      setCustomerName("");
      setOrder(null);

      try {
        const data = await getOrder(orderId);

        if (cancelled) return;

        setOrder(data);


        try {
          const customer = await getCustomer(
            data.customer_id,
          );

          if (!cancelled) {
            setCustomerName(customer.business_name);
          }
        } catch {
          if (!cancelled) {
            setCustomerError(true);
          }
        }

      } catch (err) {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "No se pudo cargar la orden.",
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadOrder();

    return () => {
      cancelled = true;
    };
  }, [orderId]);


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


  if (error || !order) {
    return (
      <Box>
        <Button
          startIcon={<ArrowBackOutlined />}
          onClick={() => navigate("/orders")}
          color="inherit"
          sx={{ mb: 2 }}
        >
          Volver a órdenes
        </Button>

        <Alert severity="error">
          {error ?? "Orden no encontrada."}
        </Alert>
      </Box>
    );
  }

  async function handleRevisionSaved() {
    if (!orderId) return;

    setSuccessMessage("Revisión registrada correctamente.");

    try {
        const updatedOrder = await getOrder(orderId);

        setOrder(updatedOrder);
        setRefreshError(null);
    } catch {
        setRefreshError(
        "La revisión se guardó, pero no se pudo actualizar la información. Recarga la página.",
        );
    }
    }

  return (
    <Box>
      <Button
        startIcon={<ArrowBackOutlined />}
        color="inherit"
        onClick={() => navigate("/orders")}
        sx={{ mb: 2 }}
      >
        Volver a órdenes
      </Button>


      <Box
        sx={{
          display: "flex",
          alignItems: "flex-start",
          justifyContent: "space-between",
          flexWrap: "wrap",
          gap: 2,
          mb: 3,
        }}
      >
        <Box>
          <Typography variant="h1">
            Orden de trabajo
          </Typography>

          <Typography
            color="text.secondary"
            sx={{
              mt: 0.5,
              overflowWrap: "anywhere",
            }}
          >
            {order.id}
          </Typography>
        </Box>

        <OrderStatusChip status={order.status} />
      </Box>


      <Paper
        variant="outlined"
        sx={{ p: 3, mb: 3 }}
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
              md: "repeat(3, 1fr)",
            },
            gap: 3,
          }}
        >
          <Box>
            <InfoItem
              label="Cliente"
              value={
                customerName ||
                (customerError
                  ? "No se pudo consultar el nombre"
                  : order.customer_id)
              }
            />

            <Button
              size="small"
              onClick={() =>
                navigate(
                  `/customers/${order.customer_id}`,
                )
              }
              sx={{ mt: 1, px: 0 }}
            >
              Ver cliente
            </Button>
          </Box>

          <InfoItem
            label="Moneda"
            value={order.currency}
          />

          <InfoItem
            label="Impuesto"
            value={`${order.tax_rate}%`}
          />

          <InfoItem
            label="Estado de facturación"
            value={
              getBillingStatusLabel(
                order.billing_status,
              )
            }
          />

          <InfoItem
            label="Número de revisiones"
            value={String(order.revision_number)}
          />

          <InfoItem
            label="Estado de la orden"
            value={getOrderStatusLabel(order.status)}
          />
        </Box>
      </Paper>


      {order.origin_quotation_id && (
        <Paper
          variant="outlined"
          sx={{ p: 3, mb: 3 }}
        >
          <Typography variant="h2">
            Cotización de origen
          </Typography>

          <Divider sx={{ my: 2 }} />

          <Typography
            color="text.secondary"
            sx={{
              mb: 2,
              overflowWrap: "anywhere",
            }}
          >
            {order.origin_quotation_id}
          </Typography>

          <Button
            startIcon={<DescriptionOutlined />}
            variant="outlined"
            color="inherit"
            onClick={() =>
              navigate(
                `/quotations/${order.origin_quotation_id}`,
              )
            }
          >
            Ver cotización original
          </Button>
        </Paper>
      )}


      <Paper
        variant="outlined"
        sx={{
          mb: 3,
          overflow: "hidden",
        }}
      >
        <Box sx={{ px: 3, py: 2 }}>
          <Typography variant="h2">
            Conceptos de la orden
          </Typography>
        </Box>

        <Divider />

        <Box sx={{ overflowX: "auto" }}>
          <Table sx={{ minWidth: 600 }}>
            <TableHead>
              <TableRow>
                <TableCell>
                  Descripción
                </TableCell>

                <TableCell align="right">
                  Cantidad
                </TableCell>

                <TableCell align="right">
                  Precio unitario
                </TableCell>

                <TableCell align="right">
                  Total
                </TableCell>
                {canRevise && (
                <TableCell align="center" sx={{ width: 110 }}>
                    Acciones
                </TableCell>
                )}
              </TableRow>
            </TableHead>

            <TableBody>
              {order.items.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={4}>
                    No hay conceptos registrados.
                  </TableCell>
                </TableRow>
              ) : (
                order.items.map((item) => (
                  <TableRow key={item.id}>
                    <TableCell>
                      {item.description}
                    </TableCell>

                    <TableCell align="right">
                      {item.quantity}
                    </TableCell>

                    <TableCell align="right">
                      {formatMoney(
                        item.unit_price,
                        item.currency,
                      )}
                    </TableCell>

                    <TableCell align="right">
                      {formatMoney(
                        item.total,
                        item.currency,
                      )}
                    </TableCell>
                    {canRevise && (
                    <TableCell align="center">
                        <IconButton
                        aria-label="Revisar concepto"
                        onClick={() => setSelectedItem(item)}
                        >
                        <EditOutlined />
                        </IconButton>
                    </TableCell>
                    )}
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </Box>
      </Paper>

      <Paper
        variant="outlined"
        sx={{ p: 3 }}
      >
        <Box
          sx={{
            display: "flex",
            justifyContent: "flex-end",
          }}
        >
          <Box
            sx={{
              width: {
                xs: "100%",
                sm: 340,
              },
            }}
          >
            <SummaryRow
              label="Subtotal"
              value={order.subtotal}
              currency={order.currency}
            />

            <SummaryRow
              label="Impuesto"
              value={order.tax}
              currency={order.currency}
            />

            <Divider sx={{ my: 1 }} />

            <SummaryRow
              label="Total de la orden"
              value={order.total}
              currency={order.currency}
              strong
            />
          </Box>
        </Box>
      </Paper>
      <ReviseOrderItemDialog
        open={Boolean(selectedItem)}
        orderId={order.id}
        item={selectedItem}
        onClose={() => setSelectedItem(null)}
        onSaved={() => {
            void handleRevisionSaved();
        }}
        />

        {refreshError && (
        <Alert severity="warning" sx={{ mt: 2 }}>
            {refreshError}
        </Alert>
        )}

        <Snackbar
                open={Boolean(successMessage)}
                autoHideDuration={3500}
                onClose={() => setSuccessMessage(null)}
                message={successMessage}
                />
                <OrderRevisionsSection
        orderId={order.id}
        revisionNumber={order.revision_number}
        />
    </Box>
  );
}



function InfoItem({
  label,
  value,
}: {
  label: string;
  value: string;
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

      <Typography sx={{ fontWeight: 500 }}>
        {value}
      </Typography>
    </Box>
  );
}


function SummaryRow({
  label,
  value,
  currency,
  strong = false,
}: {
  label: string;
  value: string;
  currency: string;
  strong?: boolean;
}) {
  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "space-between",
        gap: 2,
        py: 0.5,
      }}
    >
      <Typography
        color={
          strong
            ? "text.primary"
            : "text.secondary"
        }
        sx={{
          fontWeight: strong ? 700 : 400,
        }}
      >
        {label}
      </Typography>

      <Typography
        sx={{
          fontWeight: strong ? 700 : 500,
          whiteSpace: "nowrap",
        }}
      >
        {formatMoney(value, currency)}
      </Typography>
    </Box>
  );
}


function formatMoney(
  value: string,
  currency: string,
): string {
  return `${currency} ${Number(value).toLocaleString(
    "es-MX",
    {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    },
  )}`;
}


function getOrderStatusLabel(
  status: string,
): string {
  const labels: Record<string, string> = {
    CREATED: "Creada",
  };

  return labels[status] ?? status;
}


function getBillingStatusLabel(
  status: string,
): string {
  const labels: Record<string, string> = {
    NOT_INVOICED: "No facturada",
    PARTIALLY_INVOICED: "Parcialmente facturada",
    FULLY_INVOICED: "Totalmente facturada",
  };

  return labels[status] ?? status;
}


function OrderStatusChip({
  status,
}: {
  status: string;
}) {
  return (
    <Chip
      label={getOrderStatusLabel(status)}
      color="default"
      variant="outlined"
    />
  );
}