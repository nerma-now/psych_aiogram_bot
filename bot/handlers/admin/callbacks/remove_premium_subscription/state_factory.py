from aiogram.fsm.state import StatesGroup, State


class RemovePremiumState(StatesGroup):
    subscription_plan_id = State()
