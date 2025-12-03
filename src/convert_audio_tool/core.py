from __future__ import annotations

"""
Core functionality for convert-audio-tool.

This module provides reusable functions for batch-converting media files
(audio and simple video containers) using ffmpeg, with a per-file progress bar.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from tqdm import tqdm  # type: ignore[import-untyped]

# Extensions we process (audio + some common video containers)
MEDIA_EXTENSIONS: Tuple[str, ...] = (
    ".wav",
    ".flac",
    ".aac",
    ".ogg",
    ".mp3",
    ".mp4",
    ".m4a",
    ".mxf",
    ".mov",
    ".avi",
)

# Path to a simple JSON config with default folders
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".convert_audio_tool.json")


# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

def load_config() -> Dict[str, Optional[str]]:
    """Load default folders from the config file, if it exists."""
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        if not isinstance(cfg, dict):
            return {}
        # Normalise to str/None
        out: Dict[str, Optional[str]] = {}
        for key in ("input_folder", "output_folder", "archive"):
            val = cfg.get(key)
            if isinstance(val, str) or val is None:
                out[key] = val
        return out
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        # Corrupted config – ignore
        return {}


def save_config(input_folder: str, output_folder: str, archive_folder: Optional[str]) -> None:
    """Save default folders to the config file."""
    cfg = {
        "input_folder": input_folder,
        "output_folder": output_folder,
        "archive": archive_folder,
    }
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    print(f"Saved defaults to {CONFIG_FILE}")


# ---------------------------------------------------------------------------
# FFmpeg helpers
# ---------------------------------------------------------------------------

def check_ffmpeg() -> None:
    """Raise if ffmpeg or ffprobe are not available in PATH."""
    if shutil.which("ffmpeg") is None:
        raise EnvironmentError("ffmpeg is not installed or not found in PATH.")
    if shutil.which("ffprobe") is None:
        raise EnvironmentError("ffprobe is not installed or not found in PATH.")


def get_media_duration(path: str) -> Optional[float]:
    """
    Returns duration in seconds using ffprobe, or None if unavailable.
    """
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                path,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return float(result.stdout.strip())
    except Exception:
        return None


def _parse_out_time(line: str) -> Optional[float]:
    """
    Parse a line like 'out_time=00:01:23.456789' to seconds.

    Returns:
        Seconds as float, or None if parsing fails.
    """
    try:
        _, value = line.split("=", 1)
    except ValueError:
        return None

    value = value.strip()
    if not value:
        return None

    # value is HH:MM:SS.micro
    try:
        h_str, m_str, s_str = value.split(":")
        h = int(h_str)
        m = int(m_str)
        s = float(s_str)
        return s + 60 * (m + 60 * h)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Conversion
# ---------------------------------------------------------------------------

def convert_media(
    input_file: str | Path,
    output_file: str | Path,
    *,
    overwrite: bool = False,
    quiet: bool = False,
) -> None:
    """
    Convert a single media file with ffmpeg and show a progress bar.

    Falls back to no progress bar if duration can't be detected.
    """
    check_ffmpeg()

    input_file = str(input_file)
    output_file = str(output_file)

    # Skip if output exists and we don't want to overwrite
    if os.path.exists(output_file) and not overwrite:
        if not quiet:
            print(f"Skipping (exists): {output_file}")
        return

    duration = get_media_duration(input_file)

    # IMPORTANT:
    # -progress pipe:1 has to be BEFORE the output URL so it is treated
    # as a global option, and we can read progress lines from stdout.
    command: List[str] = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",  # keep stderr quiet, progress goes to stdout
        "-progress",
        "pipe:1",
        "-nostats",
        "-y" if overwrite else "-n",
        "-i",
        input_file,
        output_file,
    ]

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            universal_newlines=True,
            bufsize=1,
        )

        # If we don't know duration → no progress bar, just drain stdout.
        if not duration or not process.stdout:
            for _ in process.stdout or []:
                pass
            ret = process.wait()
            if ret == 0 and not quiet:
                print(f"OK  {input_file} -> {output_file}")
            elif ret != 0:
                print(f"Error during conversion: {input_file} -> {output_file}")
            return

        last_t = 0.0
        filename = os.path.basename(input_file)

        with tqdm(
            total=duration,
            unit="s",
            desc=filename,
            leave=True,
        ) as pbar:
            for raw_line in process.stdout:
                line = raw_line.strip()
                if not line:
                    continue

                # Prefer out_time_ms if present
                t: Optional[float] = None
                if line.startswith("out_time_ms="):
                    try:
                        ms = int(line.split("=", 1)[1])
                        t = ms / 1_000_000.0  # μs → s
                    except Exception:
                        t = None
                elif line.startswith("out_time="):
                    t = _parse_out_time(line)

                if t is not None:
                    t = min(t, duration)
                    if t > last_t:
                        pbar.update(t - last_t)
                        last_t = t

                if line.startswith("progress=") and "end" in line:
                    break

            process.wait()
            if last_t < duration:
                pbar.update(duration - last_t)

        if process.returncode == 0 and not quiet:
            print(f"OK  {input_file} -> {output_file}")
        elif process.returncode != 0:
            print(f"Error during conversion: {input_file} -> {output_file}")
    except Exception as e:  # pragma: no cover - defensive logging
        print(f"Error converting {input_file}: {e}")


def iter_media_files(input_folder: str | Path, recursive: bool = False) -> Iterable[str]:
    """
    Yield absolute paths to media files under input_folder.

    Args:
        input_folder: Root folder to scan.
        recursive: Whether to walk subdirectories.
    """
    input_folder = str(input_folder)

    if recursive:
        for root, _, files in os.walk(input_folder):
            for filename in files:
                full = os.path.join(root, filename)
                if os.path.isfile(full) and full.lower().endswith(MEDIA_EXTENSIONS):
                    yield full
    else:
        for filename in os.listdir(input_folder):
            full = os.path.join(input_folder, filename)
            if os.path.isfile(full) and full.lower().endswith(MEDIA_EXTENSIONS):
                yield full


def convert_folder(
    input_folder: str | Path,
    output_folder: str | Path,
    *,
    output_ext: str = ".wav",
    recursive: bool = False,
    overwrite: bool = False,
    quiet: bool = False,
    archive_folder: str | Path | None = None,
) -> None:
    """
    Convert all media files in a folder.

    Args:
        input_folder: Folder containing input media files.
        output_folder: Folder where converted files will be written.
        output_ext: Output extension including dot, e.g. ".wav", ".mp3", ".mp4".
        recursive: Whether to scan subfolders.
        overwrite: Whether to overwrite existing outputs.
        quiet: Whether to reduce console output.
        archive_folder: If given, move originals there after successful conversion.
    """
    input_folder = str(input_folder)
    output_folder = str(output_folder)

    if not os.path.isdir(input_folder):
        print(f"Input folder does not exist: {input_folder}")
        sys.exit(1)

    os.makedirs(output_folder, exist_ok=True)

    converted_files: List[str] = []

    for src_path in iter_media_files(input_folder, recursive=recursive):
        rel_name = os.path.splitext(os.path.basename(src_path))[0]
        out_path = os.path.join(output_folder, rel_name + output_ext)
        convert_media(src_path, out_path, overwrite=overwrite, quiet=quiet)
        converted_files.append(src_path)

    # Archive originals
    if archive_folder is not None:
        archive_folder = str(archive_folder)
        os.makedirs(archive_folder, exist_ok=True)
        for src in converted_files:
            dest = os.path.join(archive_folder, os.path.basename(src))
            shutil.move(src, dest)
        if not quiet:
            print(f"Moved {len(converted_files)} file(s) to archive: {archive_folder}")
