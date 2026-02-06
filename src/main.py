# src/main.py
import sys
import os

# Add project root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.utils.logger import get_logger
from src.utils.config import PATHS, THRESHOLDS
from ingestion.loader_normalizer import load_requirements
from engine.fuzzy_matcher import fuzzy_compare
from reporting.csv_report import generate_summary_report
from reporting.scripts.clustering import build_clusters
import pandas as pd

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("STARTING QA KNOWLEDGE ENGINE")
    logger.info("=" * 60)

    # 1. Load requirements
    logger.info("\n[1/4] Loading requirements...")
    reqs = load_requirements(PATHS['reqs_csv'])
    logger.info(f"✓ {len(reqs)} requirements loaded")

    # 2. Fuzzy comparison
    logger.info("\n[2/4] Running fuzzy comparison...")
    fuzzy_compare(reqs,
                  threshold_duplicate=THRESHOLDS['duplicate'],
                  threshold_similar=THRESHOLDS['similar'],
                  output_csv=PATHS['matches_csv'])
    logger.info("✓ Matches saved in matches.csv")

    # 3. Clustering
    logger.info("\n[3/4] Running clustering...")
    matches_df = pd.read_csv(PATHS['matches_csv'])
    clusters = build_clusters(matches_df)
    with open(PATHS['clusters_csv'], 'w') as f:
        f.write("cluster_id,requirement_id\n")
        for i, cluster in enumerate(clusters):
            for req_id in cluster:
                f.write(f"{i},{req_id}\n")
    logger.info(f"✓ {len(clusters)} clusters identified")

    # 4. Report
    logger.info("\n[4/4] Generating reports...")
    generate_summary_report(
        matches_csv=PATHS['matches_csv'],
        summary_csv=PATHS['summary_csv'],
        excel_report=PATHS['excel_report']
    )
    logger.info("✓ Reports generated")

    logger.info("\n" + "=" * 60)
    logger.info("✓ PROCESS COMPLETED SUCCESSFULLY")
    logger.info("=" * 60)
