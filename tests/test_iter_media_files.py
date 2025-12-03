from pathlib import Path

from convert_audio_tool.core import iter_media_files, MEDIA_EXTENSIONS


def test_iter_media_files_filters_extensions(tmp_path: Path):
    # create some fake files
    audio = tmp_path / "sound.wav"
    video = tmp_path / "clip.mxf"
    other = tmp_path / "notes.txt"

    audio.write_bytes(b"A")
    video.write_bytes(b"B")
    other.write_bytes(b"C")

    files = list(iter_media_files(tmp_path, recursive=False))

    # all paths are strings
    assert all(isinstance(p, str) for p in files)

    # expected media files present
    assert str(audio) in files
    assert str(video) in files

    # non-media extension should not be present
    assert str(other) not in files

    # sanity: our extensions tuple contains wav, mxf
    assert ".wav" in MEDIA_EXTENSIONS
    assert ".mxf" in MEDIA_EXTENSIONS
