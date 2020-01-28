# Tourist

## Usage

For email confirmation to work u should determine env var 'MAIL_USERNAME' and 'MAIL_PASSWORD' for mail service(config location ./celery_service/config.py), dont forget to start celery service

Run app in debug mode, run in console
> cd tourist

> make debug

## Celery usage

Start redis
> sudo service redis-server start

Run in console from tourist/celery_service with active venv
> celery worker -A app.app --loglevel=debug

## Migrations 

from tourist/api run:

> python manage.py db init

> python manage.py db migrate

> python manage.py db upgrade

## Cron usage

> crontab -e
Insert the following code into opened file. Dont forget
to change PATH variable

#set PATH variable to your path to "tourist" folder 
#e.g my full path is "/home/rukadelica/tourist"
#there fore variable is set to "tourist"
PATH = tourist
59 */23 * * * $PATH/cron_task/sh-script tourist

save file and enjoy
