import os
import sys

import toml
import xxhash
from pydantic import BaseModel

from loguru import logger
from contextlib import chdir

# Configure loguru to output colored logs to stdout
logger.remove()  # Remove default handler
logger.add(
    sys.stdout,
    colorize=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<blue>{file}:{line}</blue> - "
        "<level>{message}</level>"
    ),
)


class Config(BaseModel):
    start_date: int
    end_date: int
    working_dir_base: str
    output_dir: str


def setup_working_dir(config: Config):
    config_hash = xxhash.xxh3_64_hexdigest(config.model_dump_json())
    working_dir = os.path.join(config.working_dir_base, config_hash)
    os.makedirs(working_dir, exist_ok=True)
    logger.info(f"Working directory: {os.path.abspath(working_dir)}")
    return working_dir


def run_cmd(config: Config, working_dir: str):
    with chdir(working_dir):
        os.system("echo $(date) > date.txt")
        logger.info("date.txt created")


def cp_output_dir(config: Config, working_dir: str):
    os.makedirs(config.output_dir, exist_ok=True)
    logger.info(f"Copying output directory from {working_dir} to {config.output_dir}")
    os.system(f"cp -r {working_dir}/* {config.output_dir}")
    logger.info(f"Output directory: {os.path.abspath(config.output_dir)}")


def main(config: Config):
    working_dir = setup_working_dir(config)

    run_cmd(config, working_dir)

    cp_output_dir(config, working_dir)


if __name__ == "__main__":
    config = Config(**toml.load(sys.argv[1]))
    main(config)
