# convert-audio-tool

A simple and convenient CLI tool for **batch-converting audio files** using `ffmpeg`.

It provides a clean interface for converting whole folders of audio, optionally
handling recursion, archiving originals, skipping/overwriting outputs, and saving
your default folder configuration for fast future use.

`ffmpeg` is powerful — this tool removes the need to write shell loops,
handle quoting, recursive searches, or manually move archive files.

---

## Features

- Convert all audio files in a folder to a chosen format (WAV, MP3, FLAC…)
- Optional **recursive** folder traversal
- Optional **archiving** (move original files after conversion)
- Optional **overwrite** behavior
- Simple command-line interface
- Cross-platform (Windows, macOS, Linux)
- Requires only Python + ffmpeg
- Can be installed as a console command (`convert-audio`)
- Supports saving **default folders** for fast reuse

---

## Requirements

- Python **3.8+**
- `ffmpeg` installed and available on your system’s `PATH`  
  You should be able to run:

  ```bash
  ffmpeg -version

If this fails, install FFmpeg from:
https://ffmpeg.org/

## Installation
### Option 1: Run directly
bash
Copy code
git clone https://github.com/Nemecxpetr/convert_audio_tool.git
cd convert_audio_tool
(Optional, recommended)

bash
Copy code
python -m venv .venv
.venv\Scripts\activate   # Windows
# or: source .venv/bin/activate  # macOS/Linux
Run the tool:

bash
Copy code
python convert_audio_tool.py -i samples/input -o samples/output
Option 2: Install as a CLI command
Inside the project folder:

bash
Copy code
pip install .
(or for development mode)

bash
Copy code
pip install -e .
This gives you a global command inside your environment:

bash
Copy code
convert-audio
Usage
Basic conversion (WAV output):

bash
Copy code
convert-audio -i samples/input -o samples/output
Convert to MP3:

bash
Copy code
convert-audio -i samples/input -o samples/output -f mp3
Archive originals:

bash
Copy code
convert-audio -i samples/input -o samples/output --archive samples/archived
Disable archiving:

bash
Copy code
convert-audio -i samples/input -o samples/output --no-archive
Recursive search:

bash
Copy code
convert-audio -i samples/input -o samples/output -r
Overwrite existing files:

bash
Copy code
convert-audio -i samples/input -o samples/output --overwrite
Quiet mode:

bash
Copy code
convert-audio -i samples/input -o samples/output -q
Saving Default Folders
Set your preferred default folders once:

bash
Copy code
convert-audio -i samples/input -o samples/output --archive samples/archived --save-defaults
Then next time simply run:

bash
Copy code
convert-audio
Show stored defaults:

bash
Copy code
convert-audio --show-defaults
Defaults are stored in:

bash
Copy code
~/.convert_audio_tool.json
Supported Audio Extensions
The tool automatically processes:

Copy code
.wav, .flac, .aac, .ogg, .mp3, .mp4, .m4a
(case-insensitive)

Command-line Options Overview
css
Copy code
convert-audio [-i INPUT] [-o OUTPUT] [-f FORMAT]
              [--archive FOLDER | --no-archive]
              [-r] [--overwrite] [-q]
              [--save-defaults] [--show-defaults]
Option	Description
-i, --input-folder	Input folder containing audio files
-o, --output-folder	Folder where converted files will be saved
-f, --format	Output format (e.g. wav, mp3, flac)
--archive PATH	Move original files to this folder
--no-archive	Disable archiving
-r, --recursive	Search input folder recursively
--overwrite	Force overwrite of existing output files
-q, --quiet	Minimal output
--save-defaults	Store current folders as default
--show-defaults	Display saved defaults

Examples
Convert all audio under samples/input to WAV, include subfolders, archive originals:

bash
Copy code
convert-audio -i samples/input -o samples/output -r --archive samples/archived
Convert to MP3, overwrite existing files, quiet mode:

bash
Copy code
convert-audio -i samples/input -o mp3_out -f mp3 --overwrite -q
FFmpeg License Notice
This tool depends on FFmpeg for audio conversion.

FFmpeg is a separate project and is licensed under the
GNU LGPL 2.1 or GNU GPL 2.0, depending on build configuration.

FFmpeg is not included in this repository or distributed with this tool.
You must install FFmpeg separately from:

https://ffmpeg.org/

For FFmpeg licensing details, see:
https://ffmpeg.org/legal.html

The convert-audio-tool project is not affiliated with the FFmpeg project.

Why use this tool instead of raw ffmpeg?
While FFmpeg is extremely powerful, it only operates one file at a time.
This tool adds:

Batch folder processing

Recursive search

Archiving logic

Default folder storage

Cross-platform behavior

Simple CLI with no scripting required

Automatic file skipping / overwrite handling

Clean output and workflow-friendly interface

It is intended as a higher-level workflow manager on top of FFmpeg.

License

text
Copy code
MIT License
Copyright (c) 2025 Petr Němec

Permission is hereby granted...