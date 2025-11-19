#!/usr/bin/env python
"""
Batch-convert audio files in a folder using ffmpeg and optionally archive originals.

Requires:
    - ffmpeg installed and available in PATH

Examples:
    python convert_audio_tool.py -i input_folder -o output_folder/odpovedi -f wav
    python convert_audio_tool.py -i input_folder -o output_folder -f mp3 --archive archived

After installing as a console script (see pyproject.toml), you can do:

    convert-audio -i my_input -o my_output --archive my_archive --save-defaults

Next time, you can just run:

    convert-audio

and it will use the saved defaults.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys

AUDIO_EXTENSIONS = (".wav", ".flac", ".aac", ".ogg", ".mp3", ".mp4", ".m4a")

# Path to a simple JSON config with default folders
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".convert_audio_tool.json")


def load_config():
    """Load default folders from the config file, if it exists."""
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            # Ensure it's a dict
            if not isinstance(cfg, dict):
                return {}
            return cfg
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        # Corrupted config – ignore
        return {}


def save_config(input_folder, output_folder, archive_folder):
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
    

def check_ffmpeg():
    if shutil.which("ffmpeg") is None:
        raise EnvironmentError("ffmpeg is not installed or not found in PATH.")


def convert_audio(input_file, output_file, overwrite=False, quiet=False):
    check_ffmpeg()

    # Skip if output exists and we don't want to overwrite
    if os.path.exists(output_file) and not overwrite:
        if not quiet:
            print(f"Skipping (exists): {output_file}")
        return

    # Build command
    command = ["ffmpeg", "-y" if overwrite else "-n", "-i", input_file, output_file]

    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        if not quiet:
            print(f"OK  {input_file} -> {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {input_file} -> {output_file} ({e})")


def convert_folder(input_folder, output_folder, output_ext=".wav", recursive=False,
                   overwrite=False, quiet=False, archive_folder=None):
    if not os.path.isdir(input_folder):
        print(f"Input folder does not exist: {input_folder}")
        sys.exit(1)

    os.makedirs(output_folder, exist_ok=True)

    # Walk files
    if recursive:
        walker = (
            os.path.join(root, filename)
            for root, _, files in os.walk(input_folder)
            for filename in files
        )
    else:
        walker = (
            os.path.join(input_folder, filename)
            for filename in os.listdir(input_folder)
        )

    converted_files = []

    for path in walker:
        if not os.path.isfile(path):
            continue

        if not path.lower().endswith(AUDIO_EXTENSIONS):
            continue

        rel_name = os.path.splitext(os.path.basename(path))[0]
        out_path = os.path.join(output_folder, rel_name + output_ext)

        convert_audio(path, out_path, overwrite=overwrite, quiet=quiet)
        converted_files.append(path)

    # Archive originals
    if archive_folder is not None:
        os.makedirs(archive_folder, exist_ok=True)
        for src in converted_files:
            dest = os.path.join(archive_folder, os.path.basename(src))
            shutil.move(src, dest)
        if not quiet:
            print(f"Moved {len(converted_files)} file(s) to archive: {archive_folder}")


def parse_args(config=None):
    """Parse CLI args, using config dict (if provided) as defaults."""
    if config is None:
        config = {}

    default_input = config.get("input_folder", "input_folder")
    default_output = config.get("output_folder", "output_folder/odpovedi")
    default_archive = config.get("archive", "archived")

    parser = argparse.ArgumentParser(
        description="Convert audio files in a folder using ffmpeg."
    )
    parser.add_argument(
        "-i", "--input-folder",
        default=default_input,
        help=f"Input folder with audio files (default: {default_input})",
    )
    parser.add_argument(
        "-o", "--output-folder",
        default=default_output,
        help=f"Output folder for converted files (default: {default_output})",
    )
    parser.add_argument(
        "-f", "--format",
        default="wav",
        help="Output format/extension without dot, e.g. wav, mp3 (default: wav)",
    )
    parser.add_argument(
        "--archive",
        default=default_archive,
        help=f"Folder to move originals to after conversion (default: {default_archive}). "
             "Use --no-archive to disable.",
    )
    parser.add_argument(
        "--no-archive",
        action="store_true",
        help="Do not move original files to archive.",
    )
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Search for audio files recursively in subfolders.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing output files.",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Less verbose output.",
    )
    parser.add_argument(
        "--save-defaults",
        action="store_true",
        help="Save the current -i/--input-folder, -o/--output-folder and --archive "
             "values as new defaults for future runs.",
    )
    parser.add_argument(
        "--show-defaults",
        action="store_true",
        help="Show the currently configured default folders and exit.",
    )

    return parser.parse_args()


def main():
    config = load_config()
    args = parse_args(config)

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
