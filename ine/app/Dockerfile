###########
# BUILDER #
###########

# pull official base image
FROM python:3.7.5-slim-buster as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Download latest listing of available packages:
RUN apt-get -y update
# Upgrade already installed packages:
RUN apt-get -y upgrade
# Install a new package:

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev gcc

# lint
RUN pip install --upgrade pip
ADD . /usr/src/app/

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.7.5-slim-buster

# Download latest listing of available packages:
RUN apt-get -y update
# Upgrade already installed packages:
RUN apt-get -y upgrade
# Install a new package:
RUN apt-get update && apt-get install -y --no-install-recommends netcat

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
#RUN addgroup -S app && adduser -S app -G app
#RUN groupadd -r app && useradd -r -g app app 

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy entrypoint.sh
COPY ./entrypoint.sh $APP_HOME

# copy project
COPY . $APP_HOME
