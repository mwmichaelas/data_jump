FROM python:3.10.0a5-buster

RUN apt-get update
RUN pip install --no-cache-dir pipenv

WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock bootstrap.sh ./
COPY as_services ./as_services

RUN pipenv install

EXPOSE 8000
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]