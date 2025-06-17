from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import config
from bot.filters import IsAdmin, IsSuperadmin
from bot.handlers.exception_factory import WrongTypeException

from .schemas import SubscriptionPlanCreate
from .state_factory import CreateSubscriptionPlanState
from .exception_factory import LengthException, AmountException

from infrastructure.database.crud import SubscriptionPlanRepository
from infrastructure.database.models import SubscriptionPlan


router: Router = Router(name=__name__)


@router.message(CreateSubscriptionPlanState.title, IsAdmin(), IsSuperadmin())
async def create_subscription_plan_state(message: Message, state: FSMContext):
    if not isinstance(message.text, str) or not message.text or len(message.text) > 256:
        await state.clear()

        raise LengthException()

    await state.update_data(title=message.text)

    await message.answer(_("subscription_get_description"))
    await state.set_state(CreateSubscriptionPlanState.description)


@router.message(CreateSubscriptionPlanState.description, IsAdmin(), IsSuperadmin())
async def create_subscription_plan_state(message: Message, state: FSMContext):
    if (
        not isinstance(message.text, str)
        or not message.text
        or len(message.text) >= 2048
    ):
        await state.clear()

        raise LengthException()

    await state.update_data(description=message.text)

    await message.answer(_("subscription_get_price"))
    await state.set_state(CreateSubscriptionPlanState.price)


@router.message(CreateSubscriptionPlanState.price, IsAdmin(), IsSuperadmin())
async def create_subscription_plan_state(message: Message, state: FSMContext):
    if not isinstance(message.text, str) or not message.text.isdigit():
        await state.clear()

        raise WrongTypeException()

    if (
        int(message.text) < config.payments.min_amount
        or int(message.text) > config.payments.max_amount
    ):
        await state.clear()

        raise AmountException()

    await state.update_data(price=message.text)

    await message.answer(_("subscription_get_total_classes_monthly"))
    await state.set_state(CreateSubscriptionPlanState.total_classes_monthly)


@router.message(
    CreateSubscriptionPlanState.total_classes_monthly, IsAdmin(), IsSuperadmin()
)
async def create_subscription_plan_state(
    message: Message, state: FSMContext, database: AsyncSession
):
    if not isinstance(message.text, str) or not message.text.isdigit():
        await state.clear()

        raise WrongTypeException()

    if int(message.text) < 1:
        await state.clear()

        raise AmountException()

    await state.update_data(total_classes_monthly=message.text)

    schema: SubscriptionPlanCreate = SubscriptionPlanCreate.model_validate(
        await state.get_data()
    )

    await SubscriptionPlanRepository().add(
        session=database, target=SubscriptionPlan(**schema.model_dump())
    )

    await message.answer(_("success"))

    await state.clear()
