from collections.abc import Generator, Iterable
import os
from pathlib import Path
import sys
from convert3d.utils.blender import convert as _convert


def _get_fmt(file: Path) -> str:
    return file.suffix.removeprefix(".").lower()


def _get_out_file(in_file: Path, output_pattern: str | None, fmt: str | None):
    in_file_stem = in_file.stem
    if not output_pattern or output_pattern[-1] in ("/", "\\"):
        output_pattern = str(in_file.parent / "*.*")

    out_ext = Path(output_pattern).suffix
    if out_ext == ".*":
        if fmt is None:
            raise ValueError("Output format must be specified.")
        out_ext = "." + fmt

    if fmt is None:
        fmt = out_ext.removeprefix(".")

    out_path = Path(output_pattern.replace("*", in_file_stem)).with_suffix(out_ext)

    if fmt is None:
        fmt = out_ext.lower()
    fmt = fmt.lower()
    if out_ext == "*":
        out_ext = fmt
    return out_path


def convert(in_file: Path, out_file: Path | None, fmt: str | None = None):
    if out_file is None:
        if fmt is None:
            raise ValueError("Output format must be specified")
        out_file = Path(".") / in_file.with_suffix("." + fmt).name
    in_fmt = _get_fmt(in_file)
    if fmt is None:
        fmt = _get_fmt(out_file)
    fmt = fmt.lower()
    if not in_file.exists() or not in_file.is_file():
        raise FileNotFoundError(f"'{in_file}'")

    return _convert(str(in_file), in_fmt, str(out_file), fmt)


def multi_convert(
    files: Iterable[Path], out_dir_or_pattern: Path | None, fmt: str | None = None
):
    if out_dir_or_pattern is None:
        out_dir_or_pattern = Path(".")
    if "*" in out_dir_or_pattern.name:
        out_ext = out_dir_or_pattern.suffix.removeprefix(".")
        if out_dir_or_pattern.stem != "*":
            raise ValueError(
                "Output path must be a folder or a pattern of the form *.ext"
            )
        out_dir = out_dir_or_pattern.parent
    else:
        out_ext = "*"
        out_dir = out_dir_or_pattern

    if fmt is None and out_ext == "*":
        raise ValueError("Output format must be specified.")

    if fmt is None:
        fmt = out_ext.lower()
    fmt = fmt.lower()
    if out_ext == "*":
        out_ext = fmt

    out_dir.mkdir(exist_ok=True)

    for file in files:
        out_file = out_dir / file.with_suffix("." + out_ext)
        _convert(str(file), _get_fmt(file), str(out_file), fmt)


def resolve_patterns(patterns: Iterable[str]) -> Iterable[Path]:
    for pattern in patterns:
        for file in Path(".").glob(pattern):
            yield file


def wildcard_convert(
    file_patterns: Iterable[str],
    out_dir_or_pattern: Path | None,
    fmt: str | None = None,
):
    return multi_convert(
        resolve_patterns(file_patterns),
        out_dir_or_pattern,
        fmt,
    )
