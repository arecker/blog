manage = python manage.py
install = pip install

all:
	${install} -r requirements/prod.txt
	${manage} migrate
	${manage} collectstatic --noinput
migrate:
	${manage} makemigrations
	${manage} migrate
run:
	${manage} runserver
