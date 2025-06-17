from aiogram.fsm.state import StatesGroup, State


class UploadFilesState(StatesGroup):
    praxi_id = State()
    file = State()
