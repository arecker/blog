all:
	pip install -r requirements/production.txt
	python manage.py migrate
	echo "Y" | python manage.py bower_install
	python manage.py collectstatic --noinput

test:
	python manage.py migrate
	echo "Y" | python manage.py bower_install
	npm install
	grunt
	python manage.py test
