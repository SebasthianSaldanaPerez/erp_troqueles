import {
  useEffect,
  useState,
} from "react";

import {
  Alert,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
} from "@mui/material";

import type {
  QuotationItem,
} from "./types";

import {
  updateQuotationItem,
} from "./quotationsApi";


type Props = {
  open: boolean;
  quotationId: string;
  item: QuotationItem | null;
  onClose: () => void;
  onUpdated: () => Promise<void>;
};


export default function EditQuotationItemDialog({
  open,
  quotationId,
  item,
  onClose,
  onUpdated,
}: Props) {
  const [description, setDescription] =
    useState("");

  const [quantity, setQuantity] =
    useState("");

  const [unitPrice, setUnitPrice] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);


  useEffect(() => {
    if (!open || !item) {
      return;
    }

    setDescription(
      item.description,
    );

    setQuantity(
      String(item.quantity),
    );

    setUnitPrice(
      String(item.unit_price),
    );

    setError(null);
  }, [open, item]);


  async function handleSubmit() {
    if (!item) {
      return;
    }

    if (!description.trim()) {
      setError(
        "La descripción es obligatoria.",
      );

      return;
    }

    const parsedQuantity =
      Number(quantity);

    const parsedUnitPrice =
      Number(unitPrice);

    if (
      Number.isNaN(parsedQuantity) ||
      parsedQuantity <= 0
    ) {
      setError(
        "La cantidad debe ser mayor a cero.",
      );

      return;
    }

    if (
      Number.isNaN(parsedUnitPrice) ||
      parsedUnitPrice < 0
    ) {
      setError(
        "El precio unitario no es válido.",
      );

      return;
    }

    setLoading(true);
    setError(null);

    try {
      await updateQuotationItem(
        quotationId,
        item.id,
        {
          description:
            description.trim(),

          quantity:
            parsedQuantity,

          unit_price:
            parsedUnitPrice,

          currency:
            item.currency,
        },
      );

      await onUpdated();

      onClose();

    } catch (error) {
      if (error instanceof Error) {
        setError(
          error.message,
        );
      } else {
        setError(
          "No se pudo actualizar el concepto.",
        );
      }
    } finally {
      setLoading(false);
    }
  }


  return (
    <Dialog
      open={open}
      onClose={
        loading
          ? undefined
          : onClose
      }
      fullWidth
      maxWidth="sm"
    >
      <DialogTitle>
        Editar concepto
      </DialogTitle>

      <DialogContent>
        {error && (
          <Alert
            severity="error"
            sx={{ mb: 2 }}
          >
            {error}
          </Alert>
        )}

        <TextField
          label="Descripción"
          value={description}
          onChange={(event) =>
            setDescription(
              event.target.value,
            )
          }
          fullWidth
          sx={{ mt: 1, mb: 2 }}
        />

        <TextField
          label="Cantidad"
          type="number"
          value={quantity}
          onChange={(event) =>
            setQuantity(
              event.target.value,
            )
          }
          fullWidth
          sx={{ mb: 2 }}
        />

        <TextField
          label="Precio unitario"
          type="number"
          value={unitPrice}
          onChange={(event) =>
            setUnitPrice(
              event.target.value,
            )
          }
          fullWidth
        />
      </DialogContent>

      <DialogActions
        sx={{
          px: 3,
          pb: 3,
        }}
      >
        <Button
          onClick={onClose}
          disabled={loading}
          color="inherit"
        >
          Cancelar
        </Button>

        <Button
          onClick={handleSubmit}
          disabled={loading}
          variant="contained"
        >
          {loading
            ? "Guardando..."
            : "Guardar cambios"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}