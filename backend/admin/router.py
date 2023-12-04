from fastapi import APIRouter, HTTPException, Request
from starlette.authentication import UnauthenticatedUser

from admin.services import get_all_db_backup_dates
from database import backup_db, restore_db_by_date
from users.models import RoleTypes

admin_router = APIRouter(prefix='/admin', tags=['admin'])


@admin_router.get('/db-backups')
async def get_db_backup_dates(request: Request):
    if isinstance(request.user, UnauthenticatedUser) or request.user['role'] != RoleTypes.admin.value:
        raise HTTPException(status_code=401)

    return get_all_db_backup_dates()


@admin_router.post('/backup-db', status_code=200)
async def db_backup(request: Request):
    if isinstance(request.user, UnauthenticatedUser) or request.user['role'] != RoleTypes.admin.value:
        raise HTTPException(status_code=401)

    backup_db()


@admin_router.post('/restore-db', status_code=200)
async def restore_db(request: Request):
    if isinstance(request.user, UnauthenticatedUser) or request.user['role'] != RoleTypes.admin.value:
        raise HTTPException(status_code=401)
    body = await request.json()
    try:
        date = body['date']
        restore_db_by_date(date)
    except (ValueError, KeyError):
        raise HTTPException(status_code=400, detail='Wrong date')
