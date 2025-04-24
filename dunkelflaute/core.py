import pandas as pd
import time


def get_total_production_df(df, cap_mix: list = [0.5], cap_dem_ratio: float = 1.0):
    """
    Get the total production dataframe for a given dataframe, capacity mix and
    capacity demand ratio. The total production is calculated as the sum of
    wind and solar production multiplied by the capacity mix and capacity
    demand ratio. The function returns a dataframe with the following structure:
    {
        'w0.50_s0.50': [production, ...],
        'w0.75_s0.25': [production, ...],
        ...
    }
    """

    if not isinstance(cap_mix, list):
        raise ValueError("cap_mix should be a list")
    if len(cap_mix) == 0:
        raise ValueError("cap_mix should not be empty")
    if any([cap < 0 or cap > 1 for cap in cap_mix]):
        raise ValueError("cap_mix should be between 0 and 1")

    df_total = pd.DataFrame(index=df.index)
    for cap in cap_mix:
        df_total[f"w{cap:2.2f}_s{1-cap:2.2f}"] = cap_dem_ratio * df[
            "wind"
        ] * cap + cap_dem_ratio * df["solar"] * (1 - cap)
    return df_total


def find_fuzzy_periods(df, threshold=0.1, period_len=7 * 24, tol=0):
    """
    Find periods in a dataframe where the values are below a given threshold
    for a certain period length. The periods are defined as consecutive
    time intervals where the values are below the threshold.
    The function returns a dictionary with the following structure:
    {
        column_name: [
            (start_time, end_time),
            ...
        ]
    }
    """

    if not isinstance(df, pd.DataFrame):
        raise ValueError("df should be a pandas dataframe")
    if not isinstance(threshold, (int, float)):
        raise ValueError("threshold should be a number")
    if not isinstance(period_len, int):
        raise ValueError("period_len should be an integer")
    if not isinstance(tol, int):
        raise ValueError("tol should be an integer")

    results = {}
    time_grouper = 0
    time_condition = 0
    time_filter = 0

    for col in df.columns:
        # Create a grouper for consecutive periods below the threshold
        start_time = time.time()
        group_ids = df[col].le(threshold).diff().ne(0).cumsum()
        # Reset index to make it accessible in groupby
        df["group_id"] = group_ids
        df_reset = df.reset_index()

        time_grouper += time.time() - start_time

        # Compute group statistics in a vectorized way
        start_time = time.time()
        group_stats = df_reset.groupby("group_id").agg(
            start=("datetime", "first"),
            end=("datetime", "last"),
            max_value=(col, "max"),
        )
        group_stats["duration"] = (
            group_stats["end"] - group_stats["start"]
        ).dt.total_seconds() / 3600
        time_condition += time.time() - start_time

        # Filter groups based on conditions
        start_time = time.time()
        valid_groups = group_stats[
            (group_stats["max_value"] <= threshold)
            & (group_stats["duration"] >= period_len)
        ]
        periods = list(zip(valid_groups["start"], valid_groups["end"]))
        time_filter += time.time() - start_time

        results[col] = periods

    # print(f"Time taken for grouper: {time_grouper:.2f} seconds")
    # print(f"Time taken for condition: {time_condition:.2f} seconds")
    # print(f"Time taken for filter: {time_filter:.2f} seconds")
    return results


def get_dunkelflaute_results(df, thresholds, period_lenghts):
    """
    Get the dunkelflaute results for a given dataframe, thresholds and period lengths.
    The results are stored in a dictionary with the following structure:
    {
        threshold: {
            period_length: {
                'w0.50_s0.50': [(start, end), ...],
                ...
            },
            ...
        },
        ...
    }
    """

    if not isinstance(thresholds, list):
        raise ValueError("thresholds should be a list")
    if len(thresholds) == 0:
        raise ValueError("thresholds should not be empty")

    result = {}
    for threshold in thresholds:
        result[threshold] = {}
        for period_len in period_lenghts:
            print(
                f"Found periods for threshold={threshold}, min. period length={period_len}"
            )
            result[threshold][period_len] = find_fuzzy_periods(
                df, threshold=threshold, period_len=period_len
            )

    return result
