from abc import ABC, abstractmethod


class FileStorage(ABC):

    @abstractmethod
    def upload(
        self,
        object_key: str,
        content: bytes,
        content_type: str,
    ) -> None:
        pass

    @abstractmethod
    def delete(self, object_key: str) -> None:
        pass