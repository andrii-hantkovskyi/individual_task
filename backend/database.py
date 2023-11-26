import datetime
import os

from motor.motor_asyncio import AsyncIOMotorClient

import settings

client = AsyncIOMotorClient(settings.DB_URI)
database = client[settings.DB_NAME]


def get_dump_restore_args(datetime_string: str = ''):
    if not datetime_string:
        datetime_string = datetime.datetime.now(tz=settings.TZ).strftime(settings.DATETIME_FORMAT)
    try:
        if datetime.datetime.strptime(datetime_string, settings.DATETIME_FORMAT).strftime(
                settings.DATETIME_FORMAT) != datetime_string:
            raise ValueError('Wrong datetime string')
    except ValueError:
        raise ValueError('Wrong datetime string')
    archive_path = os.path.join(settings.BACKUPS_DIR, f'{datetime_string}.gzip')
    args = f'--db={settings.DB_NAME} --archive={archive_path} --gzip'
    return args


def backup_db():
    args = get_dump_restore_args()
    os.system(f'mongodump {args}')


def restore_db_by_date(datetime_string: str):
    args = get_dump_restore_args(datetime_string)
    os.system(f'mongorestore {args}')
