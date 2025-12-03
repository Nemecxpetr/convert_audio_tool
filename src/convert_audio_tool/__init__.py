"""
convert-audio-tool

Public Python API for batch-converting media files using ffmpeg.

Most users will use the CLI entry point ``convert-audio``, but the core
functions are also importable from Python:

    from convert_audio_tool import convert_folder
"""

from .core import (
    MEDIA_EXTENSIONS,
    CONFIG_FILE,
    convert_folder,
    convert_media,
    iter_media_files,
    load_config,
    save_config,
)

__all__ = [
    "MEDIA_EXTENSIONS",
    "CONFIG_FILE",
    "convert_folder",
    "convert_media",
    "iter_media_files",
    "load_config",
    "save_config",
]
