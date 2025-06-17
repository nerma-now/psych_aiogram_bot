import uuid
from enum import StrEnum

from sqlalchemy import (
    String,
    Integer,
    UUID,
    ForeignKey,
    LargeBinary,
)
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.mixins import (
    IdPkMixin,
    CreatedAtPkMixin,
    LastUpdatedAtPkMixin,
)

from .base import Base


class FileCategory(StrEnum):
    AUDIO = "audio"
    VIDEO = "video"
    DOCUMENT = "document"
    PHOTO = "photo"
    OTHER = "other"


class PraxiFiles(IdPkMixin, CreatedAtPkMixin, LastUpdatedAtPkMixin, Base):
    __tablename__ = "praxi_files"

    praxi_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("praxis.id"), nullable=False
    )
    file_name: Mapped[String] = mapped_column(String(255), nullable=False)
    file_type: Mapped[String] = mapped_column(String(50), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[FileCategory] = mapped_column(String(15), nullable=False)
    content: Mapped[BYTEA] = mapped_column(LargeBinary, nullable=False)


__all__ = ["PraxiFiles"]
