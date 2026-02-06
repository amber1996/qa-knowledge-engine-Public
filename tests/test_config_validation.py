import pytest
from src.utils.config import validate_config


def test_valid_config_passes():
    cfg = {
        'paths': {
            'reqs_csv': 'data/raw/doors_exports/reqs.csv',
            'clusters_csv': 'data/raw/doors_exports/clusters.csv',
            'matches_csv': 'data/processed/matches.csv',
            'summary_csv': 'data/processed/summary.csv',
            'dashboard_html': 'reports/dashboard.html',
        },
        'thresholds': {'duplicate': 90, 'similar': 80}
    }

    # Should not raise in strict mode
    validate_config(cfg, strict=True)


def test_missing_paths_key_raises():
    with pytest.raises(ValueError) as e:
        validate_config({'thresholds': {'duplicate': 90}}, strict=True)
    assert "'paths'" in str(e.value)


def test_thresholds_invalid_raises():
    cfg = {
        'paths': {
            'reqs_csv': 'data/raw/doors_exports/reqs.csv',
            'clusters_csv': 'data/raw/doors_exports/clusters.csv',
            'matches_csv': 'data/processed/matches.csv',
            'summary_csv': 'data/processed/summary.csv',
            'dashboard_html': 'reports/dashboard.html',
        },
        'thresholds': {'duplicate': 200, 'similar': 'not-a-number'}
    }

    with pytest.raises(ValueError):
        validate_config(cfg, strict=True)


def test_non_strict_mode_returns_issues_and_warns(monkeypatch):
    # Provide an intentionally invalid configuration
    cfg = {
        'paths': {
            'reqs_csv': 'does_not_exist.csv',
        },
        'thresholds': {'duplicate': 'NaN'}
    }

    # In non-strict mode, the function should return a list of issues instead
    # of raising an exception.
    issues = validate_config(cfg, strict=False)
    assert isinstance(issues, list) and len(issues) > 0