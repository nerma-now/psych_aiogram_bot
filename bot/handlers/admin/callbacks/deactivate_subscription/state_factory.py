from aiogram.fsm.state import StatesGroup, State


class DeactivateSubscriptionState(StatesGroup):
    telegram_id = State()
