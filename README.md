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

### Installation - Docker container

This will create a container of ~1.1Gb

+ docker image build -t <image name> .
+ docker container run -d -p <local port>:8080  --name <container name> <image name>

### Installation - local with anaconda

It is recommended that this package is run on a Conda environment. In particular,
it has been developed using python 3.7

+ conda env create -f env.yml
+ source activate IR
+ Rscript install_R_dependencies.R
+ python3 main.py

### Cloud deployment

using the Google Cloud platform:

+ Create new project (e.g. myproj-test)
+ Set Firewall rules
  + HB -> VPC Network -> Firewall rules
    + Create Firewall rule.
    + Leave all default, except the following. 
    + Targets: All instances
    + Source IP ranges: 0.0.0.0/0
    + tcp: 8080
    + Note: This should prevent bad gateway errors.
+ If using a project from Github.
  + Link the GCP to your git repo.
    + HB -> Source repositories.
    + On the top right, click Add repository.
    + Connect to external repo (naviagate through the options).
    + You may need to add an ssh key to git (not entirely sure). If so, see [this link](https://cloud.google.com/source-repositories/docs/authentication#ssh).
    + If needed, more instructions can be found [here](https://www.youtube.com/watch?v=D85bCIvPM1s).
+ Naviagte to your GCP project and start a GCS (terminal icon on top right).
  + ls (see the content of the home dir. The git repo should be there. If not, try:
  + gcloud source repos clone "REPOSITORY_NAME" "DIRECTORY_NAME"
+ Deploy!
  + In the repo dir, simply type:
    + gcloud app deploy --stop-previous-version
      + Make sure that the debug option was set to False to prevent the app from refreshing every few seconds.

### Relevant Sources

+ https://rpy2.readthedocs.io/en/version_2.8.x/introduction.html
+ http://rpy.sourceforge.net/rpy2/doc-2.1/html/introduction.html
+ https://cran.r-project.org/web/packages/Sim.DiffProc/vignettes/fitsde.html
+ http://www.turingfinance.com/random-walks-down-wall-street-stochastic-processes-in-python/
+ https://en.wikipedia.org/wiki/Vasicek_model
+ https://www.phillipsj.net/posts/deploying-dash-to-google-app-engine/
+ https://www.youtube.com/watch?v=RbejfDTHhhg
+ https://www.youtube.com/watch?v=QUYCiIkzZlA
