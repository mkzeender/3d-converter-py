from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, cast
from convert3d.convert import convert, multi_convert
from convert3d.utils import logger, blender
import sys
import logging
from argparse import ArgumentParser

# import bpy

# --------------------------------------------------------------------
# Enable Plugins
# --------------------------------------------------------------------


def optional_path(x: str | None) -> Path | None:
    return None if x is None else Path(x)


class ArgNs:
    FILES: list[str]
    output: str | None
    format: str | None


def main(argv: Sequence[str] | None = None):
    logger.configure_logger(True)

    parser = ArgumentParser()

    parser.add_argument(
        "--output",
        "-o",
        help='Output location. For single files, this will be the file name. Otherwise, it is a folder. It can also be of the form "*.ext"',
    )
    parser.add_argument("--format", "-f", help="Output format.")
    parser.add_argument(
        "FILES", nargs="+", help="File(s) to be converted. Can include wildcards"
    )
    ns: ArgNs = cast(ArgNs, parser.parse_args(argv))

    if len(ns.FILES) > 1 or "*" in ns.FILES[0]:
        multi_convert(
            (Path(fp) for fp in ns.FILES), optional_path(ns.output), ns.format
        )

    else:
        convert(Path(ns.FILES[0]), optional_path(ns.output), ns.format)

    # --------------------------------------------------------------------
    # Initing
    # --------------------------------------------------------------------

    # PROGRAM_NAME, INPUT_PATH, OUTPUT_PATH = sys.argv
    # INPUT_FORMAT = INPUT_PATH.split(".")[-1]
    # OUTPUT_FORMAT = OUTPUT_PATH.split(".")[-1]
    # logging.info(f'Program "{PROGRAM_NAME}" started')

    # # --------------------------------------------------------------------
    # # Main
    # # --------------------------------------------------------------------

    # blender.convert(INPUT_PATH, INPUT_FORMAT, OUTPUT_PATH, OUTPUT_FORMAT)

    # # --------------------------------------------------------------------
    # # Exiting
    # # --------------------------------------------------------------------

    # logging.info("Program stopped")
