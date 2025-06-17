from aiogram.filters.callback_data import CallbackData


class TestChooseCallback(CallbackData, prefix="test_choose"):
    answer: int
    job_id: str
    
class TestAboutCallback(CallbackData, prefix="test_about"):
    pass