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
  Grid,
  TextField,
} from "@mui/material";

import {
  createCustomer,
} from "./customersApi";


type Props = {
  open: boolean;
  onClose: () => void;
  onCreated: () => void;
};


export default function CreateCustomerDialog({
  open,
  onClose,
  onCreated,
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


  function resetForm() {
    setBusinessName("");
    setRfc("");
    setContactName("");
    setPhone("");
    setEmail("");
    setNotes("");

    setStreet("");
    setExteriorNumber("");
    setInteriorNumber("");
    setNeighborhood("");
    setCity("");
    setState("");
    setPostalCode("");
    setCountry("México");

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
    setError(null);

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

    try {
      await createCustomer({
        business_name:
          businessName.trim(),

        rfc:
          rfc.trim() || null,

        contact_name:
          contactName.trim() || null,

        phone:
          phone.trim() || null,

        email:
          email.trim() || null,

        notes:
          notes.trim() || null,

        address: {
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
        },
      });

      resetForm();

      onCreated();
      onClose();

    } catch (error) {
      if (error instanceof Error) {
        setError(
          error.message,
        );
      } else {
        setError(
          "No se pudo crear el cliente.",
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
      maxWidth="md"
    >
      <DialogTitle>
        Nuevo cliente
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
              label="Razón social"
              value={businessName}
              onChange={(event) =>
                setBusinessName(
                  event.target.value,
                )
              }
              fullWidth
              required
              autoFocus
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
          onClick={handleClose}
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
            : "Crear cliente"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}