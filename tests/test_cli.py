from yadc import cli


def test_cli(capsys):
    cli.main()
    captured = capsys.readouterr()
    assert "does not currently have a CLI" in captured.out
    assert not captured.err
