from convert_audio_tool.cli import parse_args

def test_parse_args_defaults():
    # empty list → behave like "no user args", but without picking up pytest args
    args = parse_args([])
    assert args.format == "wav"
    assert args.overwrite is False
    assert args.recursive is False
    assert args.quiet is False

def test_parse_args_custom():
    args = parse_args(["-f", "mp3", "-q", "--overwrite"])
    assert args.format == "mp3"
    assert args.quiet is True
    assert args.overwrite is True
