OR-001
Una orden debe pertenecer a un cliente.
OR-002
Una orden debe contener al menos un concepto para ser confirmada.
OR-003
La cantidad de un concepto debe ser mayor a cero.
OR-004
El precio unitario no puede ser negativo.
OR-005
Una orden cancelada no puede modificarse.
OR-006
Los cambios comerciales importantes generan una nueva revisión.
OR-007
Cada revisión debe guardar:
- número de revisión;
- fecha;
- usuario;
- motivo;
- snapshot.
OR-008
El total vigente de la orden se calcula desde sus conceptos actuales.
OR-009
Los gastos no modifican el precio de venta de la orden.
OR-010
La utilidad se calcula como:
venta vigente - gastos acumulados

EX-001: Todo gasto debe pertenecer a una orden.
EX-002: El importe debe ser mayor a cero.
EX-003: El gasto debe tener categoría.
EX-004: El proveedor es opcional.
EX-005: Un gasto cancelado no entra en el cálculo de utilidad.
EX-006: Un gasto cancelado no debe modificarse.
EX-007: La cancelación debe conservar trazabilidad.

SUP-001: nombre obligatorio.
SUP-002: RFC opcional.
SUP-003: contacto, teléfono y correo opcionales.
SUP-004: un proveedor desactivado no debería poder asignarse a nuevos gastos.
SUP-005: desactivar un proveedor no elimina los gastos históricos asociados.

QUO-001
Toda cotización debe pertenecer a un cliente activo.
QUO-002
Cada concepto debe tener cantidad mayor a cero.
QUO-003
El precio no puede ser negativo.
QUO-004
Una cotización debe tener al menos un concepto antes de enviarse.
QUO-005
Una cotización cancelada no puede convertirse en orden.
QUO-006
Una cotización rechazada no puede convertirse en orden.
QUO-007
Solo una cotización aceptada puede convertirse en orden.
QUO-008
El subtotal y total se calculan, no se capturan manualmente.

# Architecture

- DDD + Modular Monolith, no microservicios.
- Frontend y backend separados.
- Python/FastAPI para backend.
- React/TypeScript para frontend.
- PostgreSQL para datos estructurados.
- Object Storage para archivos.
- No guardar PDFs dentro de PostgreSQL.
- No acoplar dominio al proveedor de almacenamiento.
- Orden editable después de acordarse, pero con revisiones.
- Gastos separados de Order.
- Utilidad calculada.
- Una Order puede tener varias invoices.
- No se rastrean pagos individuales.
- Multiusuario desde arquitectura aunque V1 tenga un usuario.