import { useEffect, useState } from "react";

import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Alert,
  Box,
  Button,
  Chip,
  CircularProgress,
  Divider,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";

import ExpandMoreOutlined from "@mui/icons-material/ExpandMoreOutlined";

import {
  getOrderRevisions,
  type OrderRevision,
  type OrderRevisionSnapshot,
} from "./ordersApi";

interface Props {
  orderId: string;
  revisionNumber: number;
}

interface ChangeRow {
  key: string;
  concept: string;
  field: string;
  before: string;
  after: string;
}

export default function OrderRevisionsSection({
  orderId,
  revisionNumber,
}: Props) {
  const [revisions, setRevisions] =
    useState<OrderRevision[]>([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] =
    useState<string | null>(null);

  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    let active = true;

    async function loadRevisions() {
      setLoading(true);
      setError(null);

      try {
        const data = await getOrderRevisions(orderId);

        if (!active) return;

        setRevisions(data);
      } catch (err) {
        if (!active) return;

        setError(
          err instanceof Error
            ? err.message
            : "No se pudo cargar el historial.",
        );
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    void loadRevisions();

    return () => {
      active = false;
    };
  }, [orderId, revisionNumber, reloadKey]);

  const visibleRevisions = revisions
    .filter((revision) => revision.revision_number > 0)
    .sort(
      (a, b) =>
        b.revision_number - a.revision_number,
    );

  return (
    <Paper
      variant="outlined"
      sx={{ p: 3, mt: 3 }}
    >
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          flexWrap: "wrap",
          gap: 2,
        }}
      >
        <Typography variant="h2">
          Historial de revisiones
        </Typography>

        <Chip
          label={`${visibleRevisions.length} revisiones`}
          size="small"
          variant="outlined"
        />
      </Box>

      <Divider sx={{ my: 2 }} />

      {loading ? (
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            py: 4,
          }}
        >
          <CircularProgress size={28} />
        </Box>
      ) : error ? (
        <Alert
          severity="error"
          action={
            <Button
              size="small"
              color="inherit"
              onClick={() =>
                setReloadKey((value) => value + 1)
              }
            >
              Reintentar
            </Button>
          }
        >
          {error}
        </Alert>
      ) : visibleRevisions.length === 0 ? (
        <Typography color="text.secondary">
          Esta orden todavía no tiene revisiones.
        </Typography>
      ) : (
        <Stack spacing={1.5}>
          {visibleRevisions.map((revision) => {
            const previous = revisions.find(
              (item) =>
                item.revision_number ===
                revision.revision_number - 1,
            );

            const canCompare =
              Boolean(previous) &&
              Array.isArray(previous?.snapshot.items) &&
              Array.isArray(revision.snapshot.items);

            const changes =
              canCompare && previous
                ? compareSnapshots(
                    previous.snapshot,
                    revision.snapshot,
                  )
                : [];

            return (
              <Accordion
                key={revision.id}
                disableGutters
                elevation={0}
                sx={{
                  border: "1px solid",
                  borderColor: "divider",
                  borderRadius: "8px !important",
                  overflow: "hidden",
                  "&::before": {
                    display: "none",
                  },
                }}
              >
                <AccordionSummary
                  expandIcon={<ExpandMoreOutlined />}
                >
                  <Box sx={{ flex: 1, minWidth: 0 }}>
                    <Typography
                      sx={{ fontWeight: 600 }}
                    >
                      Revisión #{revision.revision_number}
                    </Typography>

                    <Typography
                      variant="body2"
                      color="text.secondary"
                      sx={{ mt: 0.5 }}
                    >
                      {formatDate(revision.created_at)}
                    </Typography>

                    <Typography
                      variant="body2"
                      sx={{ mt: 1 }}
                    >
                      {revision.reason}
                    </Typography>
                  </Box>
                </AccordionSummary>

                <AccordionDetails>
                  <Divider sx={{ mb: 2 }} />

                  <Stack spacing={3}>
                    <Box>
                      <Typography
                        variant="body2"
                        color="text.secondary"
                      >
                        Registrada por
                      </Typography>

                      <Typography
                        sx={{
                          mt: 0.5,
                          overflowWrap: "anywhere",
                        }}
                      >
                        {revision.created_by}
                      </Typography>
                    </Box>

                    {canCompare ? (
                      <>
                        <Box>
                          <Typography
                            sx={{
                              fontWeight: 600,
                              mb: 1.5,
                            }}
                          >
                            Cambios realizados
                          </Typography>

                          {changes.length === 0 ? (
                            <Typography color="text.secondary">
                              No se detectaron cambios en
                              los conceptos entre estas versiones.
                            </Typography>
                          ) : (
                            <Box sx={{ overflowX: "auto" }}>
                              <Table
                                size="small"
                                sx={{ minWidth: 550 }}
                              >
                                <TableHead>
                                  <TableRow>
                                    <TableCell>
                                      Concepto
                                    </TableCell>

                                    <TableCell>
                                      Campo
                                    </TableCell>

                                    <TableCell>
                                      Antes
                                    </TableCell>

                                    <TableCell>
                                      Después
                                    </TableCell>
                                  </TableRow>
                                </TableHead>

                                <TableBody>
                                  {changes.map((change) => (
                                    <TableRow key={change.key}>
                                      <TableCell>
                                        {change.concept}
                                      </TableCell>

                                      <TableCell>
                                        {change.field}
                                      </TableCell>

                                      <TableCell>
                                        {change.before}
                                      </TableCell>

                                      <TableCell
                                        sx={{ fontWeight: 500 }}
                                      >
                                        {change.after}
                                      </TableCell>
                                    </TableRow>
                                  ))}
                                </TableBody>
                              </Table>
                            </Box>
                          )}
                        </Box>

                        <TotalsComparison
                          before={previous!.snapshot}
                          after={revision.snapshot}
                        />
                      </>
                    ) : (
                      <>
                        <Alert severity="info">
                          No tenemos una versión anterior
                          guardada para comparar esta revisión.
                          Se muestra el resultado registrado.
                        </Alert>

                        <SnapshotItems
                          snapshot={revision.snapshot}
                        />

                        <TotalsComparison
                          after={revision.snapshot}
                        />
                      </>
                    )}
                  </Stack>
                </AccordionDetails>
              </Accordion>
            );
          })}
        </Stack>
      )}
    </Paper>
  );
}

function compareSnapshots(
  before: OrderRevisionSnapshot,
  after: OrderRevisionSnapshot,
): ChangeRow[] {
  const changes: ChangeRow[] = [];

  const beforeItems = before.items ?? [];
  const afterItems = after.items ?? [];

  const beforeMap = new Map(
    beforeItems.map((item) => [item.id, item]),
  );

  const afterMap = new Map(
    afterItems.map((item) => [item.id, item]),
  );

  const currency =
    after.currency ?? before.currency;

  for (const item of afterItems) {
    const previous = beforeMap.get(item.id);

    if (!previous) {
      changes.push({
        key: `${item.id}-added`,
        concept: item.description,
        field: "Concepto agregado",
        before: "—",
        after: `${item.quantity} × ${formatMoney(
          item.unit_price,
          item.currency ?? currency,
        )}`,
      });

      continue;
    }

    if (previous.description !== item.description) {
      changes.push({
        key: `${item.id}-description`,
        concept: item.description,
        field: "Descripción",
        before: previous.description,
        after: item.description,
      });
    }

    if (previous.quantity !== item.quantity) {
      changes.push({
        key: `${item.id}-quantity`,
        concept: item.description,
        field: "Cantidad",
        before: String(previous.quantity),
        after: String(item.quantity),
      });
    }

    if (
      Number(previous.unit_price) !==
      Number(item.unit_price)
    ) {
      changes.push({
        key: `${item.id}-unit-price`,
        concept: item.description,
        field: "Precio unitario",
        before: formatMoney(
          previous.unit_price,
          previous.currency ?? before.currency,
        ),
        after: formatMoney(
          item.unit_price,
          item.currency ?? after.currency,
        ),
      });
    }
  }

  for (const item of beforeItems) {
    if (!afterMap.has(item.id)) {
      changes.push({
        key: `${item.id}-removed`,
        concept: item.description,
        field: "Concepto eliminado",
        before: `${item.quantity} × ${formatMoney(
          item.unit_price,
          item.currency ?? before.currency,
        )}`,
        after: "—",
      });
    }
  }

  return changes;
}

function SnapshotItems({
  snapshot,
}: {
  snapshot: OrderRevisionSnapshot;
}) {
  return (
    <Box>
      <Typography
        sx={{
          fontWeight: 600,
          mb: 1.5,
        }}
      >
        Conceptos de esta versión
      </Typography>

      {!snapshot.items?.length ? (
        <Typography color="text.secondary">
          No hay conceptos registrados.
        </Typography>
      ) : (
        <Box sx={{ overflowX: "auto" }}>
          <Table
            size="small"
            sx={{ minWidth: 450 }}
          >
            <TableHead>
              <TableRow>
                <TableCell>
                  Descripción
                </TableCell>

                <TableCell align="right">
                  Cantidad
                </TableCell>

                <TableCell align="right">
                  Precio unitario
                </TableCell>
              </TableRow>
            </TableHead>

            <TableBody>
              {snapshot.items.map((item) => (
                <TableRow key={item.id}>
                  <TableCell>
                    {item.description}
                  </TableCell>

                  <TableCell align="right">
                    {item.quantity}
                  </TableCell>

                  <TableCell align="right">
                    {formatMoney(
                      item.unit_price,
                      item.currency ?? snapshot.currency,
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Box>
      )}
    </Box>
  );
}

function TotalsComparison({
  before,
  after,
}: {
  before?: OrderRevisionSnapshot;
  after: OrderRevisionSnapshot;
}) {
  const rows = [
    {
      label: "Subtotal",
      oldValue: before?.subtotal,
      newValue: after.subtotal,
    },
    {
      label: "Impuesto",
      oldValue: before?.tax,
      newValue: after.tax,
    },
    {
      label: "Total",
      oldValue: before?.total,
      newValue: after.total,
    },
  ];

  return (
    <Box>
      <Typography
        sx={{
          fontWeight: 600,
          mb: 1.5,
        }}
      >
        {before
          ? "Comparación de importes"
          : "Importes de esta versión"}
      </Typography>

      <Box sx={{ overflowX: "auto" }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>
                Concepto
              </TableCell>

              {before && (
                <TableCell align="right">
                  Antes
                </TableCell>
              )}

              <TableCell align="right">
                {before ? "Después" : "Importe"}
              </TableCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {rows.map((row) => (
              <TableRow key={row.label}>
                <TableCell
                  sx={{
                    fontWeight:
                      row.label === "Total" ? 700 : 400,
                  }}
                >
                  {row.label}
                </TableCell>

                {before && (
                  <TableCell align="right">
                    {formatMoney(
                      row.oldValue,
                      before.currency,
                    )}
                  </TableCell>
                )}

                <TableCell
                  align="right"
                  sx={{
                    fontWeight:
                      row.label === "Total" ? 700 : 500,
                  }}
                >
                  {formatMoney(
                    row.newValue,
                    after.currency,
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Box>
    </Box>
  );
}

function formatMoney(
  value: string | number | undefined,
  currency?: string,
): string {
  if (value === undefined || value === null) {
    return "—";
  }

  const amount = Number(value);

  if (!Number.isFinite(amount)) {
    return String(value);
  }

  const formatted = amount.toLocaleString(
    "es-MX",
    {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    },
  );

  return currency
    ? `${currency} ${formatted}`
    : formatted;
}

function formatDate(value: string): string {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return date.toLocaleString("es-MX", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}