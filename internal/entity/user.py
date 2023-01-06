import sqlalchemy as sa

from internal.entity.base import Base
from internal.entity.timestamp_mixin import TimestampMixin


class User(Base, TimestampMixin):

    __tablename__ = "users"

    __table_args__ = (
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username'),
    )

    email = sa.Column(sa.String(255), nullable=False)
    username = sa.Column(sa.String(255), nullable=False)
    password = sa.Column(sa.String(255), nullable=False)