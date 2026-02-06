# src/engine/fuzzy_matcher.py

from fuzzywuzzy import fuzz
import csv
import os
from src.utils.logger import get_logger

logger = get_logger(__name__)

def fuzzy_compare(requirements, threshold_duplicate=90, threshold_similar=80, output_csv=None):
    """
    Compare each requirement with others using FuzzyWuzzy.
    Save results in CSV with ID1, ID2, score, match type.
    """
    if output_csv is None:
        raise ValueError("output_csv must be provided")

    logger.info("Starting fuzzy comparison between requirements")

    with open(output_csv, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["ID1", "ID2", "Score", "Match_Type"])

        total = len(requirements)
        for i in range(total):
            req_i = requirements[i]
            for j in range(i+1, total):
                req_j = requirements[j]

                score = fuzz.token_set_ratio(req_i['normalized_text'], req_j['normalized_text'])

                if score >= threshold_duplicate:
                    match_type = "DUPLICATE"
                elif score >= threshold_similar:
                    match_type = "SIMILAR"
                else:
                    match_type = "DIFFERENT"

                writer.writerow([req_i['id'], req_j['id'], score, match_type])
                logger.debug(f"{req_i['id']} vs {req_j['id']} | Score={score} | {match_type}")

    logger.info(f"Comparison complete. Results saved in {output_csv}")
