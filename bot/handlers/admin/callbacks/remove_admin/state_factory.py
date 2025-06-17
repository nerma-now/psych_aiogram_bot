from aiogram.fsm.state import StatesGroup, State


class RemoveAdminState(StatesGroup):
    telegram_id = State()
