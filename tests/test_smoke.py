from security_automation.main import main


def test_smoke_runs_without_error(capsys):
    main()
    captured = capsys.readouterr()
    assert "run_completed" in captured.out
