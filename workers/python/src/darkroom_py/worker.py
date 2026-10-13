import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pillow_heif
from temporalio.client import Client
from temporalio.envconfig import ClientConfig
from temporalio.worker import Worker

from darkroom_py.activities.filter_basic import BasicFilter

TASK_QUEUE = "darkroom-process"  # must equal names.TaskQueueProcess in Go

DEFAULT_CONFIG = Path(__file__).resolve().parents[2] / "config.toml"


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    pillow_heif.register_heif_opener()

    config_file = Path(os.environ.get("DARKROOM_CONFIG", DEFAULT_CONFIG))
    connect_config = ClientConfig.load_client_connect_config(
        config_file=str(config_file)
    )
    logging.info(
        "connecting to %s (namespace %s)",
        connect_config.get("target_host"),
        connect_config.get("namespace"),
    )
    client = await Client.connect(**connect_config)  # type: ignore[arg-type]

    filter_basic = BasicFilter()  # or Config.load("filter.toml")

    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        activities=[filter_basic.run],
        activity_executor=ThreadPoolExecutor(max_workers=4),
        max_concurrent_activities=4,
    )
    logging.info("worker polling %s", TASK_QUEUE)
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())