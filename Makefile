
default: requirements.txt
	pip install -r requirements.txt

requirements.txt:
	pip-compile requirements.in

deploy:
	git push heroku master
	heroku run python manage.py migrate