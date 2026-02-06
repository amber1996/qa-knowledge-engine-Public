import os
import sys
import runpy
from pathlib import Path


def test_e2e_offline_generates_dashboard(tmp_path, monkeypatch):
    # Ensure src is importable
    repo_root = Path(__file__).resolve().parents[1]
    src_dir = str(repo_root / 'src')
    monkeypatch.syspath_prepend(src_dir)

    # Remove existing dashboard if present
    dashboard = repo_root / 'reports' / 'dashboard.html'
    if dashboard.exists():
        dashboard.unlink()

    # Execute the dashboard module as a script (isolated run)
    runpy.run_module('reporting.scripts.dashboard', run_name='__main__')

    # Assert dashboard file now exists and has expected content
    assert dashboard.exists(), "Dashboard was not generated"
    content = dashboard.read_text(encoding='utf-8')
    assert 'QA Requirement Similarity Dashboard' in content
    # Quick sanity checks for summary and some table headers
    assert '<h2>Summary</h2>' in content
    assert '<th>ID 1</th>' in content