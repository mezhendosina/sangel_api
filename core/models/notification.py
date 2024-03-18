from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base


class Notification(Base):

    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"),  nullable=False)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    is_read: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    user_from = relationship("User", back_populates="notification_from", foreign_keys=[user_from_id])
    user_to = relationship("User", back_populates="notification_to", foreign_keys=[user_to_id])

