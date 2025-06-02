import uuid

from sqlalchemy import DateTime, UUID, func, text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class IdPkMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

class CreatedAtPkMixin:
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

class LastUpdatedAtPkMixin:
    last_updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )