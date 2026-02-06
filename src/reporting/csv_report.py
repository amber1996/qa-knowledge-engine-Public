# src/reporting/csv_report.py

import pandas as pd
import os
from src.utils.logger import get_logger

logger = get_logger(__name__)

def generate_summary_report(matches_csv, summary_csv, excel_report):
    # Create folder if it doesn't exist
    os.makedirs(os.path.dirname(summary_csv), exist_ok=True)

    logger.info(f"Loading matches from: {matches_csv}")
    df = pd.read_csv(matches_csv)

    # Summary by type
    summary = df['Match_Type'].value_counts().reset_index()
    summary.columns = ['Match_Type', 'Count']
    logger.info(f"Summary:\n{summary}")

    # Save summary in CSV
    summary.to_csv(summary_csv, index=False)
    logger.info(f"Summary saved in CSV: {summary_csv}")

    # Save detail with colors in Excel (duplicates red, similar yellow, different green)
    with pd.ExcelWriter(excel_report, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Matches', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Matches']

        # Color formats
        red_format = workbook.add_format({'bg_color': '#FF9999'})
        yellow_format = workbook.add_format({'bg_color': '#FFFF99'})
        green_format = workbook.add_format({'bg_color': '#99FF99'})
        for row_num, match_type in enumerate(df['Match_Type'], start=1):  # Excel rows start at 1
            if match_type == "DUPLICATE":
                worksheet.set_row(row_num, cell_format=red_format)
            elif match_type == "SIMILAR":
                worksheet.set_row(row_num, cell_format=yellow_format)
            elif match_type == "DIFFERENT":
                worksheet.set_row(row_num, cell_format=green_format)
    logger.info(f"Excel report generated: {excel_report}")