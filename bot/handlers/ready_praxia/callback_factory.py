from aiogram.filters.callback_data import CallbackData
from infrastructure.database.models.receive_praxi import ReceivePraxiRating


class ReadyPraxiaCallback(CallbackData, prefix="ready_praxi"):
    pass

class RatingPraxiaCallback(CallbackData, prefix="rating_praxia"):
    rating: ReceivePraxiRating