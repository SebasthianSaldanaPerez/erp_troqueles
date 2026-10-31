from sqlalchemy.orm import Session

from src.shared.application.unit_of_work import UnitOfWork


class SQLAlchemyUnitOfWork(UnitOfWork):

    def __init__(self, session: Session):
        self._session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.rollback()

        self._session.close()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()