from aiogram.fsm.state import StatesGroup, State


class DeactivateUserState(StatesGroup):
    telegram_id = State()
