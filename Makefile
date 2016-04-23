.DEFAULT_GOAL := test

requirements:
	pip install -r requirements.txt

test:
	pip install -r requirements.txt
	pip install -r test_requirements.txt
	python manage.py test --settings=tests.settings

initialize:
	python manage.py migrate
	python manage.py syncdb
	python manage.py loaddata fixtures/sites.json

run:
	python manage.py runserver
