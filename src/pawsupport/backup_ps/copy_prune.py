import shutil
from datetime import datetime
from pathlib import Path

from loguru import logger


class Pruner(object):
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
        self.intervals = {
            "day": day_retain,
            "week": week_retain,
            "month": month_retain,
            "year": year_retain,
        }

    def copy_and_prune(self):
        logger.debug("Pruning backups", category="BACKUP")
        self._create_backup_dirs()
        self._make_backup()
        self._prune_backups()

        logger.debug("Pruning complete", category="BACKUP")

    def _create_backup_dirs(self):
        for period in self.intervals:
            backup_dir = self.output_dir / period
            if not backup_dir.exists():
                backup_dir.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created backup directory: {backup_dir}", category="BACKUP")

    def _make_backup(self):
        input_file = Path(self.backup_target)
        root_dir = self.output_dir

        dated_filename = f"{input_file.stem}-{self.backup_date}{input_file.suffix}"
        daily_file = root_dir / "day" / dated_filename
        shutil.copy(input_file, daily_file)
        logger.info(f"Backup created at {daily_file}", category="BACKUP")

        for period in self.intervals:
            period_dir = root_dir / period
            if self.always_copy or self._should_copy_to_period(period):
                shutil.copy(daily_file, period_dir)
                logger.info(f"{period}ly backup copied to {period_dir}", category="BACKUP")

    def _should_copy_to_period(self, period):
        backup_date = (
            datetime.strptime(self.backup_date, "%Y-%m-%d") if self.backup_date else datetime.now()
        )
        if period == "week" and backup_date.weekday() == 0:
            return True
        if period == "month" and backup_date.day == 1:
            return True
        if period == "year" and backup_date.strftime("%j") == "001":
            return True
        return False

    def _prune_backups(self):
        for period, retention in self.intervals.items():
            backup_dir = self.output_dir / period
            all_files = sorted(backup_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)

            for file in all_files[retention:]:
                file.unlink()
                logger.info(f"Removed old backup: {file}", category="BACKUP")
