from matplotlib import pyplot as plt
import os
import pandas as pd


def create_new_figure():
    """
    Create a new figure with the specified size and DPI.
    """
    height = 13.8  # cm, for ppt
    width = 31.2  # cm, for ppt

    fig = plt.figure(figsize=(width / 2.54, height / 2.54), dpi=300)
    plt.rcParams["font.family"] = "Linux Biolinum"
    plt.rcParams["font.size"] = 10

    return fig


def save_figure(fig, filename):
    """
    Save the figure to a file with the specified filename.
    The file is saved in the 'plots' directory.
    """
    plot_dir = "plots"
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    filename = os.path.join(plot_dir, filename)
    fig.savefig(
        filename,
        bbox_inches="tight",
        pad_inches=0.1,
        transparent=True,
    )
    plt.close(fig)


def plot_dunkelflaute_events(
    results, df_total, cap_mix_range, thresholds, period_lenghts
):
    """
    Plot the dunkelflaute events for different capacity mixes and thresholds.
    The plot shows the number of dunkelflaute events for each capacity mix and threshold
    for different period lengths.
    The plots are saved as a SVG file.
    """
    no_years = len(df_total.index.year.unique())

    for cap_mix in cap_mix_range:
        fig = create_new_figure()
        for threshold in thresholds:
            dunkelflaute_counts = []
            for period_len in period_lenghts:
                dunkelflaute_counts.append(
                    len(
                        results[threshold][period_len][
                            f"w{cap_mix:2.2f}_s{1-cap_mix:2.2f}"
                        ]
                    )
                    / no_years
                )

            # Plot x-axis in days
            period_lenghts_days = [p / 24 for p in period_lenghts]
            plt.plot(
                period_lenghts_days,
                dunkelflaute_counts,
                label=f"Threshold: {threshold}",
                marker="o",
                markersize=3,
            )
        plt.title(f"Dunkelflaute Events for Wind: {cap_mix} Solar: {1-cap_mix}")
        plt.xlabel("Minimum duration (days)")
        plt.xticks(period_lenghts_days)
        plt.xlim(period_lenghts_days[0], period_lenghts_days[-1])
        plt.ylabel("Number of observed Dunkelflaute events (# of periods per year)")
        plt.legend()
        plt.grid()
        save_figure(fig, f"dunkelflaute_events_{cap_mix}.svg")

    # Do the same in a single plot, putting all capacity mix ratios side by side in subplots horizontally
    fig = create_new_figure()
    for i, cap_mix in enumerate(cap_mix_range):
        y_max = 0
        plt.subplot(1, len(cap_mix_range), i + 1)
        for threshold in thresholds:
            dunkelflaute_counts = []
            for period_len in period_lenghts:
                dunkelflaute_counts.append(
                    len(
                        results[threshold][period_len][
                            f"w{cap_mix:2.2f}_s{1-cap_mix:2.2f}"
                        ]
                    )
                    / no_years
                )

            # Plot x-axis in days
            period_lenghts_days = [p / 24 for p in period_lenghts]
            plt.plot(
                period_lenghts_days,
                dunkelflaute_counts,
                label=f"Threshold: {threshold}",
                marker="o",
                markersize=3,
            )
            y_max = max(y_max, max(dunkelflaute_counts))

        plt.title(f"Wind: {cap_mix} Solar: {1-cap_mix}")
        plt.xlabel("Minimum duration (days)")
        plt.xticks(period_lenghts_days)
        plt.xlim(period_lenghts_days[0], period_lenghts_days[-1])
        plt.ylabel("Number of observed Dunkelflaute events (# of periods per year)")
        plt.legend()
        plt.grid()

    for i in range(len(cap_mix_range)):
        plt.subplot(1, len(cap_mix_range), i + 1)
        plt.ylim(0, y_max * 1.1)

    plt.tight_layout()
    save_figure(fig, "dunkelflaute_events.svg")


def plot_period_ts_data(results, df_total, cap_mix, threshold, period_len):
    """
    Plot the time series data for a given capacity mix, threshold, and period length.
    The plot shows the total production and the dunkelflaute events
    (periods below the threshold) highlighted in red.
    Total plot and individual plots for each period are saved.
    The plots are saved as a SVG file.
    """
    fig = create_new_figure()
    for start, end in results[threshold][period_len][
        f"w{cap_mix:2.2f}_s{1-cap_mix:2.2f}"
    ]:
        plt.axvspan(start, end, color="red", alpha=0.3)
    plt.plot(
        df_total.index,
        df_total[f"w{cap_mix:2.2f}_s{1-cap_mix:2.2f}"],
        label="Total Production",
    )
    plt.axhline(threshold, color="black", linestyle="--", label="Threshold")
    plt.title(
        f"Dunkelflaute Events for Wind: {cap_mix} Solar: {1-cap_mix}, Threshold: {threshold}, Min. Period Length: {int(period_len/24)} days"
    )
    plt.xlabel("Date")
    plt.ylabel("Production")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    save_figure(fig, "period_ts_data.svg")

    # Save figure for each period, plot only the period + and - 3 days
    # around the start and end of the period
    for i, (start, end) in enumerate(
        results[threshold][period_len][f"w{cap_mix:2.2f}_s{1-cap_mix:2.2f}"]
    ):
        fig = create_new_figure()
        plt.axvspan(start, end, color="red", alpha=0.3)
        plt.plot(
            df_total.index,
            df_total[f"w{cap_mix:2.2f}_s{1-cap_mix:2.2f}"],
            label="Total Production",
        )
        plt.axhline(threshold, color="black", linestyle="--", label="Threshold")

        plt.text(
            start + (end - start) / 2,
            threshold + 0.01,
            f"{int((end - start).total_seconds() / 3600)} hours ({(end - start).total_seconds() / 3600 / 24:2.1f} days)",
            ha="center",
            va="bottom",
        )
        plt.xlim(start - pd.Timedelta(days=3), end + pd.Timedelta(days=3))

        plt.title(
            f"Dunkelflaute Event {i+1} for Wind: {cap_mix} Solar: {1-cap_mix}, Threshold: {threshold}, Min. Period Length: {int(period_len/24)} days"
        )
        plt.xlabel("Date")
        plt.ylabel("Production")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        save_figure(fig, f"period_ts_data_{i+1}.svg")


def plot_period_solar_wind_performance(
    results, df_wind_solar, cap_mix, threshold, period_len
):
    """
    Plot the performance of wind and solar production during dunkelflaute events
    for a given capacity mix, threshold, and period length.
    The performance is defined as the mean production during the dunkelflaute event
    divided by the mean production for the total time horizon.
    The plot shows the performance of wind and solar production
    during dunkelflaute events for different period lengths.
    The plot is saved as a SVG file.
    """

    if not isinstance(period_len, list):
        period_len = [period_len]

    fig = create_new_figure()
    # get the mean production for the total time horizon
    mean_wind_total = df_wind_solar["wind"].mean()
    mean_solar_total = df_wind_solar["solar"].mean()

    colors = ["red", "blue", "green", "orange", "purple"]

    for i, plen in enumerate(period_len):
        lbl = f"Period length: {int(plen/24)} days"
        for start, end in results[threshold][plen][
            f"w{cap_mix:2.2f}_s{1-cap_mix:2.2f}"
        ]:
            # get the mean production for the period
            mean_wind = df_wind_solar["wind"].loc[start:end].mean()
            mean_solar = df_wind_solar["solar"].loc[start:end].mean()

            plt.scatter(
                mean_solar / mean_solar_total,
                mean_wind / mean_wind_total,
                alpha=0.3,
                color=colors[i],
                label=lbl,
            )
            lbl = None

    plt.axhline(
        1, color="black", linestyle="--", label="Wind/solar reference performance"
    )
    plt.axvline(1, color="black", linestyle="--")

    plt.title(
        f"Dunkelflaute Events for Wind: {cap_mix} Solar: {1-cap_mix}, Threshold: {threshold}"
    )
    plt.xlabel("Solar performance relative to reference performance (mean)")
    plt.ylabel("Wind performance relative to reference performance (mean)")
    plt.legend()
    plt.grid()
    plt.tight_layout()

    save_figure(
        fig,
        f"period_solar_wind_performance_{cap_mix}_{threshold}_{period_len}.svg",
    )


def plot_dunkelflaute_contour(results, cap_mix, period_lengths, thresholds, no_years):
    """
    Create a contour plot showing the frequency of dunkelflaute events.

    Parameters:
    - results: Dictionary containing dunkelflaute results.
    - cap_mix: Capacity mix ratio (e.g., 0.5 for 50% wind, 50% solar).
    - period_lengths: List of period lengths (in hours).
    - thresholds: List of cap. factor thresholds.
    - no_years: Number of years in the dataset.
    """

    x = np.array([p / 24 for p in period_lengths])  # Convert period lengths to days
    y = np.array(thresholds)
    z = np.zeros((len(y), len(x)))

    # Populate the z matrix with the frequency of dunkelflaute events
    for i, threshold in enumerate(thresholds):
        for j, period_len in enumerate(period_lengths):
            z[i, j] = (
                len(
                    results[threshold][period_len][f"w{cap_mix:2.2f}_s{1-cap_mix:2.2f}"]
                )
                / no_years
            )

    if False:  # Set to True to debug
        print(f"Min: {z.min()}, Max: {z.max()}")
        print(f"z-matrix saved to z_matrix.csv")
        np.savetxt("z_matrix.csv", z, delimiter=",")

    # Set levels for contour plot
    min_non_zero = np.min(z[z > 0])
    min_non_zero_lvl = np.floor(min_non_zero * 100) / 100
    max_lvl = np.ceil(z.max() * 100) / 100
    levels = [
        min_non_zero_lvl,
        0.2,
        0.5,
        1,
        2,
        5,
        10,
        20,
        50,
        100,
        max_lvl,
    ]
    levels = [l for l in levels if l <= max_lvl and l >= min_non_zero_lvl]

    cmap = plt.get_cmap("RdYlBu")
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

    # Create the contour plot
    fig = create_new_figure()
    ax = fig.add_subplot(111)
    contour = ax.contourf(x, y, z, levels=levels, cmap=cmap, norm=norm)

    # Add colorbar
    cbar = plt.colorbar(contour)
    cbar.set_label("Events / year")
    cbar.set_ticks(levels)
    cbar.set_ticklabels([str(l) for l in levels])

    # Add labels and title
    ax.set_title(f"Dunkelflaute events for Wind: {cap_mix} Solar: {1-cap_mix}")
    ax.set_xlabel("> Period length (Days)")
    ax.set_ylabel("Capacity factor threshold")
    ax.grid()

    # Save the figure
    plt.tight_layout()
    save_figure(fig, f"dunkelflaute_contour_{cap_mix}.svg")
