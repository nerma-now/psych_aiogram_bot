from pydantic import BaseModel


class TestCreate(BaseModel):
    telegram_id: int