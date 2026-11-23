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
  MenuItem,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";

import {
  useNavigate,
} from "react-router";

import {
  getQuotations,
} from "./quotationsApi";

import type {
  Quotation,
} from "./types";

import AddOutlined from "@mui/icons-material/AddOutlined";

import {
  useAuth,
} from "../../auth/AuthContext";

import CreateQuotationDialog
  from "./CreateQuotationDialog";


export default function QuotationsPage() {
  const { user } = useAuth();

  const canEdit =
    user?.role === "ADMIN" ||
    user?.role === "OPERATOR";

  const [createDialogOpen, setCreateDialogOpen] =
    useState(false);

  const navigate = useNavigate();

  const [quotations, setQuotations] =
    useState<Quotation[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  const [search, setSearch] =
    useState("");

  const [statusFilter, setStatusFilter] =
    useState<string>("ALL");


  async function loadQuotations() {
    try {
      setError(null);

      const data =
        await getQuotations();

      setQuotations(data);

    } catch {
      setError(
        "No se pudieron cargar las cotizaciones.",
      );
    } finally {
      setLoading(false);
    }
  }


  useEffect(() => {
    loadQuotations();
  }, []);


  const filteredQuotations = quotations.filter(
    (quotation) => {
      const searchText =
        search.trim().toLowerCase();

      const matchesSearch =
        !searchText ||
        quotation.id
          .toLowerCase()
          .includes(searchText) ||
        quotation.customer_id
          .toLowerCase()
          .includes(searchText);

      const matchesStatus =
        statusFilter === "ALL" ||
        quotation.status === statusFilter;

      return (
        matchesSearch &&
        matchesStatus
      );
    },
  );


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


  return (
    <Box>
        <Box
      sx={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        mb: 3,
        gap: 2,
      }}
    >
      <Box>
        <Typography variant="h1">
          Cotizaciones
        </Typography>

        <Typography
          color="text.secondary"
          sx={{ mt: 0.5 }}
        >
          Consulta y administra las cotizaciones.
        </Typography>
      </Box>

      {canEdit && (
        <Button
          variant="contained"
          startIcon={<AddOutlined />}
          onClick={() =>
            setCreateDialogOpen(true)
          }
        >
          Nueva cotización
        </Button>
      )}
    </Box>

      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 2,
          mb: 2,
          flexWrap: "wrap",
        }}
      >
        <TextField
          placeholder="Buscar cotización..."
          size="small"
          value={search}
          onChange={(event) =>
            setSearch(
              event.target.value,
            )
          }
          sx={{
            width: 320,
          }}
        />

        <TextField
          select
          label="Estado"
          size="small"
          value={statusFilter}
          onChange={(event) =>
            setStatusFilter(
              event.target.value,
            )
          }
          sx={{
            width: 180,
          }}
        >
          <MenuItem value="ALL">
            Todos
          </MenuItem>

          <MenuItem value="DRAFT">
            Borrador
          </MenuItem>

          <MenuItem value="SENT">
            Enviada
          </MenuItem>

          <MenuItem value="ACCEPTED">
            Aceptada
          </MenuItem>

          <MenuItem value="REJECTED">
            Rechazada
          </MenuItem>

          <MenuItem value="CANCELLED">
            Cancelada
          </MenuItem>
        </TextField>

        <Typography
          color="text.secondary"
          sx={{
            ml: "auto",
            fontSize: 14,
          }}
        >
          {filteredQuotations.length} cotización
          {filteredQuotations.length === 1
            ? ""
            : "es"}
        </Typography>
      </Box>

      {error && (
        <Alert
          severity="error"
          sx={{ mb: 2 }}
        >
          {error}
        </Alert>
      )}

      <TableContainer
        component={Paper}
        variant="outlined"
      >
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>
                ID
              </TableCell>

              <TableCell>
                Cliente
              </TableCell>

              <TableCell>
                Estado
              </TableCell>

              <TableCell align="right">
                Subtotal
              </TableCell>

              <TableCell align="right">
                Impuesto
              </TableCell>

              <TableCell align="right">
                Total
              </TableCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {filteredQuotations.length === 0 ? (
              <TableRow>
                <TableCell
                  colSpan={6}
                  align="center"
                  sx={{
                    py: 6,
                    color: "text.secondary",
                  }}
                >
                  {quotations.length === 0
                    ? "No hay cotizaciones registradas."
                    : "No se encontraron cotizaciones con esos filtros."}
                </TableCell>
              </TableRow>
            ) : (
              filteredQuotations.map(
                (quotation) => (
                  <TableRow
                    key={quotation.id}
                    hover
                    onClick={() =>
                      navigate(
                        `/quotations/${quotation.id}`,
                      )
                    }
                    sx={{
                      cursor: "pointer",
                    }}
                  >
                    <TableCell>
                      {quotation.id.slice(
                        0,
                        8,
                      )}
                    </TableCell>

                    <TableCell>
                      {quotation.customer_id.slice(
                        0,
                        8,
                      )}
                    </TableCell>

                    <TableCell>
                      <QuotationStatusChip
                        status={
                          quotation.status
                        }
                      />
                    </TableCell>

                    <TableCell align="right">
                      ${quotation.subtotal}
                    </TableCell>

                    <TableCell align="right">
                      ${quotation.tax}
                    </TableCell>

                    <TableCell align="right">
                      <Typography
                        sx={{
                          fontWeight: 600,
                        }}
                      >
                        ${quotation.total}
                      </Typography>
                    </TableCell>
                  </TableRow>
                ),
              )
            )}
          </TableBody>
        </Table>
      </TableContainer>
      <CreateQuotationDialog
        open={createDialogOpen}
        onClose={() =>
          setCreateDialogOpen(false)
        }
        onCreated={(quotationId) => {
          setCreateDialogOpen(false);

          navigate(
            `/quotations/${quotationId}`,
          );
        }}
      />
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
      size="small"
      label={labels[status] ?? status}
      color={
        status === "ACCEPTED"
          ? "success"
          : status === "REJECTED" ||
              status === "CANCELLED"
            ? "error"
            : "default"
      }
      variant="outlined"
    />
  );
}