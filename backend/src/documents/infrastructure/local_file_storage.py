from pathlib import Path

from src.documents.application.file_storage import FileStorage


class LocalFileStorage(FileStorage):

    def __init__(self, base_path: str = "storage"):
        self._base_path = Path(base_path)

    def upload(
        self,
        object_key: str,
        content: bytes,
        content_type: str,
    ) -> None:
        path = self._base_path / object_key

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_bytes(content)

    def delete(
        self,
        object_key: str,
    ) -> None:
        path = self._base_path / object_key

        if path.exists():
            path.unlink()

    def read(
        self,
        object_key: str,
    ) -> bytes:
        path = self._base_path / object_key

        if not path.exists():
            raise FileNotFoundError(object_key)

        return path.read_bytes()

    def get_path(self, object_key: str) -> Path:
        return self._base_path / object_key