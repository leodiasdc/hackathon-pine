from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import PrimaryKeyConstraint
import uuid
from datetime import datetime
from database import db


class ChatModel(db.Model):
    __tablename__ = 'Chat'

    id: Mapped[uuid] = mapped_column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    createdAt: Mapped[datetime] = mapped_column(db.DATETIME) # might not be the right format
    title: Mapped[str]
    userId: Mapped[uuid] = mapped_column(db.UUID)
    visibility: Mapped[str] = mapped_column(default='private')

    def __repr__(self):
        return f"<Chat {self.title}>"

    @property
    def serialize(self):
        return {
                'id': str(self.id),
                'createdAt': str(self.createdAt.timestamp()),
                'title': self.title,
                'userId': str(self.userId),
                'visibility': self.visibility
            }


class MessageModel(db.Model):
    __tablename__ = 'Message'

    id: Mapped[uuid] = mapped_column(db.UUID, primary_key=True, default=uuid.uuid4)
    chatId: Mapped[uuid] = mapped_column(db.UUID)
    role: Mapped[str]
    content: Mapped[dict] = mapped_column(db.JSON)
    createdAt: Mapped[datetime]

    @property
    def serialize(self):
        return {
                'id': str(self.id),
                'chatId': str(self.chatId),
                'role': self.role,
                'content': self.content,
                'createdAt': str(self.createdAt.timestamp()),
            }


class VoteModel(db.Model):
    __tablename__ = 'Vote'

    chatId: Mapped[uuid] = mapped_column(db.UUID)
    messageId: Mapped[uuid] = mapped_column(db.UUID)
    isUpvoted: Mapped[bool]

    __table_args__ = (
        PrimaryKeyConstraint(chatId, messageId),
        {}
    )

    @property
    def serialize(self):
        return {
                'chatId': str(self.chatId),
                'messageId': str(self.messageId),
                'isUpvoted': self.isUpvoted,
            }
