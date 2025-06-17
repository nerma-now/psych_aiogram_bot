from aiogram.fsm.state import StatesGroup, State


class GiveSubscriptionState(StatesGroup):
    telegram_id = State()
    subscription_id = State()
    count_days = State()
