from sqlalchemy.orm import Mapped, mapped_column
import uuid
from database import db


class UserModel(db.Model):
    __tablename__ = 'User'

    id: Mapped[uuid] = mapped_column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str]
    password: Mapped[str]

    def __repr__(self):
        return f"<User {self.email}>"

    @property
    def serialize(self):
        return {
                'id': str(self.id),
                'email': self.email,
                'password': self.password
            }
