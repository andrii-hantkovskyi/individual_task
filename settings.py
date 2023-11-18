from os import PathLike
from pathlib import Path

from environs import Env

env = Env()
env.read_env()

BASE_DIR: PathLike[str] = Path(__file__).resolve().parent.parent

SECRET_TOKEN: str = env.str('SECRET_TOKEN')

DB_URI: str = env.str('DB_URI')

ORIGINS: list[str] = env.list('ORIGINS')
