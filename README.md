# Dunkelflaute

Dunkelflaute is a Python module designed to analyze and visualize periods of low renewable energy production, specifically focusing on wind and solar energy. This module provides tools to calculate total production based on different capacity mixes and identify fuzzy periods where production falls below specified thresholds.

## Features

- Calculate total renewable energy production from wind and solar sources.
- Identify periods of low production (dunkelflaute) based on customizable thresholds and period lengths.
- Generate visualizations to analyze the frequency and duration of dunkelflaute events.
- Contour plots to visualize the frequency of dunkelflaute events across thresholds and persistence times.

## Installation

To install the Dunkelflaute module, clone the repository and run the following command:

```bash
pip install .
```

## Usage

Here is a basic example of how to use the Dunkelflaute module:

```python
from dunkelflaute.core import get_total_production_df, find_fuzzy_periods, get_dunkelflaute_results
from dunkelflaute.utils import create_ts_from_raw

# Create a time series dataframe from raw data
df = create_ts_from_raw("data/raw", range(2006, 2013))

# Define capacity mix and thresholds
cap_mix_range = [0.25, 0.5, 0.75]  # Wind and solar capacity mix ratios
thresholds = [0.05, 0.1, 0.15]  # Capacity factor thresholds
period_lengths = [24 * t for t in range(1, 15)]  # Period lengths in hours

# Calculate total production
df_total = get_total_production_df(df, cap_mix_range)

# Get dunkelflaute results
results = get_dunkelflaute_results(df_total, thresholds, period_lengths)
```

## Visualizations

The Dunkelflaute module includes tools to visualize the results:

1. **Scatter Plot of Solar vs. Wind Performance**:
   - Visualize the relative performance of wind and solar during dunkelflaute events.

2. **Contour Plot of Dunkelflaute Frequency**:
   - Generate a contour plot showing the frequency of dunkelflaute events across thresholds and persistence times.

Example code for generating a contour plot:

```python
from dunkelflaute.visualize import plot_dunkelflaute_contour

# Generate a contour plot
plot_dunkelflaute_contour(results, cap_mix=0.5, period_lengths=period_lengths, thresholds=thresholds, no_years=7)
```

## Jupyter Notebook Guide

For a step-by-step guide on how to use the Dunkelflaute module, refer to the [Dunkelflaute Tutorial Notebook](notebooks/dunkelflaute_tutorial.ipynb). This notebook provides examples of loading data, analyzing dunkelflaute periods, and visualizing results.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.