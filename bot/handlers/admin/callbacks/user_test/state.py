from typing import Optional

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.crud import UserRepository, TestRepository
from infrastructure.database.models import User, Test

from bot.filters import IsAdmin
from bot.handlers.exception_factory import (
    WrongTypeException,
    NotFoundException,
    OneSelfException,
)
from bot.handlers.test.utils import generate_test_results, get_test_interpretation

from .exception_factory import NotFoundCompeletedException
from .state_factory import LastUserTestState


router: Router = Router(name=__name__)


@router.message(LastUserTestState.telegram_id, IsAdmin())
async def last_user_test_state(
    message: Message, state: FSMContext, database: AsyncSession
):
    if not isinstance(message.text, str) or not message.text.isdigit():
        await state.clear()

        raise WrongTypeException()

    if int(message.text) == message.from_user.id:
        await state.clear()

        raise OneSelfException()

    user: Optional[User] = await UserRepository().get(
        session=database, target=User.telegram_id, value=int(message.text)
    )

    if not user:
        await state.clear()

        raise NotFoundException()

    test: Optional[Test] = await TestRepository().get_last_completed(
        session=database, target=Test.telegram_id, value=int(message.text)
    )

    if not test:
        await state.clear()

        raise NotFoundCompeletedException()

    await message.answer(
        _("test_completed_result").format(
            user_id=test.telegram_id,
            result=generate_test_results(
                answers=get_test_interpretation(test=test),
            ),
            answers="\n".join(
                f"{i}) {get_test_interpretation(test=test).get(i, 0)}"
                for i in range(
                    1, max(get_test_interpretation(test=test).keys() or [0]) + 1
                )
            ),
            start_date=test.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            end_date=test.completed_at.strftime("%m/%d/%Y, %H:%M:%S"),
        )
    )

    await state.clear()


__all__ = ["router"]
