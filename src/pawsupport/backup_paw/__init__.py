import asyncio

from .copy_prune import Pruner
from .sqlmodel_backup import SQLModelBot


async def backup_copy_prune(backupbot: SQLModelBot, pruner: Pruner, backup_sleep):
    while True:
        await backupbot.backup()
        await pruner.copy_and_prune()
        await asyncio.sleep(backup_sleep)
