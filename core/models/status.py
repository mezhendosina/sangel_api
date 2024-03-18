from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.mixins import UserRelationMixin


class Status(UserRelationMixin, Base):
    _user_back_populates = "status"

    status_text_id = mapped_column(ForeignKey("status_name.id"), unique=False, nullable=False)
    help_user_id: Mapped[int] = mapped_column(nullable=True)
    status_text = relationship("StatusName", back_populates="statuses")
