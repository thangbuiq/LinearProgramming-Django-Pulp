run:
	rm -rf staticfiles && python3 manage.py collectstatic --no-input -v 0 && python3 manage.py runserver
push:
	git add . && git commit -m "@thangbuiq - Commit and think it'll be alright" && git push
