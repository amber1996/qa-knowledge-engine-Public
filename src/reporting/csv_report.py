# src/reporting/csv_report.py

import pandas as pd
import os
from utils.logger import get_logger

logger = get_logger(__name__)

def generate_summary_report(matches_csv=r"C:\Users\r-g-r\Desktop\Personal_portfolio\QA_PRIVATE_TOOL\qa_knowledge_engine\data\processed\matches.csv",
                            summary_csv=r"C:\Users\r-g-r\Desktop\Personal_portfolio\QA_PRIVATE_TOOL\qa_knowledge_engine\data\processed\summary.csv",
                            excel_report=r"C:\Users\r-g-r\Desktop\Personal_portfolio\QA_PRIVATE_TOOL\qa_knowledge_engine\data\processed\summary.xlsx"):
    # Crear carpeta si no existe
    os.makedirs(os.path.dirname(summary_csv), exist_ok=True)

    logger.info(f"Cargando matches desde: {matches_csv}")
    df = pd.read_csv(matches_csv)

    # Resumen por tipo
    summary = df['Match_Type'].value_counts().reset_index()
    summary.columns = ['Match_Type', 'Count']
    logger.info(f"Resumen:\n{summary}")

    # Guardar resumen en CSV
    summary.to_csv(summary_csv, index=False)
    logger.info(f"Resumen guardado en CSV: {summary_csv}")
  # Guardar detalle con colores en Excel (duplicados rojos, similares amarillos)
    with pd.ExcelWriter(excel_report, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Matches', index=False)
        workbook  = writer.book
        worksheet = writer.sheets['Matches']

        # Formato colores
        red_format = workbook.add_format({'bg_color': '#FF9999'})
        yellow_format = workbook.add_format({'bg_color': '#FFFF99'})
        green_format = workbook.add_format({'bg_color': '#99FF99'})
        for row_num, match_type in enumerate(df['Match_Type'], start=1):  # Excel rows start at 1
            if match_type == "DUPLICATE":
                worksheet.set_row(row_num, cell_format=red_format)
            elif match_type == "SIMILAR":
                  worksheet.set_row(row_num, cell_format=yellow_format)
            if match_type == "DIFFERENT":
                worksheet.set_row(row_num, cell_format=green_format)
    logger.info(f"Reporte Excel generado: {excel_report}")