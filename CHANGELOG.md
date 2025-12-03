# Changelog
All notable changes to this project will be documented in this file.

The format is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.2.0] – 2025-12-04
### Added
- Video support: can now convert simple video containers (e.g. `.mxf`, `.mov`, `.avi`) to other formats such as `.mp4` using the same CLI interface.
- Per-file progress bar based on FFmpeg `-progress pipe:1` output (`out_time_ms` / `out_time` parsing) for both audio and video conversions. :contentReference[oaicite:1]{index=1}
- Basic test suite:
  - Import test for the package.
  - CLI argument parsing tests.
  - Tests for file iteration / extension filtering.
- Expanded documentation:
  - README describes video conversion, progress bar behaviour, and supported extensions. :contentReference[oaicite:2]{index=2}

### Changed
- Refactored the project to a modern `src/` layout:
  - Package now lives in `src/convert_audio_tool/` with `core.py` and `cli.py`.
  - CLI entry point now targets `convert_audio_tool.cli:main`.
- Internals split into:
  - `core` module with reusable conversion logic.
  - `cli` module handling argument parsing and config.
- Improved configuration loading/saving and argument parsing to be easier to test (e.g. `parse_args(argv=None)`).

### Fixed
- Ensured the `convert-audio` CLI uses the installed package (editable install) rather than stale copies, avoiding confusion when the script changed but the entry point didn’t.
- Made progress display robust when media duration is missing by gracefully falling back to a no-progress-bar mode.

---

## [0.1.0] – 2025-??-??
### Added
- Initial release of `convert-audio-tool`.
- Batch audio conversion using FFmpeg.
- Support for common audio formats (e.g. `.wav`, `.flac`, `.aac`, `.ogg`, `.mp3`, `.mp4`, `.m4a`).
- Optional recursion, archiving of original files, overwrite behaviour, and saved default folders via a simple JSON config.
