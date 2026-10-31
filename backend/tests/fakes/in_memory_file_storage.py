from src.documents.application.file_storage import FileStorage


class InMemoryFileStorage(FileStorage):

    def __init__(self):
        self.files = {}

    def upload(
        self,
        object_key: str,
        content: bytes,
        content_type: str,
    ) -> None:
        self.files[object_key] = {
            "content": content,
            "content_type": content_type,
        }

    def delete(self, object_key: str) -> None:
        self.files.pop(object_key, None)