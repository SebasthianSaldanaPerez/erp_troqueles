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
  Grid,
  TextField,
} from "@mui/material";

import type { Supplier } from "./types";

import type {
  SupplierAddressData,
} from "./suppliersApi";

import {
  changeSupplierAddress,
  changeSupplierContactName,
  changeSupplierEmail,
  changeSupplierNotes,
  changeSupplierPhone,
  changeSupplierRfc,
  renameSupplier,
} from "./suppliersApi";


type Props = {
  open: boolean;
  supplier: Supplier;
  onClose: () => void;
  onUpdated: () => Promise<void>;
};


export default function EditSupplierDialog({
  open,
  supplier,
  onClose,
  onUpdated,
}: Props) {
  const [name, setName] =
    useState("");

  const [rfc, setRfc] =
    useState("");

  const [contactName, setContactName] =
    useState("");

  const [phone, setPhone] =
    useState("");

  const [email, setEmail] =
    useState("");

  const [notes, setNotes] =
    useState("");

  const [street, setStreet] =
    useState("");

  const [exteriorNumber, setExteriorNumber] =
    useState("");

  const [interiorNumber, setInteriorNumber] =
    useState("");

  const [neighborhood, setNeighborhood] =
    useState("");

  const [city, setCity] =
    useState("");

  const [state, setState] =
    useState("");

  const [postalCode, setPostalCode] =
    useState("");

  const [country, setCountry] =
    useState("México");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);


  useEffect(() => {
    if (!open) {
      return;
    }

    setName(
      supplier.name,
    );

    setRfc(
      supplier.rfc ?? "",
    );

    setContactName(
      supplier.contact_name ?? "",
    );

    setPhone(
      supplier.phone ?? "",
    );

    setEmail(
      supplier.email ?? "",
    );

    setNotes(
      supplier.notes ?? "",
    );

    setStreet(
      supplier.address?.street ?? "",
    );

    setExteriorNumber(
      supplier.address?.exterior_number ?? "",
    );

    setInteriorNumber(
      supplier.address?.interior_number ?? "",
    );

    setNeighborhood(
      supplier.address?.neighborhood ?? "",
    );

    setCity(
      supplier.address?.city ?? "",
    );

    setState(
      supplier.address?.state ?? "",
    );

    setPostalCode(
      supplier.address?.postal_code ?? "",
    );

    setCountry(
      supplier.address?.country ?? "México",
    );

    setError(null);
  }, [open, supplier]);


  async function handleSubmit() {
    if (!name.trim()) {
      setError(
        "El nombre del proveedor es obligatorio.",
      );

      return;
    }

    const hasAnyAddressField =
      street.trim() ||
      exteriorNumber.trim() ||
      interiorNumber.trim() ||
      neighborhood.trim() ||
      city.trim() ||
      state.trim() ||
      postalCode.trim();

    if (
      hasAnyAddressField &&
      (
        !street.trim() ||
        !exteriorNumber.trim() ||
        !city.trim() ||
        !state.trim() ||
        !postalCode.trim() ||
        !country.trim()
      )
    ) {
      setError(
        "Si registras dirección, completa calle, número exterior, ciudad, estado, código postal y país.",
      );

      return;
    }

    setLoading(true);
    setError(null);

    try {
      if (
        name.trim() !== supplier.name
      ) {
        await renameSupplier(
          supplier.id,
          name.trim(),
        );
      }

      if (
        rfc.trim() !==
        (supplier.rfc ?? "")
      ) {
        await changeSupplierRfc(
          supplier.id,
          rfc.trim(),
        );
      }

      if (
        contactName.trim() !==
        (supplier.contact_name ?? "")
      ) {
        await changeSupplierContactName(
          supplier.id,
          contactName.trim() || null,
        );
      }

      if (
        phone.trim() !==
        (supplier.phone ?? "")
      ) {
        await changeSupplierPhone(
          supplier.id,
          phone.trim(),
        );
      }

      if (
        email.trim() !==
        (supplier.email ?? "")
      ) {
        await changeSupplierEmail(
          supplier.id,
          email.trim(),
        );
      }

      if (
        notes.trim() !==
        (supplier.notes ?? "")
      ) {
        await changeSupplierNotes(
          supplier.id,
          notes.trim() || null,
        );
      }

      if (hasAnyAddressField) {
        const newAddress: SupplierAddressData = {
          street:
            street.trim(),

          exterior_number:
            exteriorNumber.trim(),

          interior_number:
            interiorNumber.trim() || null,

          neighborhood:
            neighborhood.trim() || null,

          city:
            city.trim(),

          state:
            state.trim(),

          postal_code:
            postalCode.trim(),

          country:
            country.trim(),
        };

        await changeSupplierAddress(
          supplier.id,
          newAddress,
        );
      }

      await onUpdated();

      onClose();

    } catch (error) {
      if (error instanceof Error) {
        setError(
          error.message,
        );
      } else {
        setError(
          "No se pudo actualizar el proveedor.",
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
      maxWidth="md"
    >
      <DialogTitle>
        Editar proveedor
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

        <Grid
          container
          spacing={2}
          sx={{ mt: 0.5 }}
        >
          <Grid size={{ xs: 12 }}>
            <TextField
              label="Nombre del proveedor"
              value={name}
              onChange={(event) =>
                setName(
                  event.target.value,
                )
              }
              fullWidth
              required
            />
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              label="RFC"
              value={rfc}
              onChange={(event) =>
                setRfc(
                  event.target.value,
                )
              }
              fullWidth
            />
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              label="Nombre de contacto"
              value={contactName}
              onChange={(event) =>
                setContactName(
                  event.target.value,
                )
              }
              fullWidth
            />
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              label="Teléfono"
              value={phone}
              onChange={(event) =>
                setPhone(
                  event.target.value,
                )
              }
              fullWidth
            />
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              label="Correo electrónico"
              type="email"
              value={email}
              onChange={(event) =>
                setEmail(
                  event.target.value,
                )
              }
              fullWidth
            />
          </Grid>

          <Grid size={{ xs: 12 }}>
            <TextField
              label="Calle"
              value={street}
              onChange={(event) =>
                setStreet(
                  event.target.value,
                )
              }
              fullWidth
            />
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              label="Número exterior"
              value={exteriorNumber}
              onChange={(event) =>
                setExteriorNumber(
                  event.target.value,
                )
              }
              fullWidth
            />
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              label="Número interior"
              value={interiorNumber}
              onChange={(event) =>
                setInteriorNumber(
                  event.target.value,
                )
              }
              fullWidth
            />
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              label="Colonia"
              value={neighborhood}
              onChange={(event) =>
                setNeighborhood(
                  event.target.value,
                )
              }
              fullWidth
            />
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              label="Ciudad"
              value={city}
              onChange={(event) =>
                setCity(
                  event.target.value,
                )
              }
              fullWidth
            />
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              label="Estado"
              value={state}
              onChange={(event) =>
                setState(
                  event.target.value,
                )
              }
              fullWidth
            />
          </Grid>

          <Grid size={{ xs: 12, md: 3 }}>
            <TextField
              label="Código postal"
              value={postalCode}
              onChange={(event) =>
                setPostalCode(
                  event.target.value,
                )
              }
              fullWidth
            />
          </Grid>

          <Grid size={{ xs: 12, md: 3 }}>
            <TextField
              label="País"
              value={country}
              onChange={(event) =>
                setCountry(
                  event.target.value,
                )
              }
              fullWidth
            />
          </Grid>

          <Grid size={{ xs: 12 }}>
            <TextField
              label="Notas"
              value={notes}
              onChange={(event) =>
                setNotes(
                  event.target.value,
                )
              }
              fullWidth
              multiline
              minRows={3}
            />
          </Grid>
        </Grid>
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
          variant="contained"
          disabled={loading}
        >
          {loading
            ? "Guardando..."
            : "Guardar cambios"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}