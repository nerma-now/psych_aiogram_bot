from aiogram.fsm.state import State, StatesGroup


class DiaryState(StatesGroup):
    answer = State()