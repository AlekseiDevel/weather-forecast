import os
import time
import requests
import logging
from database import init_db, SessionLocal, RequestLog, WeatherData
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    filename='error_log.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def fetch_and_save():
    api_key = os.getenv('API_KEY')
    city = os.getenv('CITY', 'Moscow')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}&units=metric"

    session = SessionLocal()
    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 401:
            logging.error("401: Неверный API ключ")
            return

        response.raise_for_status()
        data = response.json()

        new_request = RequestLog(city=city, status_code=response.status_code)
        session.add(new_request)
        session.flush()

        weather_info = WeatherData(
            request_id=new_request.id,
            temperature=data['main']['temp'],
            humidity=data['main']['humidity'],
            description=data['weather'][0]['description']
        )
        session.add(weather_info)
        session.commit()
        print(f"Данные сохранены для {city}: {data['main']['temp']}°C")

    except Exception as e:
        logging.error(f"Ошибка: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    print("Ожидание запуска БД...")
    time.sleep(5)
    init_db()
    interval = int(os.getenv('INTERVAL_MINUTES', 10)) * 60
    while True:
        fetch_and_save()
        time.sleep(interval)