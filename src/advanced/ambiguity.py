import re
import yaml
import os

# Load ambiguity rules from YAML
config_path = os.path.join(os.path.dirname(__file__), "..", "..", "config", "ambiguity_rules.yaml")
with open(config_path, 'r') as f:
    ambiguity_config = yaml.safe_load(f)

WEAK_VERBS = ambiguity_config['ambiguity']['weak_verbs']
VAGUE_TERMS = ambiguity_config['ambiguity']['vague_terms']
OPEN_CONDITIONS = ambiguity_config['ambiguity']['open_conditions']

# Icon thresholds from config
ICON_THRESHOLDS = ambiguity_config['ambiguity']['thresholds']

def has_measurement(text: str) -> bool:
    """
    Check if requirement text contains measurable criteria.
    """
    # Patterns that indicate measurable criteria
    measurement_patterns = [
        r'\d+',  # numbers
        r'\b\d+\s*(seconds?|minutes?|hours?|days?|weeks?|months?|years?)\b',  # time units
        r'\b\d+\s*(mb|gb|kb|bytes?|pixels?|percent|%)\b',  # data/size units
        r'\b\d+\s*(users?|requests?|connections?|items?)\b',  # countable items
        r'\b(at least|at most|maximum|minimum|between|within)\b',  # quantitative constraints
        r'\b\d+\.\d+\b',  # decimal numbers
        r'\b\d+/\d+\b',  # fractions
    ]

    return any(re.search(pattern, text, re.IGNORECASE) for pattern in measurement_patterns)

def get_icon_thresholds():
    """
    Get icon display thresholds from configuration.
    Returns dict with 'review' and 'ambiguous' thresholds.
    """
    return ICON_THRESHOLDS

def get_ambiguity_icons(score):
    """
    Return icons based on ambiguity score using configured thresholds.
    """
    thresholds = get_icon_thresholds()
    
    if score >= thresholds['ambiguous']:
        return " 🟠"  # high ambiguity - needs rewrite
    elif score >= thresholds['review']:
        return " 🔎"  # moderate ambiguity - needs review
    else:
        return ""  # no icon

def detect_ambiguity(requirement_text: str) -> dict:
    """
    MVP ambiguity detector.
    Returns score and human-readable reasons.
    """

    text = requirement_text.lower()
    score = 0
    reasons = []

    # 1️⃣ Weak verbs
    found_weak_verbs = [v for v in WEAK_VERBS if v in text]
    if found_weak_verbs:
        score += 2
        reasons.append(f"weak verb(s): {', '.join(found_weak_verbs)}")

    # 2️⃣ Vague terms
    found_vague_terms = [t for t in VAGUE_TERMS if t in text]
    if found_vague_terms:
        score += 2
        reasons.append(f"vague term(s): {', '.join(found_vague_terms)}")

    # 3️⃣ Open conditions
    found_open_conditions = [c for c in OPEN_CONDITIONS if c in text]
    if found_open_conditions:
        score += 1
        reasons.append(f"open condition(s): {', '.join(found_open_conditions)}")

    # 4️⃣ No measurable criteria
    if not has_measurement(text):
        score += 1
        reasons.append("no measurable criteria")

    return {
        "ambiguity_score": score,
        "ambiguity_reasons": "; ".join(reasons) if reasons else ""
    }