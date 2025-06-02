import datetime
from typing import List, Optional

from pydantic import BaseModel


class NotificationButton(BaseModel):
    callback_data: str
    text: str
    url: Optional[str] = None

class NotificationFile(BaseModel):
    id: str

class NotificationCreate(BaseModel):
    telegram_id: int
    chat_id: int
    run_time: datetime.datetime
    text: Optional[str] = None
    button: Optional[List[List[NotificationButton]]] = None
    video: Optional[List[NotificationFile]] = None
    photo: Optional[List[NotificationFile]] = None
    audio: Optional[List[NotificationFile]] = None
    document: Optional[List[NotificationFile]] = None
    file: Optional[List[NotificationFile]] = None