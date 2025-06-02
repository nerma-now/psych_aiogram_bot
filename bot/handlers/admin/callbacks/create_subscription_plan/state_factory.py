from aiogram.fsm.state import StatesGroup, State


class CreateSubscriptionPlanState(StatesGroup):
    title = State()
    description = State()
    price = State()
    total_classes_monthly = State()