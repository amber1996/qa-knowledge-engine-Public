# src/main.py
import sys
import os

# Agregar directorio src al path
sys.path.insert(0, os.path.dirname(__file__))

from utils.logger import get_logger
from utils.config import PATHS, THRESHOLDS
from ingestion.loader_normalizer import load_requirements
from engine.fuzzy_matcher import fuzzy_compare
from reporting.csv_report import generate_summary_report
from reporting.scripts.clustering import build_clusters
import pandas as pd

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("INICIANDO QA KNOWLEDGE ENGINE")
    logger.info("=" * 60)
    
    # 1. Cargar requisitos
    logger.info("\n[1/4] Cargando requisitos...")
    reqs = load_requirements(PATHS['reqs_csv'])
    logger.info(f"✓ {len(reqs)} requisitos cargados")
    
    # 2. Comparación fuzzy
    logger.info("\n[2/4] Ejecutando comparación fuzzy...")
    fuzzy_compare(reqs, 
                  threshold_duplicate=THRESHOLDS['duplicate'],
                  threshold_similar=THRESHOLDS['similar'],
                  output_csv=PATHS['matches_csv'])
    logger.info("✓ Matches guardados en matches.csv")
    
    # 3. Clustering
    logger.info("\n[3/4] Ejecutando clustering...")
    matches_df = pd.read_csv(PATHS['matches_csv'])
    clusters = build_clusters(matches_df)
    with open(PATHS['clusters_csv'], 'w') as f:
        f.write("cluster_id,requirement_id\n")
        for i, cluster in enumerate(clusters):
            for req_id in cluster:
                f.write(f"{i},{req_id}\n")
    logger.info(f"✓ {len(clusters)} clusters identificados")
    
    # 4. Reporte
    logger.info("\n[4/4] Generando reportes...")
    generate_summary_report(
        matches_csv=PATHS['matches_csv'],
        summary_csv=PATHS['summary_csv'],
        excel_report=PATHS['excel_report']
    )
    logger.info("✓ Reportes generados")
    
    logger.info("\n" + "=" * 60)
    logger.info("✓ PROCESO COMPLETADO EXITOSAMENTE")
    logger.info("=" * 60)
