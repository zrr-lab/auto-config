from __future__ import annotations

from pathlib import Path
from sys import stdout
from typing import Optional

import typer
from loguru import logger

from auto_config import utils

app = typer.Typer()


@app.callback()
def main(
    log_level="INFO",
):
    logger.remove()
    logger.add(stdout, level=log_level)

@app.command()
def generate_config(
    path: str = typer.Argument("~/.config/auto-config/config.toml"),
    *,
    groups: Optional[list[str]] = None,
    gateway_group: Optional[str] = None,
):
    utils.generate_config(Path(path), groups=groups, gateway_group=gateway_group)


if __name__ == "__main__":
    app()
