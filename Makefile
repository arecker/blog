manage = python manage.py
install = pip install

all:
	${install} -r requirements/prod.txt
	${manage} migrate
	${manage} collectstatic --noinput
run:
	${manage} runserver
