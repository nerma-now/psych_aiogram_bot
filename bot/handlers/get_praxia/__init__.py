from aiogram import Router

from .get_praxia import router as get_praxia_router


router: Router = Router(name=__name__)


router.include_router(get_praxia_router)

__all__ = ["router"]