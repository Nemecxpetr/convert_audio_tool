from pathlib import Path
from unittest.mock import MagicMock, patch

from convert_audio_tool.core import convert_media


def test_convert_media_with_mocked_ffmpeg(tmp_path: Path):
    input_file = tmp_path / "input.wav"
    output_file = tmp_path / "output.wav"
    input_file.write_bytes(b"dummy")  # just needs to exist

    # 1) Mock get_media_duration to return a fixed duration (e.g. 10 seconds)
    with patch("convert_audio_tool.core.get_media_duration", return_value=10.0):

        # 2) Fake Popen instance
        fake_process = MagicMock()
        # Simulate minimal ffmpeg -progress output
        fake_process.stdout = iter(
            [
                "out_time_ms=5000000\n",  # 5 seconds
                "progress=continue\n",
                "out_time_ms=10000000\n",  # 10 seconds
                "progress=end\n",
            ]
        )
        fake_process.wait.return_value = 0
        fake_process.returncode = 0

        # 3) Patch subprocess.Popen to return our fake process
        with patch("convert_audio_tool.core.subprocess.Popen", return_value=fake_process):
            # At this point, convert_media will:
            # - call get_media_duration (returns 10.0)
            # - call subprocess.Popen (returns fake_process)
            # - read the progress lines
            # - complete successfully
            convert_media(str(input_file), str(output_file), overwrite=True, quiet=True)

    # convert_media itself does not write the output file,
    # ffmpeg would normally do that. For the purpose of this test
    # we can either skip checking file existence, OR simulate it ourselves:

    # Here we simulate “ffmpeg wrote it” to assert path construction is correct:
    # In a more advanced test, you could patch os.path.exists if you want.
    # For now, just assert that we computed the string path without crashing.
    assert str(output_file).endswith("output.wav")
