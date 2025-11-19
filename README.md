# convert-audio-tool

A simple and convenient CLI tool for **batch-converting audio files** using `ffmpeg`.

It provides an easy interface for converting whole folders of audio, optionally handling recursion,
archiving originals, overwriting, quiet mode, and saving your default folder configuration for quick reuse.

This tool does *not* replace FFmpeg — it makes frequent batch workflows much easier.

## Features

- Convert audio files to a chosen format (WAV, MP3, FLAC…)
- Optional **recursive** folder traversal
- Optional **archiving** of original files
- Optional **overwrite** behavior
- Works as a standalone script or as an installed CLI command
- Cross-platform (Windows, macOS, Linux)
- Supports saving **default input/output/archive** folders

## Requirements

- Python **3.8+**
- `ffmpeg` installed and available in your system `PATH`

Verify FFmpeg installation:

```
ffmpeg -version
```

If not installed, download from:  
https://ffmpeg.org/

## Installation

### Option 1 — Run directly

```
git clone https://github.com/Nemecxpetr/convert_audio_tool.git
cd convert_audio_tool
```

(Optional, recommended)

```
python -m venv .venv
.venv\Scripts\activate      # Windows
# or: source .venv/bin/activate  # Linux/macOS
```

Run:

```
python convert_audio_tool.py -i samples/input -o samples/output
```

### Option 2 — Install as CLI (`convert-audio`)

From the project directory:

```
pip install .
```

Or development mode:

```
pip install -e .
```

This gives you the command:

```
convert-audio
```

## Usage

### Basic conversion (WAV output)

```
convert-audio -i samples/input -o samples/output
```

### Convert to MP3

```
convert-audio -i samples/input -o samples/output -f mp3
```

### Archive originals

```
convert-audio -i samples/input -o samples/output --archive samples/archived
```

### Disable archiving

```
convert-audio -i samples/input -o samples/output --no-archive
```

### Recursive folder search

```
convert-audio -i samples/input -o samples/output -r
```

### Overwrite existing files

```
convert-audio -i samples/input -o samples/output --overwrite
```

### Quiet mode

```
convert-audio -i samples/input -o samples/output -q
```

## Saving default folders

Set your preferred defaults once:

```
convert-audio -i samples/input -o samples/output --archive samples/archived --save-defaults
```

Next time:

```
convert-audio
```

Show stored defaults:

```
convert-audio --show-defaults
```

Defaults are stored in:

```
~/.convert_audio_tool.json
```

## Supported audio formats

The tool processes these extensions automatically:

```
.wav .flac .aac .ogg .mp3 .mp4 .m4a
```

## Command-line overview

```
convert-audio [-i INPUT] [-o OUTPUT] [-f FORMAT]
              [--archive FOLDER | --no-archive]
              [-r] [--overwrite] [-q]
              [--save-defaults] [--show-defaults]
```

| Option | Description |
|--------|-------------|
| `-i`, `--input-folder` | Folder containing audio files |
| `-o`, `--output-folder` | Folder for converted files |
| `-f`, `--format` | Output format (`wav`, `mp3`, …) |
| `--archive FOLDER` | Move original files here |
| `--no-archive` | Disable archiving |
| `-r`, `--recursive` | Search subfolders |
| `--overwrite` | Replace existing output files |
| `-q`, `--quiet` | Minimal console output |
| `--save-defaults` | Store current folders as defaults |
| `--show-defaults` | Display saved defaults |

## Examples

Convert recursively and archive originals:

```
convert-audio -i samples/input -o samples/output -r --archive samples/archived
```

Convert to MP3, overwrite, quiet mode:

```
convert-audio -i samples/input -o out_mp3 -f mp3 --overwrite -q
```

## FFmpeg license notice

This tool uses **FFmpeg** for audio conversion.

FFmpeg is **not included** and must be installed separately.  
It is licensed under **GNU LGPL 2.1** or **GNU GPL 2.0**, depending on the build.

More info:  
https://ffmpeg.org/legal.html

`convert-audio-tool` is not affiliated with the FFmpeg project.

## License

This project uses a separate LICENSE file included in the repository.
