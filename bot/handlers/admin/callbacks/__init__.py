from aiogram import Router

from .set_admin import router as set_admin_router
from .remove_admin import router as remove_admin_router
from .stats_subscription import router as stats_subscription_router
from .create_subscription import router as create_subscription_router
from .activate_user import router as activate_user_router
from .deactivate_user import router as deactivate_user_router
from .user_test import router as last_user_test_router
from .give_subscription import router as give_subscription_router
from .deactivate_subscription import router as deactivate_subscription_router
from .set_premium_subscription import router as set_premium_subscription_router
from .remove_premium_subscription import router as remove_premium_subscription_router
from .create_praxi import router as create_praxi_router
from .all_files import router as all_file_router
from .upload_files import router as upload_files_router
from .delete_files import router as delete_files_router


router: Router = Router(name=__name__)


router.include_router(set_admin_router)
router.include_router(remove_admin_router)
router.include_router(create_subscription_router)
router.include_router(stats_subscription_router)
router.include_router(activate_user_router)
router.include_router(deactivate_user_router)
router.include_router(last_user_test_router)
router.include_router(give_subscription_router)
router.include_router(deactivate_subscription_router)
router.include_router(set_premium_subscription_router)
router.include_router(remove_premium_subscription_router)
router.include_router(create_praxi_router)
router.include_router(all_file_router)
router.include_router(delete_files_router)
router.include_router(upload_files_router)

__all__ = ["router"]
