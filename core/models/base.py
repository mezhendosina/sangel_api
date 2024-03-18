from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
import datetime
from typing import Annotated

created = Annotated[datetime.datetime, mapped_column(server_default="now()")]
modified = Annotated[datetime.datetime, mapped_column(
    server_default="now()",
    onupdate=datetime.datetime.now
)]
is_deleted = Annotated[int, mapped_column(default=0,
    server_default="0"
)]


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_time: Mapped[created]
    modified_time: Mapped[modified]
    is_deleted: Mapped[is_deleted]