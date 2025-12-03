# tests/test_imports.py

def test_import_package():
    import convert_audio_tool

    # package exists
    assert convert_audio_tool is not None

    # core API should be exposed from __init__.py
    assert hasattr(convert_audio_tool, "convert_folder")
    assert hasattr(convert_audio_tool, "convert_media")
