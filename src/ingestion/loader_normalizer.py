# src/ingestion/loader_normalizer.py

import csv
import os
import re
import unicodedata
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Common stopwords for requirements
STOPWORDS = {"the", "shall", "must", "should", "and", "to", "all", "after", "before", "be", "using"}

def remove_accents(text):
    """Remove accents and diacritics from text."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

def normalize_text(text):
    """
    Normalize requirement text:
    - Convert to lowercase
    - Remove accents
    - Remove stopwords
    - Keep only letters and numbers
    """
    text = text.lower()
    text = remove_accents(text)
    # Remove everything that is not letters, numbers, or spaces
    text = re.sub(r'[^a-z0-9\s]', '', text)
    # Tokenize and remove stopwords
    tokens = [t for t in text.split() if t not in STOPWORDS]
    # Sort tokens alphabetically (optional, improves matching)
    tokens.sort()
    normalized = ' '.join(tokens)
    return normalized

def load_requirements(csv_path):
    """
    Load requirements from CSV and return a list of dictionaries with:
    - id
    - source
    - original_text
    - normalized_text
    """
    requirements = []
    logger.info(f"Loading requirements from: {csv_path}")

    # Check if the file exists
    if not os.path.exists(csv_path):
        logger.critical(f"CRITICAL_ERROR: Requirements CSV file does not exist: {csv_path}")
        logger.info("Run aborted safely - Cannot continue without requirements CSV file")
        raise FileNotFoundError(f"CSV file does not exist: {csv_path}")

    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # Verify required columns are present
            if 'id' not in reader.fieldnames or 'text' not in reader.fieldnames:
                logger.critical("CRITICAL_ERROR: CSV does not have required 'id' and 'text' columns for RQS format")
                logger.info("Run aborted safely - Invalid CSV format for requirements")
                raise ValueError("CSV does not have required 'id' and 'text' columns")

            for row_num, row in enumerate(reader, start=2):  # start=2 because header is 1
                req_id = row.get('id', '').strip()
                original = row.get('text', '').strip()

                # Verify required fields are not empty
                if not req_id:
                    logger.error(f"ERROR: Row {row_num}: 'id' field is empty")
                    logger.info("Run aborted safely - Incomplete requirements data")
                    raise ValueError(f"Row {row_num}: 'id' field is empty")
                if not original:
                    logger.error(f"ERROR: Row {row_num}: 'text' field is empty")
                    logger.info("Run aborted safely - Incomplete requirements data")
                    raise ValueError(f"Row {row_num}: 'text' field is empty")

                normalized = normalize_text(original)
                requirements.append({
                    'id': req_id,
                    'source': 'doors_exports',
                    'original_text': original,
                    'normalized_text': normalized
                })
                logger.debug(f"{req_id} | Normalized: {normalized}")
    except Exception as e:
        logger.error(f"Error loading CSV: {e}")
        raise

    if not requirements:
        logger.error("No valid requirements found in CSV")
        raise ValueError("No valid requirements found in CSV")

    logger.info(f"Total requirements loaded: {len(requirements)}")
    return requirements
