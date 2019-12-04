#!/bin/bash
sudo mkdir /home/R_packages
chmod a+rwx -R /home/R_packages

python3 -m venv .venvs/ir_env
source .venvs/ir_env/bin/activate

sudo apt-get update -y
sudo apt-get install -qy python3-pip
sudo apt-get install -qy  r-base
cd IR_forecaster
pip3 install -r requirements.txt
sudo Rscript -e 'install.packages("Sim.DiffProc", lib="/home/R_packages", repos="http://cran.us.r-project.org")'
python3 main.py
