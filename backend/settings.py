import os.path
from os import PathLike
from pathlib import Path

import pytz
from environs import Env

env = Env()
env.read_env()

BASE_DIR: PathLike[str] = Path(__file__).resolve().parent.parent
BACKUPS_DIR = os.path.join(BASE_DIR, 'backups')

SECRET_TOKEN: str = env.str('SECRET_TOKEN')
JWT_ALGORITHM = 'HS256'

DB_URI: str = env.str('DB_URI')
DB_NAME: str = env.str('DB_NAME')

ORIGINS: list[str] = env.list('ORIGINS')

DEBUG: bool = env.bool('DEBUG')

if DEBUG:
    ADMIN_TOKEN = env.str('ADMIN_TOKEN')
    ADVANCED_TOKEN = env.str('ADVANCED_TOKEN')
    USER_TOKEN = env.str('USER_TOKEN')

TZ = pytz.timezone(env.str('TZ'))
DATE_FORMAT = env.str('DATE_FORMAT')
DATETIME_FORMAT = env.str('DATETIME_FORMAT')
