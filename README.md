# COVIDews
Code and data associated with the paper: Using COVID-19 data to investigate the use of early warning signs to identify epidemic peaks and areas of concern

Primary authors (contributed equally): Joshua Looker.
Other authors (contributed equally): Louise Dyson, Kat Rock

## Running the data-driven analysis
The `data_processing.ipynb` notebook contains pre-processing code to process the census and UKHSA-case data for usage in the data-driven EWS analysis.

The `results_LTLA.ipynb` and `results_NHS.ipynb` notebooks contain most of the final results used in the paper (with some supplementary results also included in the `results_LTLA_supplementary.ipynb` notebook). All results can be found in the `Figures` and `Results` directories.

## Simulation/Theoretical analysis

Code to run the simulations and produce the plots can all be found in the `simulations_aggregation_theory.ipynb` notebook (node that some of the code is run in parallel and so requires a large amount of RAM/compute cores to avoid kernel failure).

## Data sources
The data sources used in `data_processing.ipynb` and shape files used for plotting the spatio-temporal analysis are not included (due to size constraints) in this repository, but can be found at links in the accompanying paper (or on the ONS and UKHSA websites).