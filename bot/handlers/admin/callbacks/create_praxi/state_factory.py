from aiogram.fsm.state import StatesGroup, State


class CreatePraxiState(StatesGroup):
    title = State()
    text = State()
