"""
Import and export SQLModel database session to json once or on a schedule
"""
from __future__ import annotations

import asyncio
import json
from pathlib import Path

from sqlmodel import Session, select
from loguru import logger

from .pruner import Pruner
from ..async_ps import quiet_cancel_as


@quiet_cancel_as
async def backup_copy_prune(backupbot: SQLModelBot, pruner: Pruner, backup_sleep):
    """
    Runs backup, copy, and prune operations in a loop with a specified sleep interval.

    :param backupbot: An instance of SQLModelBot for handling database backup operations.
    :param pruner: An instance of Pruner for handling file pruning operations.
    :param backup_sleep: Time in seconds to wait between each backup operation.
    """
    while True:
        backupbot.backup()
        pruner.copy_and_prune()
        await asyncio.sleep(backup_sleep)


class SQLModelBot:
    """
    Handles backing up of SQLModel database to JSON format, either once or on a schedule.

    :param session: The SQLModel session to be used for database operations.
    :param model_map: A dictionary mapping JSON keys to SQLModel classes.
    :param backup_target: The file path where the backup JSON will be stored.
    :param sleep_time: The interval in seconds between each backup operation. Set to 0 for a one-time backup.
    :param output_dir: The directory where backup JSON files will be saved. Defaults to the parent directory of backup_target.
    :param restore_target: The file path from which to restore backups. Defaults to backup_target.
    """
    def __init__(
            self,
            session: Session,
            model_map: dict,
            backup_target: Path,
            sleep_time: int = 0,
            output_dir: Path = None,
            restore_target: Path = None,
    ):
        self.backup_target = backup_target
        self.session = session
        self.json_key_to_model_map = model_map
        self.output_dir = output_dir or backup_target.parent
        self.restore_target = restore_target or backup_target
        self.sleep_time = sleep_time

        if self.output_dir.is_file():
            raise FileExistsError("Output directory is a file")
        if not self.output_dir.exists():
            logger.warning(f"Output directory does not exist, creating: {self.output_dir}")
            self.output_dir.mkdir(parents=True, exist_ok=True)

        if self.backup_target.is_dir():
            raise NotImplementedError("Backup Target is a directory")

    async def run(self):
        """
        Starts the backup process, either running once or in a continuous loop based on sleep_time.
        """
        sleep_time = self.sleep_time
        logger.info(f"Initialised, backing up every {sleep_time} seconds")
        while True:
            logger.debug("Waking")
            self.backup()

            if sleep_time == 0:
                logger.info("One-Time backup complete, exiting")
                return
            logger.debug(f"Sleeping for {sleep_time} seconds")
            await asyncio.sleep(sleep_time)

    def backup(self):
        """
        Creates a backup of the database models defined in model_map, saving them to backup_target in JSON format.

        :returns: {model name: [model instances] ... }.
        """
        backup_json = self.make_backup_json()

        if not backup_json:
            logger.info("No models to backup")
            return

        with open(self.backup_target, "w") as f:
            json.dump(backup_json, f, indent=4)
        logger.info(
            f"Saved {sum(len(v) for v in backup_json.values())} models to {self.backup_target}",
            category="BACKUP")

        return backup_json

    def make_backup_json(self, json_map=None, session=None):
        """
        Generates a dictionary representing the current state of the database for the models defined in model_map.

        :param json_map: An optional mapping of JSON keys to SQLModel classes. Uses self.json_key_to_model_map if not provided.
        :param session: An optional SQLModel session. Uses self.session if not provided.
        :return: A dictionary where keys are model names and values are lists of model instances in JSON format.
        """
        json_map = json_map or self.json_key_to_model_map
        session = session or self.session
        backup_json = {
            model_name_in_json: [_.model_dump_json() for _ in
                                 session.exec(select(model_class)).all()]
            for model_name_in_json, model_class in json_map.items()
        }
        backup_up_model_strs = [f"{len(backup_json[model])} {model}s" for model in backup_json if
                                backup_json[model]]
        logger.info(f"Dumped {', '.join(backup_up_model_strs)} to json", category="BACKUP")
        return backup_json

    def restore(self, target=None):
        """
        Restores the database state from a JSON file specified by target.

        :param target: The file path from which to restore backups. Defaults to self.restore_target.
        """
        target = target or self.restore_target
        try:
            with open(target, "r") as f:
                backup_j = json.load(f)
        except Exception as e:
            logger.error(f"Error loading json: {e}")
            return

        for json_key, model_class in self.json_key_to_model_map.items():
            added = 0
            for json_string in backup_j.get(json_key):
                json_record = json.loads(json_string)
                model_instance = model_class.model_validate(json_record)

                try:
                    if self.session.get(model_class, model_instance.id):
                        continue

                except AttributeError:
                    if self.session.query(model_class).filter_by(**model_instance.dict()).first():
                        continue

                self.session.add(model_instance)
                added += 1
            if added:
                logger.info(f"Loaded {added} {json_key} from {target}")

        if self.session.new:
            self.session.commit()
