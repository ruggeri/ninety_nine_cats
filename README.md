

To start the project:

```bash
mkdir ninety_nine_cats
cd ninety_cats
pyenv virtualenv ninety_nine_cats
pyenv local ninety_nine_cats
pip install --upgrade pip
pip install Django
pip freeze > requirements.txt
django-admin startproject ninety_nine_cats .
```
