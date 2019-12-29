# Heroku Set-Up

```bash
python manage.py collectstatic

heroku login
heroku create heroku-django-example-prod
git push heroku master

heroku run python3 manage.py em_setup
heroku ps:scale web=1
```

