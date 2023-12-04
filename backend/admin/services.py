import os

import settings


def get_all_db_backup_dates():
    return [file.split('.gzip')[0] for file in os.listdir(settings.BACKUPS_DIR)]
