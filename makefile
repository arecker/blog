all:
	python manage.py migrate
	echo "Y" | python manage.py bower_install
	python manage.py collectstatic --noinput

install:
	pip install -r requirements.txt
	npm install

test:
	python manage.py test
	grunt
