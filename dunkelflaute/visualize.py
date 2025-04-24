from matplotlib import pyplot as plt


def plot_dunkelflaute_events(
    results, df_total, cap_mix_range, thresholds, period_lenghts
):
    no_years = len(df_total.index.year.unique())

    for cap_mix in cap_mix_range:
        plt.figure(figsize=(10, 6))
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

    # Do the same in a single plot, putting all capacity mix ratios side by side in subplots horizontally
    plt.figure(figsize=(15, 10))
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
    plt.show()


def plot_period_ts_data(results, df_total, cap_mix, threshold, period_len):
    plt.figure(figsize=(10, 6))
    for start, end in results[threshold][period_len][
        f"w{cap_mix:2.2f}_s{1-cap_mix:2.2f}"
    ]:
        plt.axvspan(start, end, color="red", alpha=0.3)
    plt.plot(
        df_total.index,
        df_total[f"w{cap_mix:2.2f}_s{1-cap_mix:2.2f}"],
        label="Total Production",
    )
    plt.title(
        f"Dunkelflaute Events for Wind: {cap_mix} Solar: {1-cap_mix}, Threshold: {threshold}, Min. Period Length: {int(period_len/24)} days"
    )
    plt.xlabel("Date")
    plt.ylabel("Production")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()
