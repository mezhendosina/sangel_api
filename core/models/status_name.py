from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base, Status


class StatusName(Base):
    __tablename__ = 'status_name'

    text: Mapped[str] = mapped_column(String, nullable=False)
    statuses: Mapped[list["Status"] | None] = relationship(back_populates="status_text")