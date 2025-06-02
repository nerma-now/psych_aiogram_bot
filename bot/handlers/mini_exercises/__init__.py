from aiogram import Router

from .mini_exercises import router as mini_exercises_router


router: Router = Router(
    name=__name__
)
router.include_router(mini_exercises_router)

__all__ = ['router']