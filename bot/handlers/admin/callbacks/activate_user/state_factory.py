from aiogram.fsm.state import StatesGroup, State


class ActivateUserState(StatesGroup):
    telegram_id = State()