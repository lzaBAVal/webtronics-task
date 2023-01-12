from datetime import timedelta
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.orm import declarative_base

from internal.config.config import config

import sqlalchemy as sa

from internal.entity.base import Base


class JWTToken(Base):

    __tablename__ = "jwt_token"

    __table_args__ = (
        sa.UniqueConstraint('refresh_token'),
        sa.UniqueConstraint('user_id'),
    )

    refresh_token = sa.Column(sa.String(32), nullable=False)
    ttl = sa.Column(
            sa.DateTime,
            default=sa.func.now() + timedelta(seconds=config.jwt.refresh_expires_sec),
            server_default=sa.FetchedValue(),
            nullable = False
        )
    user_id = sa.Column(psql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False)
