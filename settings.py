from os import PathLike
from pathlib import Path

from environs import Env

env = Env()
env.read_env()

BASE_DIR: PathLike[str] = Path(__file__).resolve().parent.parent

SECRET_TOKEN: str = env.str('SECRET_TOKEN')
JWT_ALGORITHM = 'HS256'

DB_URI: str = env.str('DB_URI')

ORIGINS: list[str] = env.list('ORIGINS')

DEBUG: bool = env.bool('DEBUG')

if DEBUG:
    ADMIN_TOKEN = env.str('ADMIN_TOKEN')
