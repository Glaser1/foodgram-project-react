# Foodgram 
## Описание

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Шаблон наполнения env-файла:
``` DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql ```

``` DB_NAME=postgres # имя базы данных ```

``` POSTGRES_USER=postgres # логин для подключения к базе данных ```

``` POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой) ```

``` DB_HOST=db # название сервиса (контейнера) ```

``` DB_PORT=5432 # порт для подключения к БД ```
``` SECRET_KEY='' # секретный ключ Django ```
``` DEBUG=True/False # Включить/отключить режим отладки ```

## Установка:
* Клонируйте репозиторий себе на компьютер;
* Перейдите в папку infra с помощью команды cd infra;
* Установите docker и docker-compose (для Linux/MacOS):
  ``` sudo apt install curl ```
  
  ``` curl -fsSL https://get.docker.com -o get-docker.sh ```

  ``` sh get-docker.sh ```
  
  ``` sudo apt remove docker docker-engine docker.io containerd runc ```
  
  ``` sudo apt update  ```
  
  ``` sudo apt install \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg-agent \
        software-properties-common -y ```
        
   ``` curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - ```
   
   ``` sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" ```
   ``` sudo apt update  ```
   
   ``` sudo apt install docker-ce docker-compose -y ```

* Запустите приложения в контейнерах с помощью команды docker-compose up
* Выполните миграцию в контейнерах: 

  ``` docker-compose exec-web python manage.py makemigrations ```
  
  ``` docker-compose exec-web python manage.py migrate ```


