import sqlalchemy as sa

from internal.entity.base import Base
from internal.entity.timestamp_mixin import TimestampMixin


class User(TimestampMixin, Base):

    __tablename__ = "users"

    __table_args__ = (
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('refresh_token'),
    )


    email = sa.Column(sa.String(255), nullable=False)
    username = sa.Column(sa.String(255))
    password = sa.Column(sa.String(255), nullable=False)
    refresh_token = sa.Column(sa.String(32))
    disabled = sa.Column(sa.Boolean(), default=False, nullable=False)
