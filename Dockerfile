FROM python:3.7.10-slim-buster


ENV NEO_SERVICE=/home/neos
# set work directory


RUN mkdir -p $NEO_SERVICE

# where the code lives
WORKDIR $NEO_SERVICE

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install dependencies
RUN pip install --upgrade pip
# copy project
#COPY . $NEO_SERVICE
COPY requirements.txt $NEO_SERVICE
RUN pip install -r requirements.txt
CMD ["/bin/bash"]