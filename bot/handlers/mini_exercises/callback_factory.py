from enum import Enum

from aiogram.filters.callback_data import CallbackData


class MiniExercisesType(str, Enum):
    anxiety = 'anxiety'
    apathy = 'apathy'
    loneliness = 'loneliness'
    humiliation = 'humiliation'

class MiniExercisesCallback(CallbackData, prefix='mini_exercises'):
    type: MiniExercisesType