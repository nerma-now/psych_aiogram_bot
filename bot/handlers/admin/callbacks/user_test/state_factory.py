from aiogram.fsm.state import StatesGroup, State


class LastUserTestState(StatesGroup):
    telegram_id = State()
