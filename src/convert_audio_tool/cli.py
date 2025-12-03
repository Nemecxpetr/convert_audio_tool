# src/convert_audio_tool/cli.py

from __future__ import annotations

import argparse

from .core import (
    CONFIG_FILE,
    convert_folder,
    load_config,
    save_config,
)


def parse_args(argv: list[str] | None = None):
    """Parse CLI args, using config dict (if provided) as defaults.

    If argv is None, argparse will use sys.argv[1:].
    In tests, we pass an explicit list to avoid picking up pytest args.
    """
    config = load_config() or {}

    default_input = config.get("input_folder") or "input_folder"
    default_output = config.get("output_folder") or "output_folder/odpovedi"
    default_archive = config.get("archive") or "archived"

    parser = argparse.ArgumentParser(
        description=(
            "Convert media files in a folder using ffmpeg "
            "(audio + simple video containers like MXF -> MP4) "
            "with a per-file progress bar."
        )
    )
    parser.add_argument(
        "-i",
        "--input-folder",
        default=default_input,
        help=f"Input folder with media files (default: {default_input})",
    )
    parser.add_argument(
        "-o",
        "--output-folder",
        default=default_output,
        help=f"Output folder for converted files (default: {default_output})",
    )
    parser.add_argument(
        "-f",
        "--format",
        default="wav",
        help="Output format/extension without dot, e.g. wav, mp3, mp4 (default: wav)",
    )
    parser.add_argument(
        "--archive",
        default=default_archive,
        help=(
            f"Folder to move originals to after conversion (default: {default_archive}). "
            "Use --no-archive to disable."
        ),
    )
    parser.add_argument(
        "--no-archive",
        action="store_true",
        help="Do not move original files to archive.",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Search for media files recursively in subfolders.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing output files.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Less verbose output.",
    )
    parser.add_argument(
        "--save-defaults",
        action="store_true",
        help=(
            "Save the current -i/--input-folder, -o/--output-folder and --archive "
            "values as new defaults for future runs."
        ),
    )
    parser.add_argument(
        "--show-defaults",
        action="store_true",
        help="Show the currently configured default folders and exit.",
    )

    # pass argv through; if None, argparse uses sys.argv[1:]
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    # Just show defaults and exit, if requested
    if args.show_defaults:
        print("Current defaults (including config + built-in):")
        print(f"  input-folder:  {args.input_folder}")
        print(f"  output-folder: {args.output_folder}")
        archive_info = "disabled (no archive)" if args.no_archive else args.archive
        print(f"  archive:       {archive_info}")
        print(f"Config file: {CONFIG_FILE}")
        return

    # Optionally save current settings as new defaults
    if args.save_defaults:
        archive_for_config = None if args.no_archive else args.archive
        save_config(args.input_folder, args.output_folder, archive_for_config)

    output_ext = "." + args.format.lstrip(".")
    archive_folder = None if args.no_archive else args.archive

    convert_folder(
        input_folder=args.input_folder,
        output_folder=args.output_folder,
        output_ext=output_ext,
        recursive=args.recursive,
        overwrite=args.overwrite,
        quiet=args.quiet,
        archive_folder=archive_folder,
    )


if __name__ == "__main__":
    main()
