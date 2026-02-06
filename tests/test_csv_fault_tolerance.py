import runpy
import pandas as pd
import pytest
from pandas import DataFrame


def _clusters_df():
    return DataFrame({'requirement_id': ['R1', 'R2'], 'cluster_id': ['C1', 'C2']})


def _reqs_df():
    return DataFrame({'id': ['R1', 'R2'], 'text': ['foo', 'bar'], 'domain': ['SECURITY', 'USABILITY']})


def _matches_df_missing_match_type():
    # Intentionally omit 'Match_Type' column
    return DataFrame({'ID1': ['R1'], 'ID2': ['R2'], 'Score': [95]})


def test_missing_match_type_column_raises_keyerror(monkeypatch):
    """If matches CSV is missing 'Match_Type', dashboard generation should fail with KeyError."""

    def fake_read_csv(path, *args, **kwargs):
        if 'clusters.csv' in str(path):
            return _clusters_df()
        if 'reqs.csv' in str(path):
            return _reqs_df()
        if 'matches.csv' in str(path):
            return _matches_df_missing_match_type()
        # default safe empty
        return DataFrame()

    monkeypatch.setattr(pd, 'read_csv', fake_read_csv)

    with pytest.raises(KeyError):
        runpy.run_module('reporting.scripts.dashboard', run_name='__main__')


def test_empty_matches_csv_raises_emptydataerror(monkeypatch):
    """If matches CSV is empty, ensure pandas EmptyDataError is propagated."""
    def fake_read_csv(path, *args, **kwargs):
        if 'matches.csv' in str(path):
            raise pd.errors.EmptyDataError("No columns to parse from file")
        if 'clusters.csv' in str(path):
            return _clusters_df()
        if 'reqs.csv' in str(path):
            return _reqs_df()
        return DataFrame()

    monkeypatch.setattr(pd, 'read_csv', fake_read_csv)

    with pytest.raises(pd.errors.EmptyDataError):
        runpy.run_module('reporting.scripts.dashboard', run_name='__main__')


def test_malformed_matches_csv_raises_parsererror(monkeypatch):
    """If matches CSV is malformed, ensure pandas ParserError is propagated."""
    def fake_read_csv(path, *args, **kwargs):
        if 'matches.csv' in str(path):
            raise pd.errors.ParserError("Error tokenizing data")
        if 'clusters.csv' in str(path):
            return _clusters_df()
        if 'reqs.csv' in str(path):
            return _reqs_df()
        return DataFrame()

    monkeypatch.setattr(pd, 'read_csv', fake_read_csv)

    with pytest.raises(pd.errors.ParserError):
        runpy.run_module('reporting.scripts.dashboard', run_name='__main__')