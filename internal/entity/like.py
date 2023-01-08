import sqlalchemy as sa

from sqlalchemy.dialects import postgresql as psql

from internal.entity.base import Base
from internal.entity.timestamp_mixin import TimestampMixin


class Like(Base, TimestampMixin):
    __tablename__ = "likes"

    likes = sa.Column(
        sa.BigInteger, 
        server_default='0',
        nullable=False)

    dislikes = sa.Column(
        sa.BigInteger, 
        server_default='0',
        nullable=False)

    user_id = sa.Column(psql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False)
    post_id = sa.Column(psql.UUID(as_uuid=True), sa.ForeignKey('posts.id'), nullable=False)
