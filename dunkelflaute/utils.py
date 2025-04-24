import os
import pandas as pd


def create_ts_from_raw(file_path, yr_range):
    """
    Create a dataframe with wind and solar data time series both as normalized to maximum capacity
    """
    df_all = pd.DataFrame()
    for yr in yr_range:
        date_time = pd.date_range(
            start=f"{yr}-01-01 00:00:00", end=f"{yr}-12-31 23:00:00", freq="h"
        )

        fn_wind = os.path.join(file_path, f"DEU1_ONSHORE_IEC_3_LCOE_1_{yr}_ts.csv")
        df_wind = pd.read_csv(fn_wind, header=3)
        df_wind.dropna(inplace=True)
        df_wind.rename(columns={f"{yr}": "wind"}, inplace=True)
        df_wind["datetime"] = date_time
        df_wind.rename(columns={f"{yr}": "wind"}, inplace=True)
        df_wind.set_index("datetime", inplace=True)

        fn_solar = os.path.join("data", "raw", f"DEU1_SOLAR_ROOFTOP_LCOE_1_{yr}_ts.csv")
        df_solar = pd.read_csv(fn_solar, header=3)
        df_solar.dropna(inplace=True)
        df_solar.rename(columns={f"{yr}": "solar"}, inplace=True)
        df_solar["datetime"] = date_time
        df_solar.rename(columns={f"{yr}": "solar"}, inplace=True)
        df_solar.set_index("datetime", inplace=True)

        df_yr = pd.concat([df_wind, df_solar], axis=1)
        if df_all.empty:
            df_all = df_yr
        else:
            df_all = pd.concat([df_all, df_yr], axis=0)

    return df_all


def load_df(file_path):
    """
    Load a dataframe from a CSV file
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist")

    df = pd.read_csv(file_path, index_col=0, parse_dates=True)

    if df.empty:
        raise ValueError(f"File {file_path} is empty")
    if not all(df.columns.isin(["wind", "solar"])):
        raise ValueError(f"File {file_path} should contain 'wind' and 'solar' columns")
    if not df.index.isin(
        pd.date_range(start=df.index[0], end=df.index[-1], freq="h")
    ).all():
        raise ValueError(
            f"File {file_path} should have a datetime index with hourly frequency"
        )
    if not pd.api.types.is_datetime64_any_dtype(df.index):
        raise ValueError(f"File {file_path} should have a datetime index")

    return df


def validate_capacity_mix(cap_mix):
    if not isinstance(cap_mix, list):
        raise ValueError("cap_mix should be a list")
    if len(cap_mix) == 0:
        raise ValueError("cap_mix should not be empty")
    if any([cap < 0 or cap > 1 for cap in cap_mix]):
        raise ValueError("cap_mix should be between 0 and 1")


def validate_dataframe(df):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("df should be a pandas dataframe")


def validate_threshold(threshold):
    if not isinstance(threshold, (int, float)):
        raise ValueError("threshold should be a number")


def validate_period_length(period_len):
    if not isinstance(period_len, int):
        raise ValueError("period_len should be an integer")


def validate_tolerance(tol):
    if not isinstance(tol, int):
        raise ValueError("tol should be an integer")


def validate_thresholds(thresholds):
    if not isinstance(thresholds, list):
        raise ValueError("thresholds should be a list")
    if len(thresholds) == 0:
        raise ValueError("thresholds should not be empty")
