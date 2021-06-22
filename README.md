# Foodgram
### Social network for culinary authors
## Author: @devgomax
### Techs: Postgresql, Django + Gunicorn, Nginx
## Website - www.devgomax.gq
### Server deployment instructions:
- create ```.env``` file to the project's root directory with the next lines:
     ```
        DB_ENGINE=django.db.backends.postgresql
        DB_NAME={database name}
        POSTGRES_USER=postgres
        POSTGRES_PASSWORD={create password for db user}
        DB_HOST=db
        DB_PORT=5432
        SECRET_KEY={type the secret key for django settings.py}
     ```
- create directory ```/static/``` with static files for django
- create directory ```/media/``` with media files for django
- change the next line in file ```/nginx/default.conf```:
    ```server_name {your server's IP} {domain} www.{domain}```
- execute next commands in terminal:
    ```
        docker-compose up -d --build
        docker-compose exec web python manage.py makemigrations users
        docker-compose exec web python manage.py makemigrations recipes
        docker-compose exec web python manage.py migrate --noinput
        docker-compose exec web python manage.py createsuperuser
        docker-compose exec web python manage.py collectstatic --no-input
        docker-compose exec web python manage.py loaddata dump.json
    ```
### That's it! Now your website is available at ```http://{your domain}/``` and admin panel at ```/admin/```
- ```docker-compose up -d``` to start project
- ```docker-compose down``` to stop all the working containers