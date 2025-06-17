from aiogram.filters.callback_data import CallbackData


class StartNextCallback(CallbackData, prefix="start_next"):
    job_id: str