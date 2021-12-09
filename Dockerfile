
#Date:8th Dec, 2020

#Base image
FROM continuumio/miniconda3

RUN apt-get update

RUN conda install docopt=0.6.* -y

RUN conda install pandas=1.3.* -y

RUN conda install altair=4.1.* -y

RUN conda install pytest=6.2.* -y

RUN pip install altair_saver

RUN conda install scikit-learn=1.0.* -y

RUN conda install jinja2=3.0.* -y

RUN conda install statsmodels=0.13.* -y

#Install R and R packages
RUN apt-get install r-base -y
RUN Rscript -e 'install.packages("knitr")'

RUN conda install -y -c conda-forge ipykernel=6.5.*

RUN conda install -y -c conda-forge graphviz=2.49.*

RUN conda install -y -c conda-forge dataframe_image=0.1.*

WORKDIR "${HOME}"