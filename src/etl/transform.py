
import pandas as pd


def transform_data(df):
    """
    Приводит типы столбцов датасета
    к необходимым и возвращает DataFrame.
    """

    df = df.copy()

    # Категориальные признаки
    category_cols = [
        "hotel", "arrival_date_month", "meal", "country",
        "market_segment", "distribution_channel",
        "reserved_room_type", "assigned_room_type",
        "deposit_type", "customer_type", "reservation_status"
    ]

    for col in category_cols:
        df[col] = df[col].astype("category")

    # ID агентов и компаний — категориальные признаки
    for col in ["agent", "company"]:
        df[col] = (
            pd.to_numeric(df[col])
            .astype("Int64")
            .astype("string")
            .astype("category")
        )

    # Бинарные признаки
    for col in ["is_canceled", "is_repeated_guest"]:
        df[col] = df[col].astype("bool")

    # Целочисленные признаки
    df["children"] = df["children"].astype("Int8")

    int_cols = [
        "lead_time", "arrival_date_year",
        "arrival_date_week_number", "arrival_date_day_of_month",
        "stays_in_weekend_nights", "stays_in_week_nights",
        "adults", "babies", "previous_cancellations",
        "previous_bookings_not_canceled", "booking_changes",
        "days_in_waiting_list", "required_car_parking_spaces",
        "total_of_special_requests"
    ]

    for col in int_cols:
        df[col] = df[col].astype("int16")

    # Вещественное число
    df["adr"] = df["adr"].astype("float32")

    # Дата
    df["reservation_status_date"] = pd.to_datetime(
        df["reservation_status_date"]
    )

    print("Transform: преобразование типов завершено")

    return df