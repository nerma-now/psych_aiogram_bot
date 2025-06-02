from aiogram.filters.callback_data import CallbackData


class BuyCallback(CallbackData, prefix='buy'):
    plan_id: str