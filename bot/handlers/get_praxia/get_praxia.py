from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.i18n import gettext as _

from typing import Optional

from bot.loader import BotLoader
from bot.filters import ExistUser, TextOrCommandFilter

from sqlalchemy.ext.asyncio import AsyncSession

from .callback_factory import GetPraxiaCallback
from .schemas import ReceivePraxiCreate

from bot.handlers.admin.callbacks.all_files.utils import send_praxi_file
from bot.handlers.ready_praxia.callback_factory import ReadyPraxiaCallback

from infrastructure.database.crud import PraxiRepository, ReceivePraxiRepository, PraxiFilesRepository
from infrastructure.database.models import Praxi, ReceivePraxi, PraxiFiles


router: Router = Router(name=__name__)


@router.message(TextOrCommandFilter(text_key="menu_praxi_keyboard", command="praxi"))
async def get_praxia_callback(message: Message, database: AsyncSession):
    receive_praxi: Optional[ReceivePraxi] = await ReceivePraxiRepository().get_last_uncompleted_test(
        session=database,
        telegram_id=message.from_user.id
    )
    all_praxi: Optional[Praxi] = await ReceivePraxiRepository().get_last(
        session=database,
        target=ReceivePraxi.telegram_id,
        value=message.from_user.id
    )
    print(receive_praxi, 1)

    if receive_praxi is not None:
        print(2)
        praxi: Optional[Praxi] = await PraxiRepository().get(
            session=database,
            target=Praxi.id,
            value=receive_praxi.praxi_id
        )

        if praxi is None:
            await message.answer("Упражнение не найдено")

            return
        
        try:
            praxi_files = await PraxiFilesRepository().get_current_all(
                session=database, target=PraxiFiles.praxi_id, value=praxi.id
            )

            if praxi:
                for pr in praxi_files:
                    await send_praxi_file(BotLoader().bot, message.chat.id, pr)
        except Exception as e:
            pass

        await message.answer(
            "<b>ЗАВЕРШИТЕ ПРЕДЫДУЮЩЕЕ УПРАЖНЕНИЕ</b>\n\n" + praxi.text,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=_("ready_praxia_keyboard"),
                            callback_data=ReadyPraxiaCallback().pack(),
                        )
                    ]
                ]
            ),
        )

        return
    
    receive_praxi = await ReceivePraxiRepository().get_last(
        session=database,
        target=ReceivePraxi.telegram_id,
        value=message.from_user.id
    )
    print(receive_praxi.id, 3)

    if all_praxi is None:
        print(4)
        praxi: Optional[Praxi] = await PraxiRepository().get_first(
            session=database,
        )

        if praxi is None:
            await message.message.answer(_("praxi_not_found"))

        try:
            praxi_files = await PraxiFilesRepository().get_current_all(
                session=database, target=PraxiFiles.praxi_id, value=praxi.id
            )

            if praxi:
                for pr in praxi_files:
                    await send_praxi_file(BotLoader().bot, message.chat.id, pr)
        except Exception as e:
            pass

        receive_praxi_create: ReceivePraxiCreate = ReceivePraxiCreate(
            telegram_id=message.from_user.id, praxi_id=praxi.id
        )
        await ReceivePraxiRepository().add(
            session=database, target=ReceivePraxi(**receive_praxi_create.model_dump())
        )

        await message.answer(
            praxi.text,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=_("ready_praxia_keyboard"),
                            callback_data=ReadyPraxiaCallback().pack(),
                        )
                    ]
                ]
            ),
        )
        return

    next_praxi: Optional[Praxi] = await PraxiRepository().get_next_praxi(
        session=database,
        telegram_id=message.from_user.id
    )

    if next_praxi is None:
        await message.answer(_("praxi_not_found"))

    try:
        next_praxi_files = await PraxiFilesRepository().get_current_all(
            session=database, target=PraxiFiles.praxi_id, value=praxi.id
        )

        if next_praxi:
            for pr in next_praxi_files:
                await send_praxi_file(BotLoader().bot, message.chat.id, pr)
    except Exception as e:
        pass

    receive_praxi_create: ReceivePraxiCreate = ReceivePraxiCreate(
        telegram_id=message.from_user.id, praxi_id=next_praxi.id
    )
    await ReceivePraxiRepository().add(
        session=database, target=ReceivePraxi(**receive_praxi_create.model_dump())
    )

    await message.answer(
        next_praxi.text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=_("ready_praxia_keyboard"),
                        callback_data=ReadyPraxiaCallback().pack(),
                    )
                ]
            ]
        ),
    )


@router.callback_query(
    GetPraxiaCallback.filter(),
    ExistUser(),
)
async def get_praxia_callback(query: CallbackQuery, database: AsyncSession):
    receive_praxi: Optional[ReceivePraxi] = await ReceivePraxiRepository().get(
        session=database, target=ReceivePraxi.telegram_id, value=query.from_user.id
    )

    if receive_praxi is not None:
        await query.message.answer(_("praxi_not_right"))

        return

    praxi: Optional[Praxi] = await PraxiRepository().get_first(
        session=database,
    )

    if praxi is None:
        await query.message.answer(_("praxi_not_found"))

        return

    try:
        praxi_files = await PraxiFilesRepository().get_current_all(
            session=database, target=PraxiFiles.praxi_id, value=praxi.id
        )
    except Exception as e:
        pass

    if praxi:
        for pr in praxi_files:
            await send_praxi_file(BotLoader().bot, query.message.chat.id, pr)

    receive_praxi_create: ReceivePraxiCreate = ReceivePraxiCreate(
        telegram_id=query.from_user.id, praxi_id=praxi.id
    )
    await ReceivePraxiRepository().add(
        session=database, target=ReceivePraxi(**receive_praxi_create.model_dump())
    )

    await query.message.answer(
        praxi.text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=_("ready_praxia_keyboard"),
                        callback_data=ReadyPraxiaCallback().pack(),
                    )
                ]
            ]
        ),
    )


__all__ = ["router"]
