#Specify OS.
FROM ubuntu:18.04

#Set timezone env variable, so that r-base installation does not ask the user
#to specify a timezone when deploying the app.
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#Make a directory for R-Packages and assign permissions.
RUN mkdir /home/R_packages \
    && chmod a+rwx -R /home/R_packages

#Copy files to an "app/" directory.
COPY . /app

#Switch directory to the newly created app/
WORKDIR /app

#Make sure apt-get is up-to-date and install series of dependencies.
RUN apt-get update -y \
    && apt-get install -qy python3 python3-pip r-base \
    && pip3 install -r requirements.txt \
    && Rscript -e "install.packages('Sim.DiffProc', lib='/home/R_packages', \
                                    repos='http://cran.wustl.edu/')"

#open necessary ports to avoid gateway errors. Ensure that main.py server
#matches the same port app.run_server(host='0.0.0.0', port=8080, debug=True).
EXPOSE 8080

#Execute the main.py script.
CMD ["python3", "main.py"]
