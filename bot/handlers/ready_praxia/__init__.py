from aiogram import Router

from .ready_praxia import router as ready_praxia_router


router: Router = Router()


router.include_router(ready_praxia_router)

__all__ = ['router']