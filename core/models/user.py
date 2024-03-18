from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Status
from core.models.base import Base
from core.models.contact import Contact
from core.models.notification import Notification


class User(Base):

    name: Mapped[str] = mapped_column(String(32), nullable=False)
    surname: Mapped[str] = mapped_column(String(32), nullable=False)
    email: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    device_id: Mapped[str] = mapped_column(Integer, nullable=True)
    image: Mapped[str] = mapped_column(String, nullable=True)
    access: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    code: Mapped[str] = mapped_column(String(6), nullable=False)
    my_contacts: Mapped[list["Contact"] | None] = relationship(back_populates="user",
                                                                        primaryjoin="User.id == Contact.user_id")
    for_contacts: Mapped[list["Contact"] | None] = relationship(back_populates="contact_user",
                                                                        primaryjoin="User.id == Contact.contact_user_id")
    status: Mapped["Status"] = relationship(back_populates="user")
    notification_to: Mapped[list["Notification"] | None] = relationship(back_populates="user_from",
                                                                        primaryjoin="User.id == Notification.user_from_id")
    notification_from: Mapped[list["Notification"] | None] = relationship(back_populates="user_to", primaryjoin="User.id == Notification.user_to_id")


    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r}), name={self.surname!r})"

    def __repr__(self):
        return str(self)
