from fastapi import APIRouter
from starlette.middleware.cors import CORSMiddleware

from .users.views import router as users_router
from .contacts.views import router as contacts_router
from .status.views import router as status_names_router
from .auth.views import router as auth_router
from .notifications.views import router as notifications_router

router = APIRouter()
router.include_router(router=users_router, prefix="/users")
router.include_router(router=contacts_router, prefix="/contacts")
router.include_router(router=status_names_router, prefix="/status")
router.include_router(router=auth_router, prefix="/auth")
router.include_router(router=notifications_router, prefix="/notifications")