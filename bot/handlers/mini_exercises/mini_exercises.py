from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

from bot.filters import ActiveSubscription

from .callback_factory import MiniExercisesCallback, MiniExercisesType


router: Router = Router(
    name=__name__
)

@router.message(
    F.text.func(lambda text: text == _('menu_problems_keyboard')),
    ActiveSubscription()
)
async def menu_problems_command(message: Message):
    await message.answer(
        'Выберите необходимое мини-упражнение:',
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=_('anxiety_user_keyboard'),
                        callback_data=MiniExercisesCallback(
                            type=MiniExercisesType.anxiety
                        ).pack()
                    ),
                    InlineKeyboardButton(
                        text=_('apathy_user_keyboard'),
                        callback_data=MiniExercisesCallback(
                            type=MiniExercisesType.apathy
                        ).pack()
                    ),
                    InlineKeyboardButton(
                        text=_('loneliness_user_keyboard'),
                        callback_data=MiniExercisesCallback(
                            type=MiniExercisesType.loneliness
                        ).pack()
                    ),
                    InlineKeyboardButton(
                        text=_('humiliation_user_keyboard'),
                        callback_data=MiniExercisesCallback(
                            type=MiniExercisesType.humiliation
                        ).pack()
                    )
                ]
            ]
        )
    )

@router.callback_query(
    MiniExercisesCallback.filter(F.type == MiniExercisesType.apathy),
    ActiveSubscription()
)
async def apathy_callback(
    query: CallbackQuery
):
    await query.message.answer(_('apathy_mini_exercises'))

@router.callback_query(
    MiniExercisesCallback.filter(F.type == MiniExercisesType.humiliation),
    ActiveSubscription()
)
async def humiliation_callback(
    query: CallbackQuery
):
    await query.message.answer(_('humiliation_mini_exercises'))

@router.callback_query(
    MiniExercisesCallback.filter(F.type == MiniExercisesType.anxiety),
    ActiveSubscription()
)
async def anxiety_callback(
    query: CallbackQuery
):
    await query.message.answer(_('anxiety_mini_exercises'))

@router.callback_query(
    MiniExercisesCallback.filter(F.type == MiniExercisesType.loneliness),
    ActiveSubscription()
)
async def loneliness_callback(
    query: CallbackQuery
):
    await query.message.answer(_('loneliness_mini_exercises'))

__all__ = ['router']