from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class GetOrderProfitabilityQuery:
    order_id: UUID