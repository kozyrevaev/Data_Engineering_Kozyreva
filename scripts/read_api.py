import os

import pandas as pd
import requests

API_URL = "https://archive-api.open-meteo.com/v1/archive"

# города, где находятся отели из датасета Hotel booking demand
CITIES = {
    "Lisbon": (38.72, -9.14),  # City Hotel
    "Faro": (37.02, -7.93),    # Resort Hotel (Алгарве)
}

# период совпадает с датасетом бронирований
START_DATE = "2015-07-01"
END_DATE = "2017-08-31"

DAILY_VARIABLES = [
    "weather_code",
    "temperature_2m_max",
    "temperature_2m_min",
    "temperature_2m_mean",
    "apparent_temperature_mean",
    "precipitation_sum",
    "rain_sum",
    "precipitation_hours",
    "sunshine_duration",
    "daylight_duration",
    "wind_speed_10m_max",
    "wind_gusts_10m_max",
    "wind_direction_10m_dominant",
    "shortwave_radiation_sum",
]

OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "weather_portugal.parquet")


def fetch_city(city, lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "daily": ",".join(DAILY_VARIABLES),
        "timezone": "Europe/Lisbon",
    }
    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()  # если сервер вернул ошибку — остановиться

    df = pd.DataFrame(response.json()["daily"])
    df.insert(0, "city", city)
    return df


def build_dataset():
    frames = []
    for city, (lat, lon) in CITIES.items():
        print(f"Запрашиваю погоду: {city}")
        frames.append(fetch_city(city, lat, lon))
    return pd.concat(frames, ignore_index=True)


def convert_types(df):
    df = df.rename(columns={"time": "date"})
    df["date"] = pd.to_datetime(df["date"])
    df["city"] = df["city"].astype("category")
    df["weather_code"] = df["weather_code"].astype("Int16")

    # API отдаёт длительность в секундах — переводим в часы
    df["sunshine_hours"] = (df.pop("sunshine_duration") / 3600).round(1)
    df["daylight_hours"] = (df.pop("daylight_duration") / 3600).round(1)

    float_cols = df.select_dtypes("float64").columns
    df[float_cols] = df[float_cols].astype("float32")
    return df


if __name__ == "__main__":
    df = build_dataset()
    df = convert_types(df)

    with pd.option_context(
        "display.max_columns", None,
        "display.width", 400,
        "display.float_format", "{:.1f}".format,
    ):
        print(df.head(20))
    print(f"\nРазмер: {df.shape[0]} строк × {df.shape[1]} столбцов")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df.to_parquet(OUTPUT_FILE, index=False)
    print(f"Сохранено: {OUTPUT_FILE}")
