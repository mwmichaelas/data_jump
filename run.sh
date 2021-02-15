#!/bin/sh
export FLASK_APP=./data_jump/app.py
source $(pipenv --venv)/bin/activate
flask run -h 127.0.0.1 -p 8000