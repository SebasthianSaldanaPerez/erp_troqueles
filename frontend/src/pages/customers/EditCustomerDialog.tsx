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

import type { Customer } from "./types";

import type {
  CustomerAddressData,
} from "./customersApi";

import {
  changeCustomerAddress,
  changeCustomerBusinessName,
  changeCustomerContactName,
  changeCustomerEmail,
  changeCustomerNotes,
  changeCustomerPhone,
  changeCustomerRfc,
} from "./customersApi";


type Props = {
  open: boolean;
  customer: Customer;
  onClose: () => void;
  onUpdated: () => Promise<void>;
};


export default function EditCustomerDialog({
  open,
  customer,
  onClose,
  onUpdated,
}: Props) {
  const [businessName, setBusinessName] =
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

    setBusinessName(
      customer.business_name,
    );

    setRfc(
      customer.rfc ?? "",
    );

    setContactName(
      customer.contact_name ?? "",
    );

    setPhone(
      customer.phone ?? "",
    );

    setEmail(
      customer.email ?? "",
    );

    setNotes(
      customer.notes ?? "",
    );

    setStreet(
      customer.address?.street ?? "",
    );

    setExteriorNumber(
      customer.address?.exterior_number ?? "",
    );

    setInteriorNumber(
      customer.address?.interior_number ?? "",
    );

    setNeighborhood(
      customer.address?.neighborhood ?? "",
    );

    setCity(
      customer.address?.city ?? "",
    );

    setState(
      customer.address?.state ?? "",
    );

    setPostalCode(
      customer.address?.postal_code ?? "",
    );

    setCountry(
      customer.address?.country ?? "México",
    );

    setError(null);
  }, [open, customer]);


  async function handleSubmit() {
    if (!businessName.trim()) {
      setError(
        "La razón social es obligatoria.",
      );

      return;
    }

    if (
      !street.trim() ||
      !exteriorNumber.trim() ||
      !city.trim() ||
      !state.trim() ||
      !postalCode.trim() ||
      !country.trim()
    ) {
      setError(
        "Completa los campos obligatorios de la dirección.",
      );

      return;
    }

    setLoading(true);
    setError(null);

    try {
      if (
        businessName.trim() !==
        customer.business_name
      ) {
        await changeCustomerBusinessName(
          customer.id,
          businessName.trim(),
        );
      }

      if (
        (rfc.trim() || null) !==
        customer.rfc
      ) {
        await changeCustomerRfc(
          customer.id,
          rfc.trim() || null,
        );
      }

      if (
        (contactName.trim() || null) !==
        customer.contact_name
      ) {
        await changeCustomerContactName(
          customer.id,
          contactName.trim() || null,
        );
      }

      if (
        (phone.trim() || null) !==
        customer.phone
      ) {
        await changeCustomerPhone(
          customer.id,
          phone.trim() || null,
        );
      }

      if (
        (email.trim() || null) !==
        customer.email
      ) {
        await changeCustomerEmail(
          customer.id,
          email.trim() || null,
        );
      }

      if (
        (notes.trim() || null) !==
        customer.notes
      ) {
        await changeCustomerNotes(
          customer.id,
          notes.trim() || null,
        );
      }

      const newAddress: CustomerAddressData = {
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

      await changeCustomerAddress(
        customer.id,
        newAddress,
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
          "No se pudo actualizar el cliente.",
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
        Editar cliente
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
          sx={{ mt: 0.6 }}
        >
          <Grid size={{ xs: 12 }}>
            <TextField
              label="Razón social"
              value={businessName}
              onChange={(event) =>
                setBusinessName(
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
              required
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
              required
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
              required
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
              required
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
              required
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
              required
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