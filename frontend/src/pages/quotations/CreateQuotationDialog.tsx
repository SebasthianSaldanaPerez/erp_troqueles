import {
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  Alert,
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  IconButton,
  MenuItem,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";

import AddOutlined from "@mui/icons-material/AddOutlined";
import DeleteOutlineOutlined from "@mui/icons-material/DeleteOutlineOutlined";

import {
  getCustomers,
} from "../customers/customersApi";

import type {
  Customer,
} from "../customers/types";

import {
  addQuotationItem,
  createQuotation,
} from "./quotationsApi";


type Props = {
  open: boolean;
  onClose: () => void;
  onCreated: (
    quotationId: string,
  ) => void;
};


type DraftItem = {
  id: string;
  description: string;
  quantity: string;
  unitPrice: string;
};


function createEmptyItem(): DraftItem {
  return {
    id: crypto.randomUUID(),
    description: "",
    quantity: "1",
    unitPrice: "",
  };
}


export default function CreateQuotationDialog({
  open,
  onClose,
  onCreated,
}: Props) {
  const [customers, setCustomers] =
    useState<Customer[]>([]);

  const [customerId, setCustomerId] =
    useState("");

  const [taxRate, setTaxRate] =
    useState("16");

  const [currency, setCurrency] =
    useState("MXN");

  const [items, setItems] =
    useState<DraftItem[]>([
      createEmptyItem(),
    ]);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);


  useEffect(() => {
    if (!open) {
      return;
    }

    async function loadCustomers() {
      try {
        const data =
          await getCustomers();

        setCustomers(
          data.filter(
            (customer) =>
              customer.status === "ACTIVE",
          ),
        );

      } catch {
        setError(
          "No se pudieron cargar los clientes.",
        );
      }
    }

    loadCustomers();
  }, [open]);


  const subtotal = useMemo(() => {
    return items.reduce(
      (total, item) => {
        const quantity =
          Number(item.quantity);

        const unitPrice =
          Number(item.unitPrice);

        if (
          Number.isNaN(quantity) ||
          Number.isNaN(unitPrice)
        ) {
          return total;
        }

        return (
          total +
          quantity * unitPrice
        );
      },
      0,
    );
  }, [items]);


  const tax = useMemo(() => {
    const parsedTaxRate =
      Number(taxRate);

    if (
      Number.isNaN(parsedTaxRate)
    ) {
      return 0;
    }

    return (
      subtotal *
      (parsedTaxRate / 100)
    );
  }, [subtotal, taxRate]);


  const total =
    subtotal + tax;


  function resetForm() {
    setCustomerId("");
    setTaxRate("16");
    setCurrency("MXN");

    setItems([
      createEmptyItem(),
    ]);

    setError(null);
  }


  function handleClose() {
    if (loading) {
      return;
    }

    resetForm();
    onClose();
  }


  function handleItemChange(
    itemId: string,
    field:
      | "description"
      | "quantity"
      | "unitPrice",
    value: string,
  ) {
    setItems((current) =>
      current.map((item) =>
        item.id === itemId
          ? {
              ...item,
              [field]: value,
            }
          : item,
      ),
    );
  }


  function addItemRow() {
    setItems((current) => [
      ...current,
      createEmptyItem(),
    ]);
  }


  function removeItemRow(
    itemId: string,
  ) {
    setItems((current) => {
      if (current.length === 1) {
        return current;
      }

      return current.filter(
        (item) =>
          item.id !== itemId,
      );
    });
  }


  async function handleSubmit() {
    setError(null);

    /*
     * 1. Validar cliente
     */
    if (!customerId) {
      setError(
        "Selecciona un cliente.",
      );

      return;
    }


    /*
     * 2. Validar impuesto
     */
    const parsedTaxRate =
      Number(taxRate);

    if (
      Number.isNaN(parsedTaxRate) ||
      parsedTaxRate < 0
    ) {
      setError(
        "La tasa de impuesto no es válida.",
      );

      return;
    }


    /*
     * 3. Validar items
     */
    if (items.length === 0) {
      setError(
        "Agrega al menos un concepto.",
      );

      return;
    }


    for (const item of items) {
      const quantity =
        Number(item.quantity);

      const unitPrice =
        Number(item.unitPrice);


      if (!item.description.trim()) {
        setError(
          "Todos los conceptos deben tener descripción.",
        );

        return;
      }


      if (
        Number.isNaN(quantity) ||
        quantity <= 0
      ) {
        setError(
          "Las cantidades deben ser mayores a cero.",
        );

        return;
      }


      if (
        Number.isNaN(unitPrice) ||
        unitPrice < 0
      ) {
        setError(
          "Los precios unitarios no son válidos.",
        );

        return;
      }
    }


    /*
     * 4. Crear quotation
     */
    setLoading(true);

    try {
      const quotationId =
        await createQuotation({
          customer_id:
            customerId,

          tax_rate:
            parsedTaxRate,

          currency,
        });


      /*
       * 5. Agregar items
       */
      for (const item of items) {
        await addQuotationItem(
          quotationId,
          {
            description:
              item.description.trim(),

            quantity:
              Number(
                item.quantity,
              ),

            unit_price:
              Number(
                item.unitPrice,
              ),

            currency,
          },
        );
      }


      /*
       * 6. Todo salió bien
       */
      resetForm();

      onCreated(
        quotationId,
      );

    } catch (error) {
      console.error(
        "Error creating quotation:",
        error,
      );

      if (error instanceof Error) {
        setError(
          error.message,
        );
      } else {
        setError(
          "No se pudo crear la cotización.",
        );
      }

    } finally {
      setLoading(false);
    }
  }


  return (
    <Dialog
      open={open}
      onClose={handleClose}
      fullWidth
      maxWidth="lg"
    >
      <DialogTitle>
        Nueva cotización
      </DialogTitle>

      <DialogContent>
        {error && (
          <Alert
            severity="error"
            sx={{
              mb: 2,
            }}
          >
            {error}
          </Alert>
        )}

        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: {
              xs: "1fr",
              md: "2fr 1fr 1fr",
            },
            gap: 2,
            mt: 1,
            mb: 3,
          }}
        >
          <TextField
            select
            label="Cliente"
            value={customerId}
            onChange={(event) =>
              setCustomerId(
                event.target.value,
              )
            }
            fullWidth
            required
          >
            {customers.map(
              (customer) => (
                <MenuItem
                  key={
                    customer.id
                  }
                  value={
                    customer.id
                  }
                >
                  {
                    customer.business_name
                  }
                </MenuItem>
              ),
            )}
          </TextField>

          <TextField
            label="Impuesto (%)"
            type="number"
            value={taxRate}
            onChange={(event) =>
              setTaxRate(
                event.target.value,
              )
            }
            fullWidth
            required
          />

          <TextField
            select
            label="Moneda"
            value={currency}
            onChange={(event) =>
              setCurrency(
                event.target.value,
              )
            }
            fullWidth
          >
            <MenuItem value="MXN">
              MXN
            </MenuItem>

            <MenuItem value="USD">
              USD
            </MenuItem>
          </TextField>
        </Box>


        <Paper
          variant="outlined"
          sx={{
            overflow: "hidden",
          }}
        >
          <Box
            sx={{
              px: 2,
              py: 1.5,
              display: "flex",
              alignItems:
                "center",
              justifyContent:
                "space-between",
            }}
          >
            <Typography
              sx={{
                fontWeight: 600,
              }}
            >
              Conceptos
            </Typography>

            <Button
              startIcon={
                <AddOutlined />
              }
              onClick={
                addItemRow
              }
            >
              Agregar concepto
            </Button>
          </Box>


          <Table>
            <TableHead>
              <TableRow>
                <TableCell>
                  Descripción
                </TableCell>

                <TableCell
                  sx={{
                    width: 140,
                  }}
                >
                  Cantidad
                </TableCell>

                <TableCell
                  sx={{
                    width: 180,
                  }}
                >
                  Precio unitario
                </TableCell>

                <TableCell
                  align="right"
                  sx={{
                    width: 170,
                  }}
                >
                  Total
                </TableCell>

                <TableCell
                  sx={{
                    width: 50,
                  }}
                />
              </TableRow>
            </TableHead>


            <TableBody>
              {items.map(
                (item) => {
                  const quantity =
                    Number(
                      item.quantity,
                    );

                  const unitPrice =
                    Number(
                      item.unitPrice,
                    );

                  const itemTotal =
                    (
                      Number.isFinite(
                        quantity,
                      ) &&
                      Number.isFinite(
                        unitPrice,
                      )
                    )
                      ? quantity *
                        unitPrice
                      : 0;


                  return (
                    <TableRow
                      key={
                        item.id
                      }
                    >
                      <TableCell>
                        <TextField
                          value={
                            item.description
                          }
                          onChange={(
                            event,
                          ) =>
                            handleItemChange(
                              item.id,
                              "description",
                              event
                                .target
                                .value,
                            )
                          }
                          placeholder="Descripción"
                          size="small"
                          fullWidth
                        />
                      </TableCell>


                      <TableCell>
                        <TextField
                          value={
                            item.quantity
                          }
                          onChange={(
                            event,
                          ) =>
                            handleItemChange(
                              item.id,
                              "quantity",
                              event
                                .target
                                .value,
                            )
                          }
                          type="number"
                          size="small"
                          fullWidth
                        />
                      </TableCell>


                      <TableCell>
                        <TextField
                          value={
                            item.unitPrice
                          }
                          onChange={(
                            event,
                          ) =>
                            handleItemChange(
                              item.id,
                              "unitPrice",
                              event
                                .target
                                .value,
                            )
                          }
                          type="number"
                          size="small"
                          fullWidth
                        />
                      </TableCell>


                      <TableCell
                        align="right"
                      >
                        {currency}{" "}
                        {itemTotal.toLocaleString(
                          "es-MX",
                          {
                            minimumFractionDigits:
                              2,

                            maximumFractionDigits:
                              2,
                          },
                        )}
                      </TableCell>


                      <TableCell>
                        <IconButton
                          size="small"
                          disabled={
                            items.length ===
                            1
                          }
                          onClick={() =>
                            removeItemRow(
                              item.id,
                            )
                          }
                        >
                          <DeleteOutlineOutlined />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  );
                },
              )}
            </TableBody>
          </Table>
        </Paper>


        <Box
          sx={{
            display: "flex",
            justifyContent:
              "flex-end",
            mt: 3,
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
              value={subtotal}
              currency={
                currency
              }
            />

            <SummaryRow
              label={`Impuesto (${taxRate || 0}%)`}
              value={tax}
              currency={
                currency
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
                value={total}
                currency={
                  currency
                }
                strong
              />
            </Box>
          </Box>
        </Box>
      </DialogContent>


      <DialogActions
        sx={{
          px: 3,
          pb: 3,
        }}
      >
        <Button
          onClick={
            handleClose
          }
          color="inherit"
          disabled={
            loading
          }
        >
          Cancelar
        </Button>

        <Button
          onClick={
            handleSubmit
          }
          variant="contained"
          disabled={
            loading
          }
        >
          {loading
            ? "Creando..."
            : "Crear cotización"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}


function SummaryRow({
  label,
  value,
  currency,
  strong = false,
}: {
  label: string;
  value: number;
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
        {value.toLocaleString(
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