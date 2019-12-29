# Heroku Set-Up

Edit the values of variables in the **`set_env_vars`** file and save the changes.

```bash
python manage.py collectstatic

git add staticfiles/
git commit -m "performed collectstatic"

heroku login
heroku create em-entry-management-prod
source set_env_vars_heroku
git push heroku heroku-production:master

heroku run python3 manage.py em_setup
heroku ps:scale web=1
```
