from aiogram.fsm.state import StatesGroup, State


class SetAdminState(StatesGroup):
    telegram_id = State()