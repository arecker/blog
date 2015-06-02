all:
	pip install -r requirements/production.txt
	python manage.py migrate
	echo "Y" | python manage.py bower_install
	python manage.py collectstatic --noinput
