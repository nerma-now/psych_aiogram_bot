from pydantic import BaseModel

from uuid import UUID

from infrastructure.database.models.praxi_file import FileCategory


class FileCreate(BaseModel):
    praxi_id: UUID
    file_name: str
    file_type: str
    file_size: int
    category: FileCategory
    content: bytes