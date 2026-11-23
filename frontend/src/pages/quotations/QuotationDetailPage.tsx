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
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";

import ArrowBackOutlined from "@mui/icons-material/ArrowBackOutlined";

import {
  useNavigate,
  useParams,
} from "react-router";

import {
  getQuotation,
  sendQuotation,
} from "./quotationsApi";

import {
  getCustomer,
} from "../customers/customersApi";

import EditOutlined
  from "@mui/icons-material/EditOutlined";

import IconButton
  from "@mui/material/IconButton";

import EditQuotationItemDialog
  from "./EditQuotationItemDialog";

import type {
  Quotation,
  QuotationItem,
} from "./types";

import { useAuth }
  from "../../auth/AuthContext";



export default function QuotationDetailPage() {
  const navigate = useNavigate();
  
  const [updatingStatus, setUpdatingStatus] =
  useState(false);

  const [successMessage, setSuccessMessage] =
  useState<string | null>(null);

  const { user } = useAuth();

  const canEdit =
  user?.role === "ADMIN" ||
  user?.role === "OPERATOR";

  const [
  selectedItem,
  setSelectedItem,
] = useState<QuotationItem | null>(
  null,
);

  const { quotationId } = useParams();

  const [quotation, setQuotation] =
    useState<Quotation | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [customerName, setCustomerName] =
    useState("");

  const [error, setError] =
    useState<string | null>(null);


  async function loadQuotation() {
  if (!quotationId) {
    setError(
      "No se proporcionó una cotización válida.",
    );

    setLoading(false);
    return;
  }

  try {
    setError(null);

    const data =
      await getQuotation(
        quotationId,
      );

    setQuotation(data);

    const customer =
      await getCustomer(
        data.customer_id,
      );

    setCustomerName(
      customer.business_name,
    );

  } catch {
    setError(
      "No se pudo cargar la cotización.",
    );
  } finally {
    setLoading(false);
  }
}


  useEffect(() => {
    loadQuotation();
  }, [quotationId]);

  async function handleSendQuotation() {
  if (!quotation) {
    return;
  }

  setUpdatingStatus(true);
  setError(null);

  try {
    await sendQuotation(
      quotation.id,
    );

    await loadQuotation();

    setSuccessMessage(
      "Cotización enviada correctamente.",
    );

  } catch (error) {
    if (error instanceof Error) {
      setError(
        error.message,
      );
    } else {
      setError(
        "No se pudo enviar la cotización.",
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


  if (error || !quotation) {
    return (
      <Alert severity="error">
        {error ??
          "Cotización no encontrada."}
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
          navigate("/quotations")
        }
        sx={{ mb: 2 }}
      >
        Volver a cotizaciones
      </Button>

      


        <Box
        sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-start",
            gap: 2,
            mb: 3,
        }}
        >
        <Box>
            <Typography variant="h1">
            Cotización
            </Typography>

            <Typography
            color="text.secondary"
            sx={{ mt: 0.5 }}
            >
            {quotation.id}
            </Typography>
        </Box>

        <Box
            sx={{
            display: "flex",
            alignItems: "center",
            gap: 1.5,
            }}
        >
            <QuotationStatusChip
            status={quotation.status}
            />

            {canEdit &&
            quotation.status === "DRAFT" && (
                <Button
                variant="contained"
                disabled={updatingStatus}
                onClick={handleSendQuotation}
                >
                {updatingStatus
                    ? "Enviando..."
                    : "Enviar cotización"}
                </Button>
            )}
        </Box>
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
              md: "repeat(3, 1fr)",
            },
            gap: 3,
          }}
        >
          <InfoItem
            label="Cliente"
            value={
              customerName
            }
          />

          <InfoItem
            label="Moneda"
            value={
              quotation.currency
            }
          />

          <InfoItem
            label="Impuesto"
            value={`${quotation.tax_rate}%`}
          />
        </Box>
      </Paper>


      <Paper
        variant="outlined"
        sx={{
          mb: 3,
          overflow: "hidden",
        }}
      >
        <Box
          sx={{
            px: 3,
            py: 2,
          }}
        >
          <Typography variant="h2">
            Conceptos
          </Typography>
        </Box>

        <Divider />

        <Table>
          <TableHead>
            <TableRow>
              <TableCell>
                Descripción
              </TableCell>

              <TableCell
                align="right"
              >
                Cantidad
              </TableCell>

              <TableCell
                align="right"
              >
                Precio unitario
              </TableCell>

              <TableCell
                align="right"
              >
                Total
              </TableCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {quotation.items.map(
              (item) => (
                <TableRow
                  key={item.id}
                >
                  <TableCell>
                    {
                      item.description
                    }
                  </TableCell>

                  <TableCell
                    align="right"
                  >
                    {
                      item.quantity
                    }
                  </TableCell>

                  <TableCell
                    align="right"
                  >
                    {quotation.currency}{" "}
                    {
                      item.unit_price
                    }
                  </TableCell>

                  <TableCell
                    align="right"
                  >
                    {quotation.currency}{" "}
                    {
                      item.total
                    }
                  </TableCell>
                  <TableCell>
                    {canEdit &&
                        quotation.status === "DRAFT" && (
                        <IconButton
                            size="small"
                            onClick={() =>
                            setSelectedItem(item)
                            }
                        >
                            <EditOutlined />
                        </IconButton>
                        )}
                    </TableCell>
                </TableRow>
              ),
            )}
          </TableBody>
        </Table>
      </Paper>


      <Paper
        variant="outlined"
        sx={{
          p: 3,
        }}
      >
        <Box
          sx={{
            display: "flex",
            justifyContent:
              "flex-end",
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
              value={
                quotation.subtotal
              }
              currency={
                quotation.currency
              }
            />

            <SummaryRow
              label="Impuesto"
              value={
                quotation.tax
              }
              currency={
                quotation.currency
              }
            />

            <Box
              sx={{
                borderTop:
                  "1px solid",

                borderColor:
                  "divider",

                mt: 1,
                pt: 1,
              }}
            >
              <SummaryRow
                label="Total"
                value={
                  quotation.total
                }
                currency={
                  quotation.currency
                }
                strong
              />
            </Box>
          </Box>
        </Box>
      </Paper>
      <EditQuotationItemDialog
        open={Boolean(selectedItem)}
        quotationId={quotation.id}
        item={selectedItem}
        onClose={() =>
            setSelectedItem(null)
        }
        onUpdated={loadQuotation}
        />
        <Snackbar
            open={Boolean(successMessage)}
            autoHideDuration={3000}
            onClose={() =>
                setSuccessMessage(null)
            }
            message={successMessage}
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

      <Typography
        sx={{
          fontWeight: 500,
        }}
      >
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
        justifyContent:
          "space-between",
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
          fontWeight:
            strong
              ? 700
              : 400,
        }}
      >
        {label}
      </Typography>

      <Typography
        sx={{
            fontWeight:
            strong
                ? 700
                : 500,
        }}
        >
        {currency}{" "}
        {Number(value).toLocaleString(
            "es-MX",
            {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
            },
        )}
        </Typography>
    </Box>
  );
}


function QuotationStatusChip({
  status,
}: {
  status: string;
}) {
  const labels: Record<string, string> = {
    DRAFT: "Borrador",
    SENT: "Enviada",
    ACCEPTED: "Aceptada",
    REJECTED: "Rechazada",
    CANCELLED: "Cancelada",
  };

  return (
    <Chip
      label={
        labels[status] ?? status
      }
      color={
        status === "ACCEPTED"
          ? "success"
          : status ===
                "REJECTED" ||
              status ===
                "CANCELLED"
            ? "error"
            : "default"
      }
      variant="outlined"
    />
  );
}