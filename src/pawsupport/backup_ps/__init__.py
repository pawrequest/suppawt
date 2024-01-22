import asyncio

from .copy_prune import Pruner
from .sqlmodel_backup import SQLModelBot
from ..async_ps import quiet_cancel_as


@quiet_cancel_as
async def backup_copy_prune(backupbot: SQLModelBot, pruner: Pruner, backup_sleep):
    while True:
        await backupbot.backup()
        pruner.copy_and_prune()
        await asyncio.sleep(backup_sleep)
