from pydantic import BaseModel


class DiaryCreate(BaseModel):
    telegram_id: int
    week: int
    line: int
    answer: str