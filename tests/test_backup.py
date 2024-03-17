import os
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

from suppawt.backup_ps import Pruner


def test_backup_pruning():
    # Create a temporary directory and a test file
    with tempfile.TemporaryDirectory() as tmp_dir_str:
        tmp_dir = Path(tmp_dir_str)
        test_file = tmp_dir / "testfile.txt"
        with open(test_file, "w") as f:
            f.write("Test content")

        # Simulate 9 weeks of backups
        for week in range(9):
            for day in range(7):
                backup_date = (datetime.now() + timedelta(weeks=week, days=day)).strftime("%Y-%m-%d")
                Pruner(
                    output_dir=tmp_dir,
                    backup_target=test_file,
                    _backup_date=backup_date,
                ).copy_and_prune()

        # Check the number of backups in each directory
        for period, expected_count in [("day", 7), ("week", 4), ("month", 12), ("year", 5)]:
            backup_dir = os.path.join(tmp_dir, period)
            actual_count = len(os.listdir(backup_dir))
            assert (
                actual_count <= expected_count
            ), f"Too many backups in {period} directory: {actual_count} (expected: {expected_count})"

