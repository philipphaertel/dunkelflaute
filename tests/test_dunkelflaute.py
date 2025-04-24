from dunkelflaute.core import get_total_production_df, find_fuzzy_periods, get_dunkelflaute_results
import pandas as pd
import pytest

def test_get_total_production_df():
    df = pd.DataFrame({
        'wind': [0.1, 0.2, 0.3],
        'solar': [0.4, 0.5, 0.6]
    })
    cap_mix = [0.5]
    result = get_total_production_df(df, cap_mix)
    expected = pd.DataFrame({
        'w0.50_s0.50': [0.25, 0.35, 0.45]
    })
    pd.testing.assert_frame_equal(result, expected)

def test_find_fuzzy_periods():
    df = pd.DataFrame({
        'wind': [0.1, 0.0, 0.0, 0.1, 0.2],
        'solar': [0.4, 0.5, 0.0, 0.0, 0.1]
    })
    threshold = 0.1
    period_len = 3
    result = find_fuzzy_periods(df, threshold, period_len)
    expected = {
        'wind': [(pd.Timestamp('2000-01-01 00:00:00'), pd.Timestamp('2000-01-01 02:00:00'))],
        'solar': [(pd.Timestamp('2000-01-01 01:00:00'), pd.Timestamp('2000-01-01 02:00:00'))]
    }
    assert result == expected

def test_get_dunkelflaute_results():
    df = pd.DataFrame({
        'wind': [0.1, 0.2, 0.3],
        'solar': [0.4, 0.5, 0.6]
    })
    thresholds = [0.1]
    period_lengths = [2]
    result = get_dunkelflaute_results(df, thresholds, period_lengths)
    assert isinstance(result, dict)
    assert len(result) == len(thresholds)  # Check number of thresholds

# Additional tests can be added for edge cases and other functionalities.