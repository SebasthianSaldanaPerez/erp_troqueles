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
  getSuppliers,
} from "./suppliersApi";

import type {
  Supplier,
} from "./types";
import CreateSupplierDialog from "./CreateSupplierDialog";
import AddOutlined from "@mui/icons-material/AddOutlined";
import { useAuth } from "../../auth/AuthContext";


export default function SuppliersPage() {
  const navigate = useNavigate();
  const [createDialogOpen, setCreateDialogOpen] =
  useState(false);
  const { user } = useAuth();

  const [suppliers, setSuppliers] =
    useState<Supplier[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  const [search, setSearch] =
    useState("");

  const canEdit =
    user?.role === "ADMIN" ||
    user?.role === "OPERATOR";

  const [statusFilter, setStatusFilter] =
    useState<
      "ALL" | "ACTIVE" | "INACTIVE"
    >("ALL");


  async function loadSuppliers() {
    try {
      setError(null);

      const data =
        await getSuppliers();

      setSuppliers(data);

    } catch {
      setError(
        "No se pudieron cargar los proveedores.",
      );
    } finally {
      setLoading(false);
    }
  }


  useEffect(() => {
    loadSuppliers();
  }, []);


  const filteredSuppliers = suppliers
    .filter((supplier) => {
      const searchText = search
        .trim()
        .toLowerCase();

      const matchesSearch =
        !searchText ||
        supplier.name
          .toLowerCase()
          .includes(searchText) ||
        supplier.rfc
          ?.toLowerCase()
          .includes(searchText) ||
        supplier.contact_name
          ?.toLowerCase()
          .includes(searchText) ||
        supplier.email
          ?.toLowerCase()
          .includes(searchText);

      const matchesStatus =
        statusFilter === "ALL" ||
        supplier.status === statusFilter;

      return (
        matchesSearch &&
        matchesStatus
      );
    })
    .sort((a, b) => {
      if (a.status !== b.status) {
        return a.status === "ACTIVE"
          ? -1
          : 1;
      }

      return a.name.localeCompare(
        b.name,
        "es",
        {
          sensitivity: "base",
        },
      );
    });


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
          Proveedores
        </Typography>

        <Typography
          color="text.secondary"
          sx={{ mt: 0.5 }}
        >
          Consulta y administra los proveedores registrados.
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
          placeholder="Buscar proveedor..."
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
          {filteredSuppliers.length} proveedor
          {filteredSuppliers.length === 1
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
                Proveedor
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
            {filteredSuppliers.length === 0 ? (
              <TableRow>
                <TableCell
                  colSpan={6}
                  align="center"
                  sx={{
                    py: 6,
                    color: "text.secondary",
                  }}
                >
                  {suppliers.length === 0
                    ? "No hay proveedores registrados."
                    : "No se encontraron proveedores con esos filtros."}
                </TableCell>
              </TableRow>
            ) : (
              filteredSuppliers.map(
                (supplier) => (
                  <TableRow
                    key={supplier.id}
                    hover
                    onClick={() =>
                      navigate(
                        `/suppliers/${supplier.id}`,
                      )
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
                        {supplier.name}
                      </Typography>
                    </TableCell>

                    <TableCell>
                      {supplier.rfc ?? "—"}
                    </TableCell>

                    <TableCell>
                      {supplier.contact_name ?? "—"}
                    </TableCell>

                    <TableCell>
                      {supplier.phone ?? "—"}
                    </TableCell>

                    <TableCell>
                      {supplier.email ?? "—"}
                    </TableCell>

                    <TableCell>
                      <Chip
                        size="small"
                        label={
                          supplier.status ===
                          "ACTIVE"
                            ? "Activo"
                            : "Inactivo"
                        }
                        color={
                          supplier.status ===
                          "ACTIVE"
                            ? "success"
                            : "default"
                        }
                        variant="outlined"
                      />
                    </TableCell>
                  </TableRow>
                ),
              )
            )}
          </TableBody>
        </Table>
      </TableContainer>
      <CreateSupplierDialog
        open={createDialogOpen}
        onClose={() =>
          setCreateDialogOpen(false)
        }
        onCreated={loadSuppliers}
      />
    </Box>
  );
}