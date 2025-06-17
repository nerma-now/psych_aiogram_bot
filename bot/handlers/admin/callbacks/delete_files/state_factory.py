from aiogram.fsm.state import StatesGroup, State


class DeleteFilesState(StatesGroup):
    file_id = State()
