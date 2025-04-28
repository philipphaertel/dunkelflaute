from dunkelflaute.core import get_total_production_df, get_dunkelflaute_results
from dunkelflaute.utils import create_ts_from_raw, load_df, get_number_of_years
from dunkelflaute.visualize import (
    plot_dunkelflaute_events,
    plot_period_ts_data,
    plot_period_solar_wind_performance,
    plot_dunkelflaute_contour,
)


def main():
    # # Preprocess data (replace with your actual data loading logic)
    # fp_raw_data = "data/raw"
    # df = create_ts_from_raw(fp_raw_data, range(2006, 2013))

    # # Save the data to a CSV file
    # save_path = "data"
    # df.to_csv(f"{save_path}/wind_solar_data.csv", index=True)

    # Load the wind and solar production data (normalized) from a CSV file
    # The CSV file should contain two columns, 'wind' and 'solar', indexed by datetime:
    # datetime,wind,solar
    # 2006-01-01 00:00:00,0.788652,0.0
    # 2006-01-01 01:00:00,0.753641,0.0
    # 2006-01-01 02:00:00,0.752583,0.0
    # 2006-01-01 03:00:00,0.716325,0.0
    # 2006-01-01 04:00:00,0.654579,0.0
    # 2006-01-01 05:00:00,0.638375,0.0
    # 2006-01-01 06:00:00,0.553482,0.0
    # 2006-01-01 07:00:00,0.502253,0.00640064
    # 2006-01-01 08:00:00,0.503986,0.0363262
    # 2006-01-01 09:00:00,0.475175,0.0659112
    # 2006-01-01 10:00:00,0.397465,0.0937201
    # ...
    df_wind_solar = load_df("data/wind_solar_data.csv")

    # Define configuration parameters

    cap_mix_range = [
        0.25,
        0.5,
        0.75,
    ]  # Wind and solar capacity mix ratios, e.g., 0.25 => 25% wind, 75% solar

    thresholds = [
        0.05,
        0.075,
        0.1,
        0.15,
        0.2,
        0.25,
        0.3,
        0.35,
        0.4,
        0.45,
        0.5,
    ]  # list of thresholds for production
    period_lengths = [
        12 * t for t in range(1, 16 * 2 + 1)
    ]  # list of period lengths in hours

    split_long_periods = False  # whether to split long periods into shorter ones

    # Calculate total production
    cap_dem_ratio = 1.2  # ratio of wind and solar capacity (combined) to demand capacity, e.g., 1.5 means 50% more capacity than demand, default is 1.0
    df_total_production = get_total_production_df(
        df_wind_solar, cap_mix_range, cap_dem_ratio
    )

    no_years = get_number_of_years(df_total_production)  # number of years in the data

    # Analyze dunkelflaute periods
    results = get_dunkelflaute_results(
        df_total_production,
        thresholds,
        period_lengths,
        split_long_periods,
    )

    # Visualize results
    plot_dunkelflaute_events(
        results, df_total_production, cap_mix_range, thresholds, period_lengths
    )
    # Plot the dunkelflaute events for a given capacity mix, threshold, period length of interest
    plot_period_ts_data(results, df_total_production, 0.5, 0.35, 7 * 24)

    # Plot the solar and wind performance for a given capacity mix, threshold, period length of interest
    plot_period_solar_wind_performance(
        results, df_wind_solar, 0.75, 0.35, [7 * 24, 10 * 24, 14 * 24]
    )

    plot_dunkelflaute_contour(results, 0.5, period_lengths, thresholds, no_years)


if __name__ == "__main__":
    main()
