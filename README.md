# Weather Monitor Script

Сервис для периодического сбора данных о погоде через OpenWeatherMap API и сохранения в PostgreSQL.


Функционал

+ Периодический сбор: Запрашивает данные из OpenWeatherMap API каждые N минут.
+ Хранение данных: Использует PostgreSQL с двумя связанными таблицами (requests_log и weather_data).
+ Логирование: Ошибки сети, таймауты и некорректные ответы API записываются в файл error_log.log.
+ Контейнеризация: Полностью разворачивается одной командой через Docker Compose.


Архитектура БД
+ requests_log: Хранит метаданные (время запроса, город, HTTP-статус).
+ weather_data: Хранит фактические показатели погоды. Связана с первой таблицей через request_id (Foreign Key).


Как развернуть

1. Подготовка окружения  

Клонируйте репозиторий и создайте файл .env в корневой папке. Используйте следующий пример:

API_KEY=ваш_ключ_от_openweathermap  
CITY=Moscow  
INTERVAL_MINUTES=N  
DATABASE_URL=postgresql://user:password@db:5432/weather_db


2. Запуск

Выполните команду для сборки и запуска контейнеров:

docker-compose up --build

Сервис автоматически создаст необходимые таблицы при первом запуске.


3. Работа с данными

Выполните команду для подключения к базе данных

docker-compose exec db psql -U user -d weather_db


Для получения полной истории запросов с данными о погоде выполните следующий SQL-запрос:

SELECT  
      r.timestamp AT TIME ZONE 'UTC' as "Time",  
      r.city as "City",  
      w.temperature as "Temp",  
      w.description as "Weather"  
FROM  
      requests_log r  
JOIN  
      weather_data w ON r.id = w.request_id  
ORDER BY  
      r.timestamp DESC;  


4. Просмотр логов ошибок

Если сервис работает некорректно, проверьте файл логов:

docker-compose exec app cat error_log.log


