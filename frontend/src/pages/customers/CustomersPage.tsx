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
  Paper,
  MenuItem,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";

import AddOutlined from "@mui/icons-material/AddOutlined";

import { useAuth } from "../../auth/AuthContext";
import { getCustomers } from "./customersApi";
import CreateCustomerDialog
  from "./CreateCustomerDialog";
import type { Customer } from "./types";
import { useNavigate } from "react-router";


export default function CustomersPage() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [customers, setCustomers] =
    useState<Customer[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  const [
    createDialogOpen,
    setCreateDialogOpen,
    ] = useState(false);

  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] =
  useState<"ALL" | "ACTIVE" | "INACTIVE">("ALL");

  const filteredCustomers = customers.filter(
  (customer) => {
    const searchText = search
      .trim()
      .toLowerCase();

    const matchesSearch =
      !searchText ||
      customer.business_name
        .toLowerCase()
        .includes(searchText) ||
      customer.rfc
        ?.toLowerCase()
        .includes(searchText) ||
      customer.contact_name
        ?.toLowerCase()
        .includes(searchText) ||
      customer.email
        ?.toLowerCase()
        .includes(searchText);

    const matchesStatus =
      statusFilter === "ALL" ||
      customer.status === statusFilter;

    return matchesSearch && matchesStatus;
  })
    .sort((a, b) => {
        if (a.status !== b.status) {
        return a.status === "ACTIVE" ? -1 : 1;
        }

        return a.business_name.localeCompare(
        b.business_name,
        "es",
        {
            sensitivity: "base",
        },
        );
    });

  const canEdit =
    user?.role === "ADMIN" ||
    user?.role === "OPERATOR";


    async function loadCustomers() {
    try {
        setError(null);

        const data =
        await getCustomers();

        setCustomers(data);

    } catch {
        setError(
        "No se pudieron cargar los clientes.",
        );
    } finally {
        setLoading(false);
    }
    }


    useEffect(() => {
    loadCustomers();
}, []);


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
          alignItems: "center",
          justifyContent: "space-between",
          mb: 3,
          gap: 2,
        }}
      >
        <Box>
          <Typography variant="h1">
            Clientes
          </Typography>

          <Typography
            color="text.secondary"
            sx={{ mt: 0.5 }}
          >
            Consulta y administra los clientes registrados.
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
            Nuevo cliente
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
            placeholder="Buscar cliente..."
            size="small"
            value={search}
            onChange={(event) =>
            setSearch(event.target.value)
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
                event.target.value as
                | "ALL"
                | "ACTIVE"
                | "INACTIVE",
            )
            }
            sx={{
            width: 180,
            }}
        >
            <MenuItem value="ALL">
            Todos
            </MenuItem>

            <MenuItem value="ACTIVE">
            Activos
            </MenuItem>

            <MenuItem value="INACTIVE">
            Inactivos
            </MenuItem>
        </TextField>

        <Typography
            color="text.secondary"
            sx={{
            ml: "auto",
            fontSize: 14,
            }}
        >
            {filteredCustomers.length} cliente
            {filteredCustomers.length === 1
            ? ""
            : "s"}
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
                Cliente
              </TableCell>

              <TableCell>
                RFC
              </TableCell>

              <TableCell>
                Contacto
              </TableCell>

              <TableCell>
                Teléfono
              </TableCell>

              <TableCell>
                Correo
              </TableCell>

              <TableCell>
                Estado
              </TableCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {filteredCustomers.length === 0 ? (
              <TableRow>
                <TableCell
                  colSpan={6}
                  align="center"
                  sx={{
                    py: 6,
                    color: "text.secondary",
                  }}
                >
                  {customers.length === 0
                    ? "No hay clientes registrados."
                    : "No se encontraron clientes con esos filtros."}
                </TableCell>
              </TableRow>
            ) : (
              filteredCustomers.map((customer) => (
                <TableRow
                  key={customer.id}
                  hover
                  onClick={() =>
                    navigate(`/customers/${customer.id}`)
                  }
                  sx={{
                    cursor: "pointer",
                    }}                
                >
                  <TableCell>
                    <Typography
                      sx={{
                        fontWeight: 600,
                      }}
                    >
                      {customer.business_name}
                    </Typography>
                  </TableCell>

                  <TableCell>
                    {customer.rfc ?? "—"}
                  </TableCell>

                  <TableCell>
                    {customer.contact_name ?? "—"}
                  </TableCell>

                  <TableCell>
                    {customer.phone ?? "—"}
                  </TableCell>

                  <TableCell>
                    {customer.email ?? "—"}
                  </TableCell>

                  <TableCell>
                    <Chip
                      size="small"
                      label={
                        customer.status === "ACTIVE"
                          ? "Activo"
                          : "Inactivo"
                      }
                      color={
                        customer.status === "ACTIVE"
                          ? "success"
                          : "default"
                      }
                      variant="outlined"
                    />
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>
      <CreateCustomerDialog
        open={createDialogOpen}
        onClose={() =>
            setCreateDialogOpen(false)
        }
        onCreated={loadCustomers}
        />
    </Box>
  );
}