from aiogram.filters.callback_data import CallbackData


class CanceledSubscriptionCallback(CallbackData, prefix="canceled_subscription"):
    pass