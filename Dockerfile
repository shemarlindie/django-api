FROM python:3

WORKDIR /usr/src/app

RUN pip install pipenv

COPY . .

RUN pipenv install
RUN pipenv run python manage.py migrate

ARG DJANGO_SUPERUSER_USERNAME
ARG DJANGO_SUPERUSER_EMAIL
ARG DJANGO_SUPERUSER_PASSWORD
RUN pipenv run python manage.py createsuperuser --noinput

RUN pipenv run python manage.py loaddata issue/all
RUN pipenv run python manage.py loaddata skill/skills
RUN pipenv run python manage.py loaddata django_api/api/auth/fixtures/auth/demo_user.json

ENTRYPOINT [ "pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:80" ]

EXPOSE 80