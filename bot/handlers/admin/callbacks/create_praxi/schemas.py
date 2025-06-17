from pydantic import BaseModel


class PraxiCreate(BaseModel):
    title: str
    text: str