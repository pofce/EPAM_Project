#!/bin/bash

if [ ! -d venv ]; then
	echo "Setting up the virtual environment."
	sleep 1
	python3 -m venv venv

	echo "Activating virtual environment."
	sleep 1
	source venv/bin/activate

	echo "Installing dependencies."
	sleep 1
	pip install wheel
	pip install -r requirements.txt
else
	echo "Activating virtual environment."
	sleep 1
	source venv/bin/activate
fi

export FLASK_APP=wsgi.py
if [ ! -f department_app.db ]; then
	echo "Creating SQLite database"
	sleep 1
	flask db upgrade

	echo "Populating database with test data"
	sleep 1
	python3 population.py
fi

echo "Running... "
sleep 1
python3 -m flask run