FROM continuumio/miniconda3

RUN apt-get update
RUN conda install docopt=0.6.* -y
RUN conda install pandas=1.3.* -y
RUN conda install altair=4.1.* -y
RUN pip install altair_saver
RUN conda install scikit-learn=1.0.* -y
RUN conda install jinja2=3.0.* -y
RUN conda install statsmodels=0.13.* -y

RUN apt-get install r-base -y

RUN Rscript -e 'install.packages("knitr")'

RUN pip install graphviz
RUN pip install dataframe_image
RUN pip install ipykernel


#RUN Rscript -e 'install.packages(c("tidyverse","caret","ggthemes"))'


