# Setting up this repo from scratch

## Virtual Environment
rm `.python-version`
pyenv virtualenv ninety_nine_cats
pyenv local ninety_nine_cats

## Install requirements

pip install -r requirements.txt

## Migrate Database

./manage.py migrate


## Connect to ipython

./manage.py shell_plus --print-sql

### Create a super user

 ./manage.py createsuperuser


## Start local development

./manage.py runserver_plus --print-sql

Log in to admin.
http://localhost:8000/admin/
