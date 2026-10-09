import os

import gdown
import pandas as pd

FILE_ID = "1kzqYU6rFBZY_vPr8Ud1pgffuE-8rol6a"
FILE_NAME = "hotel_bookings.csv"
PARQUET_NAME = "hotel_bookings.parquet"


def load_data():
    if not os.path.exists(FILE_NAME):
        gdown.download(id=FILE_ID, output=FILE_NAME)

    df = pd.read_csv(FILE_NAME, na_values="NULL")
    print(df.head(10))
    return df


def convert_types(df):
    df = df.copy()

    # признаки по категориям
    category_cols = [
        "hotel", "arrival_date_month", "meal", "country", "market_segment",
        "distribution_channel", "reserved_room_type", "assigned_room_type",
        "deposit_type", "customer_type", "reservation_status",
    ]
    for col in category_cols:
        df[col] = df[col].astype("category")

    # ID агентов и компаний — метки, а не числа (9, а не 9.0)
    for col in ["agent", "company"]:
        df[col] = pd.to_numeric(df[col]).astype("Int64").astype("string").astype("category")

    # бинарные признаки 0/1 -> True/False
    for col in ["is_canceled", "is_repeated_guest"]:
        df[col] = df[col].astype("bool")

    # целые числа; в children есть пропуски, поэтому Int8 с большой буквы
    df["children"] = df["children"].astype("Int8")
    int_cols = [
        "lead_time", "arrival_date_year", "arrival_date_week_number",
        "arrival_date_day_of_month", "stays_in_weekend_nights",
        "stays_in_week_nights", "adults", "babies", "previous_cancellations",
        "previous_bookings_not_canceled", "booking_changes",
        "days_in_waiting_list", "required_car_parking_spaces",
        "total_of_special_requests",
    ]
    for col in int_cols:
        df[col] = df[col].astype("int16")

    # дробное число — цена за ночь
    df["adr"] = df["adr"].astype("float32")

    # дата
    df["reservation_status_date"] = pd.to_datetime(df["reservation_status_date"])

    return df


def save_parquet(df):
    df.to_parquet(PARQUET_NAME, index=False)
    print(f"Сохранено: {PARQUET_NAME}")


if __name__ == "__main__":
    df = load_data()
    df = convert_types(df)
    print(df.dtypes)
    save_parquet(df)