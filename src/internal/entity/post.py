import sqlalchemy as sa

from sqlalchemy.dialects import postgresql as psql

from internal.entity.base import Base
from internal.entity.timestamp_mixin import TimestampMixin


class Post(Base, TimestampMixin):
    __tablename__ = "posts"

    __table_args__ = (
        sa.UniqueConstraint('title'),
    )

    title = sa.Column(sa.String(255), nullable=False)
    text = sa.Column(sa.Text(), nullable=False)
    user_id = sa.Column(psql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False)
