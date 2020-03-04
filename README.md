# Indeed Parser

POSTGRESQL
-----------------------------------

Установака postgresql версии 12:
```
echo 'deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main' | sudo tee /etc/apt/sources.list.d/pgdg.list
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

Создание пользователя и БД:
```
sudo -u postgres
psql
CREATE ROLE indeed WITH LOGIN PASSWORD 'indeed';
CREATE DATABASE indeed WITH OWNER indeed;
```

Настройка окружения
-----------------------------------
```bash
pip install -r requirements.txt
```

Применение миграций
-----------------------------------
```bash
python manage.py migrate
```

Сборка статики
-----------------------------------
```bash
python manage.py collectstatic --noinput --clear
```