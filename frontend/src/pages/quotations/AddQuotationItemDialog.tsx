import {
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

import {
  addQuotationItem,
} from "./quotationsApi";


type Props = {
  open: boolean;
  quotationId: string;
  currency: string;
  onClose: () => void;
  onCreated: () => Promise<void>;
};


export default function AddQuotationItemDialog({
  open,
  quotationId,
  currency,
  onClose,
  onCreated,
}: Props) {
  const [description, setDescription] =
    useState("");

  const [quantity, setQuantity] =
    useState("1");

  const [unitPrice, setUnitPrice] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);


  function resetForm() {
    setDescription("");
    setQuantity("1");
    setUnitPrice("");
    setError(null);
  }


  function handleClose() {
    if (loading) {
      return;
    }

    resetForm();
    onClose();
  }


  async function handleSubmit() {
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
      await addQuotationItem(
        quotationId,
        {
          description:
            description.trim(),

          quantity:
            parsedQuantity,

          unit_price:
            parsedUnitPrice,

          currency,
        },
      );

      await onCreated();

      resetForm();
      onClose();

    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError(
          "No se pudo agregar el concepto.",
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
      maxWidth="sm"
    >
      <DialogTitle>
        Agregar concepto
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
          autoFocus
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
          onClick={handleClose}
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
            ? "Agregando..."
            : "Agregar concepto"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}