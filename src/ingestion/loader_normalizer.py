# src/ingestion/loader_normalizer.py

import csv
import unicodedata
import re
from utils.logger import get_logger

logger = get_logger(__name__)

# --- STOPWORDS comunes para requisitos ---
STOPWORDS = {"the", "shall", "must", "should", "and", "to", "all", "after", "before", "be", "using"}

# --- Funciones ---

def remove_accents(text):
    """Quita acentos y tildes del texto"""
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

def normalize_text(text):
    """
    Normaliza texto de requisito:
    - Lowercase
    - Quita acentos
    - Quita stopwords
    - Solo letras y números
    """
    text = text.lower()
    text = remove_accents(text)
    # Quitar todo lo que no sea letras, números o espacios
    text = re.sub(r'[^a-z0-9\s]', '', text)
    # Tokenizar y eliminar stopwords
    tokens = [t for t in text.split() if t not in STOPWORDS]
    # Reordenar tokens alfabéticamente (opcional, mejora matching)
    tokens.sort()
    normalized = ' '.join(tokens)
    return normalized

def load_requirements(csv_path):
    """
    Carga CSV de requisitos y devuelve lista de diccionarios con:
    - id
    - source
    - original_text
    - normalized_text
    """
    requirements = []
    logger.info(f"Cargando requisitos desde: {csv_path}")
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            original = row['text']
            normalized = normalize_text(original)
            requirements.append({
                'id': row['id'],
                'source': 'doors_exports',
                'original_text': original,
                'normalized_text': normalized
            })
            logger.debug(f"{row['id']} | Normalizado: {normalized}")
    logger.info(f"Total requisitos cargados: {len(requirements)}")
    return requirements

# --- Test rápido ---
if __name__ == "__main__":
    csv_file = r"C:\Users\r-g-r\Desktop\Personal_portfolio\QA_PRIVATE_TOOL\qa_knowledge_engine\data\raw\doors_exports\reqs.csv"
    reqs = load_requirements(csv_file)
    for r in reqs:
        print(f"{r['id']} | {r['normalized_text']}")
