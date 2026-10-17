from abc import ABC, abstractmethod
from uuid import UUID

from .customer import Customer


class CustomerRepository(ABC):

    @abstractmethod
    def save(self, customer: Customer) -> None:
        pass

    @abstractmethod
    def get_by_id(self, customer_id: UUID) -> Customer | None:
        pass