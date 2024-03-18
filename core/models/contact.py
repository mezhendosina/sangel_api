from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.mixins import UserRelationMixin


class Contact(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    contact_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="my_contacts", foreign_keys=[user_id])
    contact_user = relationship("User", back_populates="for_contacts", foreign_keys=[contact_user_id])

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, user_id={self.user_id})"

    def __repr__(self):
        return str(self)