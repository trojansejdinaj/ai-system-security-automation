import runpy


def test_module_entrypoint_runs():
    """Ensure `python -m security_automation` executes without error."""
    runpy.run_module("security_automation", run_name="__main__")
