"""
Create a backup directory structure for days weeks months and years
Copy the backup file to the daily directory
Copy the daily backup file to the weekly, monthly and yearly directories if the date is appropriate
Prune the backup directories to the specified retention periods
"""

import shutil
from datetime import datetime
from pathlib import Path
from typing import Literal, NamedTuple

from loguru import logger


class RetentionPeriod(NamedTuple):
    name: Literal["day", "week", "month", "year"]
    retain: int


class Pruner(object):
    """
    Copy and prune backups

    :param backup_target: The file to back up.
    :param output_dir: The directory where backups will be stored. Defaults to the parent directory of the backup target.
    :param day_retain: The number of daily backups to retain. Defaults to 7.
    :param week_retain: The number of weekly backups to retain. Defaults to 4.
    :param month_retain: The number of monthly backups to retain. Defaults to 12.
    :param year_retain: The number of yearly backups to retain. Defaults to 5.
    :param always_copy: If True, always copy the daily backup to other periods for debugging/testing. Defaults to False.
    :param backup_date: The date to use in the backup's name. Defaults to today's date for debugging/testing.
    """

    def __init__(
            self,
            backup_target: Path,
            output_dir: Path = None,
            day_retain=7,
            week_retain=4,
            month_retain=12,
            year_retain=5,
            always_copy=False,
            backup_date=None,
    ):
        self.backup_target = backup_target
        self.output_dir = output_dir or backup_target.parent
        self.always_copy = always_copy
        self.backup_date = backup_date if backup_date else datetime.now().strftime("%Y-%m-%d")
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
        Copies the backup file to the daily directory and prunes backups according to the specified retention periods.
        """
        logger.debug("Pruning backups", category="BACKUP")

        self._create_backup_dirs()
        self._make_backup()
        self._prune_backups()

        logger.debug("Pruning complete", category="BACKUP")

    def _create_backup_dirs(self):
        """
        Creates the backup directory structure for daily, weekly, monthly, and yearly backups.
        """
        for period in self.retention_tuples:
            backup_dir = self.output_dir / period.name
            if not backup_dir.exists():
                backup_dir.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created backup directory: {backup_dir}", category="BACKUP")

    def _make_backup(self):
        """
        Copies the backup file to the daily directory and, if applicable, to the weekly, monthly, and yearly directories.
        """
        input_file = Path(self.backup_target)
        root_dir = self.output_dir

        dated_filename = f"{input_file.stem}-{self.backup_date}{input_file.suffix}"
        daily_file = root_dir / "day" / dated_filename
        shutil.copy(input_file, daily_file)
        logger.info(f"Backup created at {daily_file}", category="BACKUP")

        for period in self.retention_tuples:
            period_dir = root_dir / period.name
            if self.always_copy or self._should_copy(period):
                shutil.copy(daily_file, period_dir)
                logger.info(f"{period}ly backup copied to {period_dir}", category="BACKUP")

    def _should_copy(self, period: RetentionPeriod):
        """
        Returns true if self.backup_date is first of the period.

        :param period: The period to check (day, week, month, or year).
        :return: True if the backup should be copied, False otherwise.
        """
        backup_date = datetime.strptime(self.backup_date, "%Y-%m-%d")

        if period.name == "week" and backup_date.weekday() == 0:
            return True
        if period.name == "month" and backup_date.day == 1:
            return True
        if period.name == "year" and backup_date.strftime("%j") == "001":
            return True
        return False

    def _prune_backups(self):
        """Prune the backup directories to the specified retention periods"""
        for period in self.retention_tuples:
            backup_dir = self.output_dir / period.name
            all_files = sorted(backup_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)

            for file in all_files[period.retain:]:
                file.unlink()
                logger.info(f"Removed old backup: {file}", category="BACKUP")

# """
# Create a backup directory structure for days weeks months and years
# Copy the backup file to the daily directory
# Copy the daily backup file to the weekly, monthly and yearly directories if the date is appropriate
# Prune the backup directories to the specified retention periods
# """
#
#
#
# import shutil
# from datetime import datetime
# from pathlib import Path
#
# from loguru import logger
#
#
# class Pruner(object):
#     """
#     Copy and prune backups
#
#     :param backup_target: The file to back up.
#     :param output_dir: The directory where backups will be stored. Defaults to the parent directory of the backup target.
#     :param day_retain: The number of daily backups to retain. Defaults to 7.
#     :param week_retain: The number of weekly backups to retain. Defaults to 4.
#     :param month_retain: The number of monthly backups to retain. Defaults to 12.
#     :param year_retain: The number of yearly backups to retain. Defaults to 5.
#     :param always_copy: If True, always copy the daily backup to other periods for debugging/testing. Defaults to False.
#     :param backup_date: The date to use in the backup's name. Defaults to today's date for debugging/testing.
#     """
#
#
#     def __init__(
#             self,
#             backup_target: Path,
#             output_dir: Path = None,
#             day_retain=7,
#             week_retain=4,
#             month_retain=12,
#             year_retain=5,
#             always_copy=False,
#             backup_date=None,
#     ):
#         self.backup_target = backup_target
#         self.output_dir = output_dir or backup_target.parent
#         self.always_copy = always_copy
#         self.backup_date = backup_date if backup_date else datetime.now().strftime("%Y-%m-%d")
#         self.retentions = {
#             "day": day_retain,
#             "week": week_retain,
#             "month": month_retain,
#             "year": year_retain,
#         }
#
#     def copy_and_prune(self):
#         """Copy and prune backups"""
#         logger.debug("Pruning backups", category="BACKUP")
#         self._create_backup_dirs()
#         self._make_backup()
#         self._prune_backups()
#
#         logger.debug("Pruning complete", category="BACKUP")
#
#     def _create_backup_dirs(self):
#         """Create backup directory structure for self.retentions.keys()"""
#         for period in self.retentions:
#             backup_dir = self.output_dir / period
#             if not backup_dir.exists():
#                 backup_dir.mkdir(parents=True, exist_ok=True)
#                 logger.info(f"Created backup directory: {backup_dir}", category="BACKUP")
#
#     def _make_backup(self):
#         """Copy the backup file to the daily directory
#         Copy the daily backup file to the weekly, monthly and yearly directories if the date is appropriate
#         """
#         input_file = Path(self.backup_target)
#         root_dir = self.output_dir
#
#         dated_filename = f"{input_file.stem}-{self.backup_date}{input_file.suffix}"
#         daily_file = root_dir / "day" / dated_filename
#         shutil.copy(input_file, daily_file)
#         logger.info(f"Backup created at {daily_file}", category="BACKUP")
#
#         for period in self.retentions:
#             period_dir = root_dir / period
#             if self.always_copy or self._should_copy_to_period(period):
#                 shutil.copy(daily_file, period_dir)
#                 logger.info(f"{period}ly backup copied to {period_dir}", category="BACKUP")
#
#     def _should_copy_to_period(self, period):
#         """Return True if self.backup_date or today is first day of period"""
#         backup_date = (
#             datetime.strptime(self.backup_date, "%Y-%m-%d") if self.backup_date else datetime.now()
#         )
#         if period == "week" and backup_date.weekday() == 0:
#             return True
#         if period == "month" and backup_date.day == 1:
#             return True
#         if period == "year" and backup_date.strftime("%j") == "001":
#             return True
#         return False
#
#     def _prune_backups(self):
#         """Prune the backup directories to the specified retention periods"""
#         for period, retention in self.retentions.items():
#             backup_dir = self.output_dir / period
#             all_files = sorted(backup_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)
#
#             for file in all_files[retention:]:
#                 file.unlink()
#                 logger.info(f"Removed old backup: {file}", category="BACKUP")
