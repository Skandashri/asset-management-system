from fastapi import APIRouter

from app.routers import assets, assignments, users, roles, dashboard, auth, reports, requests

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(roles.router)
api_router.include_router(assets.router)
api_router.include_router(assignments.router)
api_router.include_router(dashboard.router)
api_router.include_router(reports.router)
api_router.include_router(requests.router)

