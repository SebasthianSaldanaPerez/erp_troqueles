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

import AddOutlined
  from "@mui/icons-material/AddOutlined";

import ArrowBackOutlined
  from "@mui/icons-material/ArrowBackOutlined";

import DeleteOutlineOutlined
  from "@mui/icons-material/DeleteOutlineOutlined";

import EditOutlined
  from "@mui/icons-material/EditOutlined";

import {
  useNavigate,
  useParams,
} from "react-router";

import {
  useAuth,
} from "../../auth/AuthContext";

import {
  getCustomer,
} from "../customers/customersApi";

import AddQuotationItemDialog
  from "./AddQuotationItemDialog";

import EditQuotationItemDialog
  from "./EditQuotationItemDialog";

import {
  acceptQuotation,
  cancelQuotation,
  convertQuotationToOrder,
  getQuotation,
  rejectQuotation,
  removeQuotationItem,
  reopenQuotation,
  sendQuotation,
} from "./quotationsApi";

import type {
  Quotation,
  QuotationItem,
} from "./types";


export default function QuotationDetailPage() {
  const navigate = useNavigate();

  const { quotationId } =
    useParams();

  const { user } =
    useAuth();


  const [quotation, setQuotation] =
    useState<Quotation | null>(null);

  const [customerName, setCustomerName] =
    useState("");

  const [loading, setLoading] =
    useState(true);

  const [updatingStatus, setUpdatingStatus] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  const [successMessage, setSuccessMessage] =
    useState<string | null>(null);

  const [
    selectedItem,
    setSelectedItem,
  ] = useState<QuotationItem | null>(
    null,
  );

  const [
    addItemDialogOpen,
    setAddItemDialogOpen,
  ] = useState(false);


  const canEdit =
    user?.role === "ADMIN" ||
    user?.role === "OPERATOR";


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


  async function handleQuotationAction(
    action: () => Promise<void>,
    successMessageText: string,
  ) {
    setUpdatingStatus(true);
    setError(null);

    try {
      await action();

      await loadQuotation();

      setSuccessMessage(
        successMessageText,
      );

    } catch (error) {
      if (error instanceof Error) {
        setError(
          error.message,
        );
      } else {
        setError(
          "No se pudo actualizar la cotización.",
        );
      }
    } finally {
      setUpdatingStatus(false);
    }
  }


  async function handleSendQuotation() {
    if (!quotation) {
      return;
    }

    await handleQuotationAction(
      () =>
        sendQuotation(
          quotation.id,
        ),
      "Cotización enviada correctamente.",
    );
  }


  async function handleAcceptQuotation() {
    if (!quotation) {
      return;
    }

    await handleQuotationAction(
      () =>
        acceptQuotation(
          quotation.id,
        ),
      "Cotización aceptada correctamente.",
    );
  }


  async function handleRejectQuotation() {
    if (!quotation) {
      return;
    }

    await handleQuotationAction(
      () =>
        rejectQuotation(
          quotation.id,
        ),
      "Cotización rechazada correctamente.",
    );
  }


  async function handleCancelQuotation() {
    if (!quotation) {
      return;
    }

    await handleQuotationAction(
      () =>
        cancelQuotation(
          quotation.id,
        ),
      "Cotización cancelada correctamente.",
    );
  }


  async function handleReopenQuotation() {
    if (!quotation) {
      return;
    }

    await handleQuotationAction(
      () =>
        reopenQuotation(
          quotation.id,
        ),
      "Cotización abierta nuevamente para revisión.",
    );
  }


  async function handleRemoveItem(
    itemId: string,
  ) {
    if (!quotation) {
      return;
    }

    try {
      setError(null);

      await removeQuotationItem(
        quotation.id,
        itemId,
      );

      await loadQuotation();

      setSuccessMessage(
        "Concepto eliminado correctamente.",
      );

    } catch (error) {
      if (error instanceof Error) {
        setError(
          error.message,
        );
      } else {
        setError(
          "No se pudo eliminar el concepto.",
        );
      }
    }
  }


  async function handleConvertToOrder() {
    if (!quotation) {
      return;
    }

    setUpdatingStatus(true);
    setError(null);

    try {
      const orderId =
        await convertQuotationToOrder(
          quotation.id,
        );

      navigate(
        `/orders/${orderId}`,
      );

    } catch (error) {
      if (error instanceof Error) {
        setError(
          error.message,
        );
      } else {
        setError(
          "No se pudo convertir la cotización en orden.",
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
        sx={{
          mb: 2,
        }}
      >
        Volver a cotizaciones
      </Button>


      {/* Encabezado */}
      <Box
        sx={{
          display: "flex",
          justifyContent:
            "space-between",
          alignItems:
            "flex-start",
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
            sx={{
              mt: 0.5,
            }}
          >
            {quotation.id}
          </Typography>
        </Box>


        {/* Estado y acciones */}
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 1,
            flexWrap: "wrap",
            justifyContent:
              "flex-end",
          }}
        >
          <QuotationStatusChip
            status={
              quotation.status
            }
          />


          {/* DRAFT */}
          {canEdit &&
            quotation.status === "DRAFT" && (
              <Button
                variant="contained"
                disabled={
                  updatingStatus
                }
                onClick={
                  handleSendQuotation
                }
              >
                {updatingStatus
                  ? "Procesando..."
                  : "Enviar cotización"}
              </Button>
            )}


          {/* SENT */}
          {canEdit &&
            quotation.status === "SENT" && (
              <>
                <Button
                  variant="contained"
                  color="success"
                  disabled={
                    updatingStatus
                  }
                  onClick={
                    handleAcceptQuotation
                  }
                >
                  Aceptar
                </Button>

                <Button
                  variant="outlined"
                  color="error"
                  disabled={
                    updatingStatus
                  }
                  onClick={
                    handleRejectQuotation
                  }
                >
                  Rechazar
                </Button>

                <Button
                  variant="outlined"
                  color="inherit"
                  disabled={
                    updatingStatus
                  }
                  onClick={
                    handleCancelQuotation
                  }
                >
                  Cancelar
                </Button>
              </>
            )}


          {/* REJECTED */}
          {canEdit &&
            quotation.status === "REJECTED" && (
              <Button
                variant="contained"
                disabled={
                  updatingStatus
                }
                onClick={
                  handleReopenQuotation
                }
              >
                Revisar cotización
              </Button>
            )}


          {/* ACCEPTED */}
          {canEdit &&
            quotation.status === "ACCEPTED" && (
              <Button
                variant="contained"
                disabled={
                  updatingStatus
                }
                onClick={
                  handleConvertToOrder
                }
              >
                Convertir a orden
              </Button>
            )}
        </Box>
      </Box>


      {/* Información general */}
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

        <Divider
          sx={{
            my: 2,
          }}
        />

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


      {/* Conceptos */}
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
            display: "flex",
            alignItems: "center",
            justifyContent:
              "space-between",
          }}
        >
          <Typography variant="h2">
            Conceptos
          </Typography>

          {canEdit &&
            quotation.status === "DRAFT" && (
              <Button
                startIcon={
                  <AddOutlined />
                }
                onClick={() =>
                  setAddItemDialogOpen(
                    true,
                  )
                }
              >
                Agregar concepto
              </Button>
            )}
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

              <TableCell
                align="center"
                sx={{
                  width: 90,
                  minWidth: 90,
                  maxWidth: 90,
                  px: 1,
                }}
              >
                Acciones
              </TableCell>
            </TableRow>
          </TableHead>


          <TableBody>
            {quotation.items.map(
              (item) => (
                <TableRow
                  key={
                    item.id
                  }
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
                    {Number(
                      item.unit_price,
                    ).toLocaleString(
                      "es-MX",
                      {
                        minimumFractionDigits:
                          2,
                        maximumFractionDigits:
                          2,
                      },
                    )}
                  </TableCell>

                  <TableCell
                    align="right"
                  >
                    {quotation.currency}{" "}
                    {Number(
                      item.total,
                    ).toLocaleString(
                      "es-MX",
                      {
                        minimumFractionDigits:
                          2,
                        maximumFractionDigits:
                          2,
                      },
                    )}
                  </TableCell>

                  <TableCell
                    align="center"
                    sx={{
                      width: 90,
                      minWidth: 90,
                      maxWidth: 90,
                      px: 0.5,
                      whiteSpace:
                        "nowrap",
                    }}
                  >
                    {canEdit &&
                      quotation.status ===
                        "DRAFT" && (
                        <Box
                          sx={{
                            display:
                              "flex",
                            justifyContent:
                              "center",
                            gap: 0.25,
                          }}
                        >
                          <IconButton
                            size="small"
                            onClick={() =>
                              setSelectedItem(
                                item,
                              )
                            }
                          >
                            <EditOutlined
                              fontSize="small"
                            />
                          </IconButton>

                          <IconButton
                            size="small"
                            color="error"
                            onClick={() =>
                              handleRemoveItem(
                                item.id,
                              )
                            }
                          >
                            <DeleteOutlineOutlined
                              fontSize="small"
                            />
                          </IconButton>
                        </Box>
                      )}
                  </TableCell>
                </TableRow>
              ),
            )}
          </TableBody>
        </Table>
      </Paper>


      {/* Totales */}
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


      {/* Editar concepto */}
      <EditQuotationItemDialog
        open={
          Boolean(
            selectedItem,
          )
        }
        quotationId={
          quotation.id
        }
        item={
          selectedItem
        }
        onClose={() =>
          setSelectedItem(
            null,
          )
        }
        onUpdated={
          loadQuotation
        }
      />


      {/* Agregar concepto */}
      <AddQuotationItemDialog
        open={
          addItemDialogOpen
        }
        quotationId={
          quotation.id
        }
        currency={
          quotation.currency
        }
        onClose={() =>
          setAddItemDialogOpen(
            false,
          )
        }
        onCreated={async () => {
          await loadQuotation();

          setSuccessMessage(
            "Concepto agregado correctamente.",
          );
        }}
      />


      {/* Feedback */}
      <Snackbar
        open={
          Boolean(
            successMessage,
          )
        }
        autoHideDuration={
          3000
        }
        onClose={() =>
          setSuccessMessage(
            null,
          )
        }
        message={
          successMessage
        }
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
        {Number(
          value,
        ).toLocaleString(
          "es-MX",
          {
            minimumFractionDigits:
              2,
            maximumFractionDigits:
              2,
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
  const labels: Record<
    string,
    string
  > = {
    DRAFT: "Borrador",
    SENT: "Enviada",
    ACCEPTED: "Aceptada",
    REJECTED: "Rechazada",
    CANCELLED: "Cancelada",
  };


  return (
    <Chip
      label={
        labels[status] ??
        status
      }
      color={
        status === "ACCEPTED"
          ? "success"

          : status === "REJECTED" ||
              status === "CANCELLED"
            ? "error"

            : status === "SENT"
              ? "primary"

              : "default"
      }
      variant="outlined"
    />
  );
}