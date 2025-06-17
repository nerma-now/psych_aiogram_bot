from typing import Optional, List, Type, TypeVar, Tuple, Any

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaVideo,
    InputMedia,
    InputMediaPhoto,
    InputMediaAudio,
    InputMediaDocument,
)

from apscheduler.job import Job
from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.date import DateTrigger

from bot.loader import BotLoader

from .abc import AbstractRepository
from .schemas import NotificationCreate, NotificationButton, NotificationFile


class NotificationRepository(AbstractRepository):
    provider = BotLoader().scheduler
    T: TypeVar = TypeVar("T", bound=InputMedia)

    def add(
        self,
        notification_create: NotificationCreate,
        id: Optional[str] = None,
        trigger: BaseTrigger = DateTrigger(),
    ) -> Job:
        job: Job = self.provider.add_job(
            func=self.send,
            trigger=trigger,
            args=[notification_create],
            next_run_time=notification_create.run_time,
        )

        return job

    def delete(self, job_id: str) -> None:
        self.provider.remove_job(job_id)

    def modify(self, job_id: str, **changes) -> None:
        self.provider.modify_job(job_id=job_id, **changes)

    async def send(self, notification_create: NotificationCreate) -> None:
        reply_markup: Optional[InlineKeyboardMarkup] = self._get_keyboard(
            notification_create.button
        )

        for media in self._get_media_groups(notification=notification_create):
            if not media:
                break

            await BotLoader().bot.send_media_group(
                chat_id=notification_create.telegram_id, media=media
            )

        await BotLoader().bot.send_message(
            chat_id=notification_create.chat_id,
            text=notification_create.text,
            reply_markup=reply_markup,
        )

    @staticmethod
    def _create_media_group(
        media_type: Type[T], files: Optional[List[NotificationFile]]
    ) -> Optional[List[T]]:
        if not files:
            return None

        return [media_type(media=file.id) for file in files]

    @staticmethod
    def _get_media_groups(
        notification: NotificationCreate,
    ) -> List[
        Optional[
            List[
                InputMediaAudio | InputMediaDocument | InputMediaPhoto | InputMediaVideo
            ]
        ]
    ]:
        media_mapping: List[Tuple[Type[InputMedia], Any]] = [
            (InputMediaVideo, notification.video),
            (InputMediaPhoto, notification.photo),
            (InputMediaAudio, notification.audio),
            (InputMediaDocument, notification.document),
            (InputMediaDocument, notification.file),
        ]

        media_group: List[
            Optional[
                List[
                    InputMediaAudio
                    | InputMediaDocument
                    | InputMediaPhoto
                    | InputMediaVideo
                ]
            ]
        ] = list()

        for media_type, files in media_mapping:
            media: Optional[List[Type[InputMedia]]] = (
                NotificationRepository._create_media_group(
                    media_type=media_type, files=files
                )
            )

            media_group.append(media)

        return media_group

    @staticmethod
    def _get_media_files(media_type: Type[T], files: Optional[List[NotificationFile]]):
        if not files:
            return None

        media: List[media_type] = list()

        for item in files:
            media.append(media_type(media=item.id))

        return media

    @staticmethod
    def _get_keyboard(
        keyboard: Optional[List[List[NotificationButton]]],
    ) -> Optional[InlineKeyboardMarkup]:
        if not keyboard:
            return None

        inline_keyboard: List[List[InlineKeyboardButton]] = list()

        for row in keyboard:
            buttons: List[InlineKeyboardButton] = list()

            for button in row:
                buttons.append(
                    InlineKeyboardButton(
                        text=button.text,
                        callback_data=button.callback_data,
                        url=button.url,
                    )
                )

            inline_keyboard.append(buttons)

        return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


__all__ = ["NotificationRepository"]
