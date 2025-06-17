from aiogram.fsm.state import StatesGroup, State


class SetPremiumState(StatesGroup):
    subscription_plan_id = State()
