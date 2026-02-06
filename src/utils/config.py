import yaml
import os
import logging

logger = logging.getLogger(__name__)


def load_config(config_file="config/paths.yaml"):
    """Load path configuration from YAML and return a dict.

    The `config_file` is interpreted relative to the project root (two levels up
    from this file) unless an absolute path is provided.
    """
    config_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", config_file))
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def validate_config(config, strict=True):
    """Validate a loaded configuration dict.

    If strict is True (default), raises ValueError on any validation issue.
    If strict is False, logs warnings for issues and returns a list of issue
    messages (but does not raise).
    """
    issues = []

    if not isinstance(config, dict):
        issues.append("Configuration must be a mapping/dict")
        if strict:
            raise ValueError(issues[0])
        for i in issues:
            logger.warning(i)
        return issues

    # Check top-level keys
    if 'paths' not in config:
        issues.append("Missing required top-level key: 'paths'")
    if 'thresholds' not in config:
        issues.append("Missing required top-level key: 'thresholds'")

    paths = config.get('paths', {})
    required_path_keys = ['reqs_csv', 'clusters_csv', 'matches_csv', 'summary_csv', 'dashboard_html']
    missing = [k for k in required_path_keys if k not in paths]
    if missing:
        issues.append(f"Missing required path keys in 'paths': {missing}")

    # Check that CSV files exist on disk (for files that should already be present)
    file_checks = ['reqs_csv', 'clusters_csv', 'matches_csv']
    not_found = [p for p in file_checks if not os.path.isfile(paths.get(p, ''))]
    if not_found:
        issues.append(f"Referenced files not found on disk: {not_found}")

    # Validate thresholds
    thresholds = config.get('thresholds', {})
    for key in ('duplicate', 'similar'):
        if key not in thresholds:
            issues.append(f"Missing threshold value: '{key}'")
            continue
        try:
            val = float(thresholds[key])
        except Exception:
            issues.append(f"Threshold '{key}' must be numeric")
            continue
        if not (0 <= val <= 100):
            issues.append(f"Threshold '{key}' must be between 0 and 100")

    if issues:
        if strict:
            raise ValueError("; ".join(issues))
        else:
            for i in issues:
                logger.warning(i)
            return issues

    # If no issues, return empty list in non-strict mode or None in strict mode
    return [] if not strict else None


# Load global config and validate on import with non-strict mode so the
# application can continue in non-critical environments; issues will be
# logged as warnings instead of raising at import time.
CONFIG = load_config()
validate_config(CONFIG, strict=False)
PATHS = CONFIG.get('paths', {})
THRESHOLDS = CONFIG.get('thresholds', {})
