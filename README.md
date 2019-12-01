# Intrabank Rate Forecaster

This package performs two main functions:

1) The analysis of intrabank (IR) time series.
  + Transforms the 'Raw' series using rate differences or the log of rate ratios.
    + The time period over which the transformation is perfomed is left as a free parameter (1 or 25 days).
  + Tools to plot the IR series and transformed series.
  + Tools to plot and fit the distribution of (transformed) rates.
  + For the term structure (IR averaged over months or years).
  + For the standard deviation of the IR according to the choice of period.
2) The simulation of future IR and term structure.
  + A financial model (Brownian or Vasicek) is used to predict the evolution of the IRs.
  + Random numbers are drawn from a normal distribution or from the distribution that best fits the IRs.
    + The correlation between tenors is taken into account when drawing random numbers.
  + The evolution of the term structure is predicted via a Monte Carlo experiment.

### Visualization

This webapp is built using [Plotly Dash](https://plot.ly/dash/) package. The
structure is tab based, providing a friendly interface for the user to
progress through the data analysis and predictions.

The webapp allows for a highly interactive and customizable experience. 

### Performance

By default, the calculations use principal component analysis (PCA) to
reduce the dimensionality of the data.

An R wrapper is used to call the 'fitsde' routine from the 'Sim.DiffProc' package.

The webapp is currently deployed on the Google Cloud Platform.

### Data

The rates used here are from the London Interbank Offered Rate (LIBOR).

Source: The Federal Bank of Saint-Louis [FRED](https://fred.stlouisfed.org/).

### Installation

It is recommended that this package is run on a Conda environment. In particular,
it has been developed using python 3.7

+ conda env create -f env.yml
+ source activate IR
+ Rscript install_R_dependencies.R
+ python3 main.py

### Relevant Sources

+ https://rpy2.readthedocs.io/en/version_2.8.x/introduction.html
+ http://rpy.sourceforge.net/rpy2/doc-2.1/html/introduction.html
+ https://cran.r-project.org/web/packages/Sim.DiffProc/vignettes/fitsde.html
+ http://www.turingfinance.com/random-walks-down-wall-street-stochastic-processes-in-python/
+ https://en.wikipedia.org/wiki/Vasicek_model
