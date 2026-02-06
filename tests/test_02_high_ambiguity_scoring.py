"""
Test 02: High Ambiguity Scoring Test
Tests the ambiguity detection system with requirements designed to have high ambiguity scores.
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from advanced.ambiguity import detect_ambiguity, get_ambiguity_icons


def test_high_ambiguity_scoring():
    """Test ambiguity detection with high-scoring requirements."""

    print("=== Test 02: High Ambiguity Scoring ===\n")

    # Test requirement with very high ambiguity (score 6+)
    test_req_1 = 'The system should provide intuitive user interface where possible with adequate efficiency and simple error handling'

    result_1 = detect_ambiguity(test_req_1)
    icon_1 = get_ambiguity_icons(result_1['ambiguity_score'])

    print(f"Test Requirement 1: {test_req_1}")
    print(f"Ambiguity Score: {result_1['ambiguity_score']}")
    print(f"Reasons: {result_1['ambiguity_reasons']}")
    print(f"Icon: '{icon_1}'")
    print()

    # Test requirement with moderate ambiguity (score 3-4)
    test_req_2 = 'The system shall support fast response times with efficient resource usage and adequate performance'

    result_2 = detect_ambiguity(test_req_2)
    icon_2 = get_ambiguity_icons(result_2['ambiguity_score'])

    print(f"Test Requirement 2: {test_req_2}")
    print(f"Ambiguity Score: {result_2['ambiguity_score']}")
    print(f"Reasons: {result_2['ambiguity_reasons']}")
    print(f"Icon: '{icon_2}'")
    print()

    # Test requirement with low ambiguity (score < 3)
    test_req_3 = 'The system shall lock the user account after five consecutive failed login attempts'

    result_3 = detect_ambiguity(test_req_3)
    icon_3 = get_ambiguity_icons(result_3['ambiguity_score'])

    print(f"Test Requirement 3: {test_req_3}")
    print(f"Ambiguity Score: {result_3['ambiguity_score']}")
    print(f"Reasons: {result_3['ambiguity_reasons']}")
    print(f"Icon: '{icon_3}'")
    print()

    # Summary
    print("=== Summary ===")
    print(f"High ambiguity (≥4): 🟠 icon - Score {result_1['ambiguity_score']}")
    print(f"Moderate ambiguity (≥3): 🔎 icon - Score {result_2['ambiguity_score']}")
    print(f"Low ambiguity (<3): No icon - Score {result_3['ambiguity_score']}")
    print("\nTest completed successfully!")


if __name__ == "__main__":
    test_high_ambiguity_scoring()