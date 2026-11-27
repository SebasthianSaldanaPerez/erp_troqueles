import { useEffect, useState } from "react";

import {
  Alert,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

import {
  reviseOrder,
  type OrderItem,
} from "./ordersApi";

interface Props {
  open: boolean;
  orderId: string;
  item: OrderItem | null;
  onClose: () => void;
  onSaved: () => void;
}

export default function ReviseOrderItemDialog({
  open,
  orderId,
  item,
  onClose,
  onSaved,
}: Props) {
  const [description, setDescription] = useState("");
  const [quantity, setQuantity] = useState("");
  const [unitPrice, setUnitPrice] = useState("");
  const [reason, setReason] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!open || !item) return;

    setDescription(item.description);
    setQuantity(String(item.quantity));
    setUnitPrice(item.unit_price);
    setReason("");
    setError(null);
  }, [open, item]);

  async function handleSave() {
    if (!item || saving) return;

    const parsedQuantity = Number(quantity);
    const parsedPrice = Number(unitPrice);

    if (!description.trim()) {
      setError("La descripción es obligatoria.");
      return;
    }

    if (!Number.isInteger(parsedQuantity) || parsedQuantity <= 0) {
      setError("La cantidad debe ser un entero mayor que cero.");
      return;
    }

    if (
      !/^\d+(\.\d+)?$/.test(unitPrice) ||
      !Number.isFinite(parsedPrice)
    ) {
      setError("Ingresa un precio válido.");
      return;
    }

    if (!reason.trim()) {
      setError("Debes indicar el motivo de la revisión.");
      return;
    }

    setSaving(true);
    setError(null);

    try {
      await reviseOrder(orderId, {
        item_id: item.id,
        description: description.trim(),
        quantity: parsedQuantity,
        unit_price: unitPrice,
        currency: item.currency,
        reason: reason.trim(),
      });

      onClose();
      onSaved();
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "No se pudo guardar la revisión.",
      );
    } finally {
      setSaving(false);
    }
  }

  return (
    <Dialog
      open={open}
      onClose={saving ? undefined : onClose}
      fullWidth
      maxWidth="sm"
    >
      <form
        onSubmit={(event) => {
          event.preventDefault();
          void handleSave();
        }}
      >
        <DialogTitle>
          Revisar concepto de la orden
        </DialogTitle>

        <DialogContent>
          <Stack spacing={2.5} sx={{ mt: 1 }}>
            <Typography
              variant="body2"
              color="text.secondary"
            >
              Los cambios se registrarán como una
              nueva revisión de la orden.
            </Typography>

            {error && (
              <Alert severity="error">
                {error}
              </Alert>
            )}

            <TextField
              label="Descripción"
              value={description}
              onChange={(event) =>
                setDescription(event.target.value)
              }
              fullWidth
              multiline
              minRows={2}
              required
              disabled={saving}
            />

            <TextField
              label="Cantidad"
              type="number"
              value={quantity}
              onChange={(event) =>
                setQuantity(event.target.value)
              }
              fullWidth
              required
              disabled={saving}
              slotProps={{
                htmlInput: {
                  min: 1,
                  step: 1,
                },
              }}
            />

            <TextField
              label={`Precio unitario (${item?.currency ?? ""})`}
              type="number"
              value={unitPrice}
              onChange={(event) =>
                setUnitPrice(event.target.value)
              }
              fullWidth
              required
              disabled={saving}
              slotProps={{
                htmlInput: {
                  min: 0,
                  step: "any",
                },
              }}
            />

            <TextField
              label="Motivo de la revisión"
              value={reason}
              onChange={(event) =>
                setReason(event.target.value)
              }
              fullWidth
              multiline
              minRows={3}
              required
              disabled={saving}
              placeholder="Explica qué solicitó cambiar el cliente..."
            />
          </Stack>
        </DialogContent>

        <DialogActions sx={{ p: 3, pt: 1 }}>
          <Button
            onClick={onClose}
            color="inherit"
            disabled={saving}
          >
            Cancelar
          </Button>

          <Button
            type="submit"
            variant="contained"
            disabled={saving}
          >
            {saving ? "Guardando..." : "Guardar revisión"}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}