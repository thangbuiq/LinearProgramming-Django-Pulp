run:
	rm -rf staticfiles && python3 manage.py collectstatic --no-input && python3 manage.py runserver
