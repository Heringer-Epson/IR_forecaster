#References:
#https://www.wintellect.com/containerize-python-app-5-minutes/
#https://blog.realkinetic.com/building-minimal-docker-containers-for-python-applications-37d0272c52f3
#https://www.youtube.com/watch?v=WAPXaDpkytw
#https://cloud.google.com/appengine/docs/flexible/custom-runtimes/build#docker

#Specify OS.
FROM ubuntu:latest

#Make sure apt-get is up-to-date.
RUN apt-get update -y

#Set timezone env variable, so that r-base installation does not ask the user
#to specify a timezone when deploying the app.
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#Install r-base so that Rscripts can be run.
RUN apt-get install -qy  r-base

#Install python3.
RUN apt-get install -qy python3

#Install/update pip.
RUN apt-get install -qy python3-pip

#Copy files to an "app/" directory.
#ADD . /app
#COPY . /app

#Switch directory to the newly created app/
WORKDIR /app

#Install requirements.
RUN pip3 install -r requirements.txt

#open necessary ports to avoid gateway errors. Ensure that main.py server
#uses app.run_server(host='0.0.0.0', port=8080, debug=True).
EXPOSE 8050
EXPOSE 8080

#Execute install_SimDiff.R script to install Sim.DiffProc package.
RUN Rscript -e "install.packages('Sim.DiffProc', lib='/usr/R_packages', repos='http://cran.us.r-project.org')"
#CMD ["python3", "install_R_dependencies.py"]

#Execute the main.py script.
CMD ["python3", "main.py"]
