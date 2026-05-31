#!/usr/bin/env python3
"""Clean up old SNAPSHOT build artifacts."""

import datetime
import glob
import logging
import os
import re
import shutil
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

PATH_TO_CLEAN = os.getenv("BUILD_CLEANUP_PATH", "/Users/rahil.shaikh/Documents/oms/")
DELETE_OLDER_THAN_DAYS = int(os.getenv("BUILD_CLEANUP_DAYS", "2"))
DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"


def process_app_folder(app: str, builds: list[str], delete_older_than_days: int) -> None:
    builds.sort(key=lambda x: os.path.getmtime(x))
    builds.pop()
    builds = [
        b for b in builds
        if (time.time() - os.path.getmtime(b)) // (24 * 3600) >= delete_older_than_days
    ]

    for build in builds:
        match = re.match(r"[0-9.]+.*", os.path.basename(build))
        logger.info("Found build match: %s", match)
        logger.info(
            "Deleting %s of %s (older than %d days)",
            os.path.basename(build),
            os.path.basename(app),
            delete_older_than_days,
        )
        if not DRY_RUN:
            shutil.rmtree(build)
            logger.info("Deleted %s", build)
        else:
            logger.info("DRY RUN: would delete %s", build)


def print_build_creation_time(builds: list[str]) -> None:
    for build in builds:
        created = datetime.datetime.fromtimestamp(os.path.getmtime(build)).strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )
        logger.info("Build: %s. Created on: %s", os.path.basename(build), created)


def main() -> None:
    logger.info(
        "Running at %s (DRY_RUN=%s)",
        datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S.%f"),
        DRY_RUN,
    )

    apps = sorted(
        (d for d in glob.glob(os.path.join(PATH_TO_CLEAN, "*")) if os.path.isdir(d)),
        key=lambda x: os.path.getmtime(x),
    )

    for app in apps:
        logger.info("===== Processing: %s =====", os.path.basename(app))
        all_builds = sorted(
            (d for d in glob.glob(os.path.join(app, "*")) if os.path.isdir(d)),
            key=lambda x: os.path.getmtime(x),
        )

        snapshot_builds = [b for b in all_builds if b.endswith("-SNAPSHOT")]
        if snapshot_builds:
            print_build_creation_time(snapshot_builds)
            process_app_folder(app, snapshot_builds, DELETE_OLDER_THAN_DAYS)
        else:
            logger.info("No SNAPSHOT builds found for %s", os.path.basename(app))


if __name__ == "__main__":
    main()
