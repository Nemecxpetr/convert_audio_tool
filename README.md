# convert-audio-tool

[📦 Download the latest release](https://github.com/Nemecxpetr/convert_audio_tool/releases/latest)

A simple and convenient CLI tool for **batch-converting audio and video files** using FFmpeg.

It wraps common batch-conversion workflows into a friendly command-line interface with:

- 🔄 Automatic audio/video transcoding  
- 🎞️ MXF → MP4 support  
- 📈 Per-file **progress bar** (based on real FFmpeg timestamp output)  
- 📁 Recursive directory scanning  
- 📦 Optional archiving of original files  
- 💾 Persistent default directory configuration  
- 🧰 Cross-platform support (Windows/macOS/Linux)

This tool does *not* replace FFmpeg — it simply makes repetitive folder conversions fast and convenient.

---

## ✨ Features

- Convert audio and simple video containers:
  - `.wav .flac .aac .ogg .mp3 .mp4 .m4a .mxf .mov .avi`
- Convert whole folders at once
- Optional:
  - Recursive search
  - Archiving of originals
  - Quiet mode
  - Overwriting existing files
  - Saving defaults
- Live **progress bar** using FFmpeg’s `-progress pipe:1`
- Easy installation as a CLI command: `convert-audio`

---

## ⚙ Requirements

- Python **3.8+**
- `ffmpeg` **and** `ffprobe` available in your system PATH  
- Python package `tqdm` (installed automatically via `pyproject.toml`)

Verify FFmpeg:

```sh
ffmpeg -version
ffprobe -version
```

If missing, download from:  
https://ffmpeg.org/

---

## 📦 Installation

### Option A — Run directly

```sh
git clone https://github.com/Nemecxpetr/convert_audio_tool.git
cd convert_audio_tool
```

(Optional – recommended):

```sh
python -m venv .venv
.venv\Scripts\activate      # Windows
# or: source .venv/bin/activate
```

Run:

```sh
python convert_audio_tool.py -i samples/input -o samples/output
```

---

### Option B — Install as a CLI command (`convert-audio`)

In the project root:

```sh
pip install -e .
```

This creates the command:

```
convert-audio
```

---

## 🚀 Usage

### Basic conversion (WAV output)

```sh
convert-audio -i samples/input -o samples/output
```

### Convert to MP3

```sh
convert-audio -i samples/input -o samples/output -f mp3
```

### Convert video: MXF → MP4

```sh
convert-audio -i samples/input/video -o samples/output/mp4_out -f mp4
```

### Recursive search

```sh
convert-audio -i samples/input -o samples/output -r
```

### Overwrite existing files

```sh
convert-audio -i samples/input -o samples/output --overwrite
```

### Quiet mode

```sh
convert-audio -i samples/input -o samples/output -q
```

### Archive originals

```sh
convert-audio -i samples/input -o samples/output --archive samples/archived
```

### Disable archiving

```sh
convert-audio -i samples/input -o samples/output --no-archive
```

---

## 💾 Saving default folders

Save your standard working folders once:

```sh
convert-audio -i in -o out --archive archived --save-defaults
```

Next time you can just type:

```sh
convert-audio
```

Show current defaults:

```sh
convert-audio --show-defaults
```

Defaults are stored in:

```
~/.convert_audio_tool.json
```

---

## 🎚 Supported formats

(from `MEDIA_EXTENSIONS`)

```
.wav .flac .aac .ogg .mp3 .mp4 .m4a .mxf .mov .avi
```

---

## 🧩 Command-line overview

```
convert-audio [-i INPUT] [-o OUTPUT] [-f FORMAT]
              [--archive FOLDER | --no-archive]
              [-r] [--overwrite] [-q]
              [--save-defaults] [--show-defaults]
```

| Option | Description |
|--------|-------------|
| `-i`, `--input-folder` | Folder containing media files |
| `-o`, `--output-folder` | Where converted files will be stored |
| `-f`, `--format` | Output format (`wav`, `mp3`, `mp4`, …) |
| `--archive` | Move original files into this folder |
| `--no-archive` | Disable archiving |
| `-r`, `--recursive` | Convert files in subfolders too |
| `--overwrite` | Replace existing output files |
| `-q`, `--quiet` | Less console output |
| `--save-defaults` | Save folders for future runs |
| `--show-defaults` | Show stored defaults and exit |

---

## 📊 Progress bar

The tool automatically shows a live progress bar **per file** if FFmpeg reports duration:

```
myvideo.mxf:  42%|███████████▎              | 25.3/60.0s
```

If duration can't be detected (rare), conversion still works but without a progress bar.

---

## 🧠 Internals

- Uses `ffprobe` to get media duration  
- Uses `ffmpeg -progress pipe:1` to receive real-time timestamps  
- Parses `out_time_ms` or `out_time`  
- Feeds progress into `tqdm`  

---

## ⚖ FFmpeg License Note

This tool uses **FFmpeg** but does not bundle it.

FFmpeg is licensed under **GNU LGPL 2.1** or **GNU GPL 2.0**, depending on the build.  
See: https://ffmpeg.org/legal.html

`convert-audio-tool` is *not affiliated* with FFmpeg.

---

## 📄 License

```
MIT License  
© 2025 Petr Němec
```
