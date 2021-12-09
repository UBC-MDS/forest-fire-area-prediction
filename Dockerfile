<<<<<<< HEAD
=======

#Date:8th Dec, 2020

#Base image
>>>>>>> dev
FROM continuumio/miniconda3

RUN apt-get update

RUN conda install docopt=0.6.* -y

RUN conda install pandas=1.3.* -y

RUN conda install altair=4.1.* -y

RUN conda install pytest=6.2.* -y

RUN conda install -y -c conda-forge altair_saver

RUN conda install scikit-learn=1.0.* -y

RUN conda install jinja2=3.0.* -y

RUN conda install statsmodels=0.13.* -y

#Install R and R packages
RUN apt-get install r-base -y
<<<<<<< HEAD

RUN Rscript -e 'install.packages("knitr")'
RUN Rscript -e 'install.packages("rmarkdown")'
=======
RUN Rscript -e 'install.packages("knitr")'
>>>>>>> dev

RUN conda install -y -c conda-forge ipykernel=6.5.*

RUN conda install -y -c conda-forge graphviz=2.49.*

RUN conda install -y -c conda-forge dataframe_image=0.1.*

<<<<<<< HEAD


WORKDIR "${HOME}" 


=======
RUN apt-get install gcc python3-dev chromium-driver -y

#RUN pip install altair-data-server==0.4.*

WORKDIR "${HOME}"
>>>>>>> dev
