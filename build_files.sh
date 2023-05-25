pip install --root-user-action=ignore -r requirements.txt
rm -rf /vercel/path0/staticfiles
python3.9 manage.py collectstatic --no-input