"""
Copy and prune backups - keep a certain number of daily, weekly, monthly, and yearly backups of the target file
"""
from __future__ import annotations
import shutil
from datetime import datetime
from pathlib import Path
from typing import Literal, NamedTuple

from loguru import logger


class Pruner(object):
    """
    :param backup_target: The file to back up.
    :param output_dir: The directory where backups will be stored. Defaults to the parent directory of the target.
    :param day_retain: The number of daily backups to retain.
    :param week_retain: The number of weekly backups to retain.
    :param month_retain: The number of monthly backups to retain.
    :param year_retain: The number of yearly backups to retain.
    :param _always_copy: Do all backups regardless of date(debug/testing).
    :param _backup_date: Date to use in filenames. Defaults to today (debug/testing).
    """

    def __init__(
            self,
            backup_target: Path,
            output_dir: Path = None,
            day_retain=7,
            week_retain=4,
            month_retain=12,
            year_retain=5,
            _always_copy=False,
            _backup_date=None,
    ):
        self.backup_target = backup_target
        self.output_dir = output_dir or backup_target.parent
        self.always_copy = _always_copy
        self.backup_date = _backup_date if _backup_date else datetime.now().strftime("%Y-%m-%d")
        self.retention_tuples = [
            RetentionPeriod("day", day_retain),
            RetentionPeriod("week", week_retain),
            RetentionPeriod("month", month_retain),
            RetentionPeriod("year", year_retain),
        ]
        self.retentions = {
            "day": day_retain,
            "week": week_retain,
            "month": month_retain,
            "year": year_retain,
        }

    def copy_and_prune(self):
        """
        Copy backup file to daily and appropriate weekly, monthly, and yearly directories, creating dirs if needed.
        Prune backups in each directory according to their retention periods.
        """
        logger.debug("Pruning backups", category="BACKUP")
        self._create_backup_dirs()
        self.make_backups()
        self.prune_backups()

    def _create_backup_dirs(self):
        """
        Create directory structure for daily, weekly, monthly, and yearly.
        """
        for period in self.retention_tuples:
            backup_dir = self.output_dir / period.name
            if not backup_dir.exists():
                backup_dir.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created backup directory: {backup_dir}", category="BACKUP")

    def make_backups(self):
        """
        Copy ``self.backup_target`` to daily and if applicable weekly, monthly, and yearly directories.
        """
        input_file = Path(self.backup_target)
        root_dir = self.output_dir

        dated_filename = f"{input_file.stem}-{self.backup_date}{input_file.suffix}"
        daily_file = input_file.with_name(dated_filename)

        for period in self.retention_tuples:
            period_dir = root_dir / period.name
            if self.always_copy or self.should_copy(period):
                shutil.copy(daily_file, period_dir)
                logger.info(f"{period}ly backup copied to {period_dir}", category="BACKUP")

    def should_copy(self, period: RetentionPeriod) -> bool:
        """
        :param period: The period to check (day, week, month, or year).
        :return: True if the backup should be copied.
        """
        backup_date = datetime.strptime(self.backup_date, "%Y-%m-%d")
        if period.name not in ["day", "week", "month", "year"]:
            raise NotImplementedError(
                f"Period must be day, week, month, or year, not {period.name}")

        if period.name == "day":
            return True
        elif period.name == "week" and backup_date.weekday() == 0:
            return True
        elif period.name == "month" and backup_date.day == 1:
            return True
        elif period.name == "year" and backup_date.strftime("%j") == "001":
            return True
        return False

    def prune_backups(self):
        """
        Prunes backups in each directory according to their retention periods.
        """
        for period in self.retention_tuples:
            backup_dir = self.output_dir / period.name
            all_files = sorted(backup_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)

            for file in all_files[period.retain:]:
                file.unlink()
                logger.info(f"Removed old backup: {file}", category="BACKUP")


class RetentionPeriod(NamedTuple):
    name: Literal["day", "week", "month", "year"]
    retain: int
