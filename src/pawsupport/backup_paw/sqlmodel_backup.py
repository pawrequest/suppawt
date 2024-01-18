"""Import and export the database to json on a schedule"""
from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

from sqlmodel import Session, select
from loguru import logger


class SQLModelBot:
    """Backup sqlmodel database to json on a schedule"""

    def __init__(
            self,
            session: Session,
            json_name_to_model_map: dict,
            backup_target: Path,
            restore_target: Path = None,
            output_dir: Path = None,
    ):
        self.backup_target = backup_target
        self.session = session
        self.json_name_to_model_map = json_name_to_model_map
        self.output_dir = output_dir or backup_target.parent
        self.restore_target = restore_target or backup_target

        if self.output_dir.is_file():
            raise FileExistsError("Output directory is a file")
        if not self.output_dir.exists():
            logger.warning(f"Output directory does not exist, creating: {self.output_dir}")
            self.output_dir.mkdir(parents=True, exist_ok=True)

        if self.backup_target.is_dir():
            raise NotImplementedError("Backup Target is a directory")

    @classmethod
    def from_env(cls, session, json_to_model_map, copy_and_prune: bool = True) -> SQLModelBot:
        target = Path(os.environ.get("BACKUP_TARGET", ""))
        restore_target = Path(os.environ.get("RESTORE_TARGET", ""))
        if not target.exists():
            logger.info(f"Backup target does not exist, creating: {target}")
            target.touch(exist_ok=True)
        if not restore_target.exists():
            restore_target = target
            logger.warning(f"Restore target does not exist, using backup target: {target}")

        return cls(
            session=session,
            json_name_to_model_map=json_to_model_map,
            backup_target=target,
            restore_target=restore_target,
        )

    async def run(self, sleep_time: int = 24 * 60 * 60):
        logger.info(f"Initialised, backing up every {sleep_time / 60} minutes")
        while True:
            logger.debug("Waking")
            await self.backup()

            if sleep_time == 0:
                logger.info("One-Time backup complete, exiting")
                raise SystemExit()
            logger.debug(f"Sleeping for {sleep_time} seconds")
            await asyncio.sleep(sleep_time)

    async def backup(self):
        backup_json = await self.make_backup_json()

        if not backup_json:
            logger.info("No models to backup")
            return

        with open(self.backup_target, "w") as f:
            json.dump(backup_json, f, indent=4)
        logger.info(
            f"Saved {sum(len(v) for v in backup_json.values())} models to {self.backup_target}")

        return backup_json

    async def make_backup_json(self, json_map=None, session=None):
        json_map = json_map or self.json_name_to_model_map
        session = session or self.session
        backup_json = {
            model_name_in_json: [_.model_dump_json() for _ in
                                 session.exec(select(model_class)).all()]
            for model_name_in_json, model_class in json_map.items()
        }
        backup_up_model_strs = [f"{len(backup_json[model])} {model}s" for model in backup_json if
                                backup_json[model]]
        logger.info(f"Dumped {', '.join(backup_up_model_strs)} to json")
        return backup_json

    def restore(self, target=None):
        target = target or self.restore_target
        try:
            with open(target, "r") as f:
                backup_j = json.load(f)
        except Exception as e:
            logger.error(f"Error loading json: {e}")
            return

        for json_name, model_class in self.json_name_to_model_map.items():
            added = 0
            for json_string in backup_j.get(json_name):
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
                logger.info(f"Loaded {added} {json_name} from {target}")

        if self.session.new:
            self.session.commit()
