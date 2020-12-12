# pic-sure-hpds-nhanes
An example HPDS environment load with a subset of the NHANES data.

NOTE : This repository uses docker-compose and Docker. Please make sure
your Docker and docker-compose are up to date before trying to run anything.

This repository serves as an example load of phenotype data into HPDS and a 
Jupyter Notebook test environment for working with that data.

This environment provides an incomplete infrastructure that is good for
adapting your data into a source form that can be loaded in PIC-SURE-HPDS
and for validating your load of that data. To complete this environment
and make it production ready, you must put the HPDS instance behind a 
properly configured PIC-SURE API v2 instance.

The repository has 2 folders in it:

nhanes-load-example : This is an example load process for PIC-SURE-HPDS
from a gzipped CSV file which is a subset of the NHANES database. 

jupyter-notebooks : Some Jupyter Notebook examples that show statistics
for each of the concepts in the dataset.

To run the example you need a docker environment with docker-compose
configured. We assume you are on a Linux based environment. We strongly
recommend that you use docker-machine if you are in a non-linux
environment such as Windows or Mac. 

Start by following the instructions in nhanes-load-example/README.md

Once that completes successfully, start the stack from this folder:

docker-compose up -d

Then open your web browser while pointing at your docker-machine,
docker engine host, or localhost if you are just running it locally.
