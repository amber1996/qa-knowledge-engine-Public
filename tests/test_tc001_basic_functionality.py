import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import pandas as pd
import src.ingestion.loader_normalizer as loader_normalizer
import src.engine.fuzzy_matcher as fuzzy_matcher
import src.reporting.scripts.clustering as clustering
import src.reporting.csv_report as csv_report
import src.utils.config as config

class TestTC001BasicFunctionality:
    """TC001: Test basic functionality with small dataset"""

    def test_load_requirements(self):
        """Test loading requirements from small CSV"""
        test_csv = "data/raw/doors_exports/test_reqs.csv"
        reqs = loader_normalizer.load_requirements(test_csv)

        assert len(reqs) == 10, f"Expected 10 requirements, got {len(reqs)}"
        assert all('id' in req for req in reqs), "All requirements should have 'id'"
        assert all('normalized_text' in req for req in reqs), "All requirements should have 'normalized_text'"

    def test_fuzzy_matching(self):
        """Test fuzzy matching on small dataset"""
        test_csv = "data/raw/doors_exports/test_reqs.csv"
        reqs = loader_normalizer.load_requirements(test_csv)

        output_csv = "data/processed/test_matches.csv"
        fuzzy_matcher.fuzzy_compare(reqs, output_csv=output_csv)

        assert os.path.exists(output_csv), "Matches CSV should be created"

        df = pd.read_csv(output_csv)
        expected_matches = len(reqs) * (len(reqs) - 1) // 2  # n choose 2
        assert len(df) == expected_matches, f"Expected {expected_matches} matches, got {len(df)}"

    def test_clustering(self):
        """Test clustering on small dataset"""
        test_csv = "data/raw/doors_exports/test_reqs.csv"
        reqs = loader_normalizer.load_requirements(test_csv)

        output_csv = "data/processed/test_matches.csv"
        fuzzy_matcher.fuzzy_compare(reqs, output_csv=output_csv)

        matches_df = pd.read_csv(output_csv)
        all_ids = [req['id'] for req in reqs]
        clusters = clustering.build_clusters(matches_df, all_ids=all_ids)

        assert isinstance(clusters, list), "Clusters should be a list"
        assert len(clusters) > 0, "Should find at least one cluster"
        # Check that all requirements are in some cluster
        all_req_ids = set(req['id'] for req in reqs)
        clustered_ids = set()
        for cluster in clusters:
            clustered_ids.update(cluster)
        assert all_req_ids == clustered_ids, "All requirements should be in clusters"

    def test_report_generation(self):
        """Test report generation on small dataset"""
        test_csv = "data/raw/doors_exports/test_reqs.csv"
        reqs = loader_normalizer.load_requirements(test_csv)

        output_csv = "data/processed/test_matches.csv"
        fuzzy_matcher.fuzzy_compare(reqs, output_csv=output_csv)

        summary_csv = "data/processed/test_summary.csv"
        excel_report = "data/processed/test_summary.xlsx"

        csv_report.generate_summary_report(
            matches_csv=output_csv,
            summary_csv=summary_csv,
            excel_report=excel_report
        )

        assert os.path.exists(summary_csv), "Summary CSV should be created"
        assert os.path.exists(excel_report), "Excel report should be created"

        df = pd.read_csv(summary_csv)
        assert len(df) > 0, "Summary should have data"

    def test_full_pipeline(self):
        """Test the complete pipeline with small dataset"""
        # This test runs the entire process
        test_csv = "data/raw/doors_exports/test_reqs.csv"
        reqs = loader_normalizer.load_requirements(test_csv)

        # Fuzzy matching
        output_csv = "data/processed/test_matches.csv"
        fuzzy_matcher.fuzzy_compare(reqs, output_csv=output_csv)

        # Clustering
        matches_df = pd.read_csv(output_csv)
        all_ids = [req['id'] for req in reqs]
        clusters = clustering.build_clusters(matches_df, all_ids=all_ids)

        # Reports
        summary_csv = "data/processed/test_summary.csv"
        excel_report = "data/processed/test_summary.xlsx"
        csv_report.generate_summary_report(
            matches_csv=output_csv,
            summary_csv=summary_csv,
            excel_report=excel_report
        )

        # Assertions
        assert len(reqs) == 10
        assert len(clusters) > 0
        assert os.path.exists(summary_csv)
        assert os.path.exists(excel_report)

        print("TC001: Basic functionality test passed!")