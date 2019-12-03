#!/bin/bash
python3 -m venv .venvs/testing
source .venvs/testing/bin/activate
apt-get update -y
apt-get install -qy python3-pip
apt-get install -qy  r-base
cd $workdir
pip3 install -r requirements.txt
Rscript install_R_dependencies.R
python3 main.py
