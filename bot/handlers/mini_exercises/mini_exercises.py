from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaAudio,
    InputMediaVideo,
    BufferedInputFile,
)
from aiogram.utils.i18n import gettext as _

from bot.filters import ActiveSubscription
from bot.config.constants import MAIN_DIR

from .callback_factory import MiniExercisesCallback, MiniExercisesType


router: Router = Router(name=__name__)


@router.message(
    F.text.func(lambda text: text == _("menu_problems_keyboard")), ActiveSubscription()
)
async def menu_problems_command(message: Message):
    await message.answer(
        "Выберите необходимое мини-упражнение:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=_("anxiety_user_keyboard"),
                        callback_data=MiniExercisesCallback(
                            type=MiniExercisesType.anxiety
                        ).pack(),
                    ),
                    InlineKeyboardButton(
                        text=_("apathy_user_keyboard"),
                        callback_data=MiniExercisesCallback(
                            type=MiniExercisesType.apathy
                        ).pack(),
                    ),
                    InlineKeyboardButton(
                        text=_("loneliness_user_keyboard"),
                        callback_data=MiniExercisesCallback(
                            type=MiniExercisesType.loneliness
                        ).pack(),
                    ),
                    InlineKeyboardButton(
                        text=_("humiliation_user_keyboard"),
                        callback_data=MiniExercisesCallback(
                            type=MiniExercisesType.humiliation
                        ).pack(),
                    ),
                ]
            ]
        ),
    )


@router.callback_query(
    MiniExercisesCallback.filter(F.type == MiniExercisesType.apathy),
    ActiveSubscription(),
)
async def apathy_callback(query: CallbackQuery):
    await query.message.answer(_("apathy_mini_exercises"))


@router.callback_query(
    MiniExercisesCallback.filter(F.type == MiniExercisesType.humiliation),
    ActiveSubscription(),
)
async def humiliation_callback(query: CallbackQuery):
    await query.message.answer(_("humiliation_mini_exercises"))


@router.callback_query(
    MiniExercisesCallback.filter(F.type == MiniExercisesType.anxiety),
    ActiveSubscription(),
)
async def anxiety_callback(query: CallbackQuery):
    try:
        with open(MAIN_DIR.joinpath("resource").joinpath("anxiety.MOV"), "rb") as f:
            video_file: BufferedInputFile = BufferedInputFile(
                file=f.read(), filename="video.MOV"
            )

        await query.message.answer_video(
            video=video_file,
            caption=_("anxiety_mini_exercises"),
        )
    except:
        await query.message.answer(_("anxiety_mini_exercises"))


@router.callback_query(
    MiniExercisesCallback.filter(F.type == MiniExercisesType.loneliness),
    ActiveSubscription(),
)
async def loneliness_callback(query: CallbackQuery):
    try:
        with open(MAIN_DIR.joinpath("resource").joinpath("loneliness.mp3"), "rb") as f:
            audio_file: BufferedInputFile = BufferedInputFile(
                file=f.read(), filename="audio.mp3"
            )

        await query.message.answer_audio(
            audio=audio_file,
            caption=_("loneliness_mini_exercises"),
        )
    except:
        await query.message.answer(_("loneliness_mini_exercises"))


__all__ = ["router"]
