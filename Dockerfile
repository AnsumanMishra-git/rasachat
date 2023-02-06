FROM rasa/rasa:2.7.0
WORKDIR  '/app'
COPY . /app
USER root

RUN  rasa train 

VOLUME /app/models


CMD [ "run","-m","/app/models","--enable-api","--cors","*","--debug" ,"--endpoints", "endpoints.yml", "--log-file", "out.log", "--debug"]

EXPOSE 5005

# FROM python:3.7.16 AS BASE

# RUN apt-get update \
#     && apt-get --assume-yes --no-install-recommends install \
#     build-essential \
#     curl \
#     git \
#     jq \
#     libgomp1 \
#     vim

# WORKDIR /app

# # upgrade pip version
# RUN pip install --no-cache-dir --upgrade pip

# RUN pip install rasa==2.8.14

# ADD config.yml config.yml
# ADD domain.yml domain.yml
# ADD credentials.yml credentials.yml
# ADD endpoints.yml endpoints.yml

# EXPOSE 8000
# EXPOSE 5055
