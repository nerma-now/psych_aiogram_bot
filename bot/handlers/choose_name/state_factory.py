from aiogram.fsm.state import State, StatesGroup


class ChooseNameState(StatesGroup):
    name = State()