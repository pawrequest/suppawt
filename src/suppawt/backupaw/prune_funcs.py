# import shutil
# from datetime import datetime
# from pathlib import Path
#
# from loguru import logger
#
#
# def prune(day_retain=7, week_retain=4, month_retain=12, year_retain=5, debug_mode=0, backup_date=None):
#     if not OUTPUT_DIR.exists():
#         raise FileNotFoundError(f"File {OUTPUT_DIR} does not exist")
#     logger.debug("Pruning backups")
#
#     intervals = {"day": day_retain, "week": week_retain, "month": month_retain, "year": year_retain}
#     create_backup_dirs(intervals)
#     make_backup(intervals, debug_mode, backup_date)
#     prune_backups(intervals)
#
#     logger.debug("Pruning complete")
#
#
# def create_backup_dirs(intervals):
#     for period in intervals:
#         backup_dir = OUTPUT_DIR / period
#         if not backup_dir.exists():
#             backup_dir.mkdir(parents=True, exist_ok=True)
#             logger.info(f"Created backup directory: {backup_dir}")
#
#
# def make_backup(intervals, debug_mode, backup_date=None):
#     input_file = Path(BACKUP_TARGET)
#     root_dir = OUTPUT_DIR
#
#     today = backup_date if backup_date else datetime.now().strftime("%Y-%m-%d")
#     dated_filename = f"{input_file.stem}-{today}{input_file.suffix}"
#     daily_file = root_dir / "day" / dated_filename
#
#     shutil.copy(input_file, daily_file)
#     logger.info(f"Backup created at {daily_file}")
#
#     for period in intervals:
#         period_dir = root_dir / period
#         if debug_mode or should_copy_to_period(period, backup_date):
#             shutil.copy(daily_file, period_dir)
#             logger.info(f"{period}ly backup copied to {period_dir}")
#
#
# def should_copy_to_period(period, backup_date=None):
#     backup_date = datetime.strptime(backup_date, "%Y-%m-%d") if backup_date else datetime.now()
#     if period == "week" and backup_date.weekday() == 0:
#         return True
#     if period == "month" and backup_date.day == 1:
#         return True
#     if period == "year" and backup_date.strftime("%j") == "001":
#         return True
#     return False
#
#
# def prune_backups(intervals):
#     for period, retention in intervals.items():
#         backup_dir = OUTPUT_DIR / period
#         all_files = sorted(backup_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)
#
#         for file in all_files[retention:]:
#             file.unlink()
#             logger.info(f"Removed old backup: {file}")
