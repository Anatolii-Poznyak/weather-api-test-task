# 🌇 Weather-api-test-task
 API for daily weather tracking. This project is designed to fetch daily weather information for Kyiv for today and the next 5 days from [pogoda.meta.ua](https://pogoda.meta.ua/)

## 🖥️ Technologies 
![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/-Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-FF8000?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/-Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/-Celery-376F9F?style=for-the-badge&logo=celery&logoColor=white)
![Django Celery Beat](https://img.shields.io/badge/-Django%20Celery%20Beat-8AC75A?style=for-the-badge&logo=celery&logoColor=white)
![Flower](https://img.shields.io/badge/-Flower-purple?style=for-the-badge&logoColor=white)


## 📝 Requirements

- Python 3.7+
- Django 4.2.1+
- PostgreSQL
- Docker

## 🛠 Before installation
1. Clone the project repository

```bash
git clone https://github.com/Anatolii-Poznyak/weather-api-test-task.git
cd weather-api-test-task
```
2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Create .env file based on .env.sample file and set variables.

```bash
cp .env.sample .env
```

- If you want to use docker - set POSTGRES_HOST=db 

## 🐳 Run with DOCKER
- DOCKER should be installed

```shell
  docker-compose up
```
- server will run on 127.0.0.1:8000
- Create superuser from terminal to be able to login (enter the container)

```shell
docker ps
docker exec -it <your container name> /bin/bash
python manage.py createsuperuser
```

## 🖼 Demo pictures

<details>
  <summary>Admin page schedule</summary>

  ![login](demo/admin_schedule.png)
</details>
<details>
  <summary>Admin page weather</summary>

  ![employees](demo/admin_weather.png)
</details>
<details>
  <summary>Flower</summary>

  ![create](demo/flower.png)
</details>
<details>
  <summary>Status started</summary>

  ![update](demo/status_started.png)
</details>
<details>
  <summary>Pending status</summary>

  ![delete](demo/status_pending.png)
</details>
<details>
  <summary>Update</summary>

  ![transfer](demo/weather_update.png)
</details>
<details>
  <summary>Weather list</summary>

  ![logout](demo/weather_list.png)
</details>
<details>
  <summary>Update start</summary>

  ![Fixture](demo/weather_update_start.png)
</details>

## 📚 Additional info
- Schedule for day-basis updating information about weather in Kyiv will be started automatically after `docker-compose up` command `python manage.py task_command`
- You can change daily-basis time for updating information also by argument after command (exmpl: `python manage.py task_command 17` -> will change time from 9:00 to 17:00). Also you can change time from endpoint