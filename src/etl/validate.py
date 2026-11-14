
import pandas as pd


EXPECTED_COLUMNS = [
    "hotel", "is_canceled", "lead_time", "arrival_date_year",
    "arrival_date_month", "arrival_date_week_number",
    "arrival_date_day_of_month", "stays_in_weekend_nights",
    "stays_in_week_nights", "adults", "children", "babies",
    "meal", "country", "market_segment", "distribution_channel",
    "is_repeated_guest", "previous_cancellations",
    "previous_bookings_not_canceled", "reserved_room_type",
    "assigned_room_type", "booking_changes", "deposit_type",
    "agent", "company", "days_in_waiting_list", "customer_type",
    "adr", "required_car_parking_spaces",
    "total_of_special_requests", "reservation_status",
    "reservation_status_date"
]


def validate_data(df, max_rows=None):
    """Проверяет корректность данных перед загрузкой."""

    # 1. Проверяем, что DataFrame не пустой
    if df.empty:
        raise ValueError("Датасет пустой")

    # 2. Проверяем наличие необходимых столбцов
    missing_columns = set(EXPECTED_COLUMNS) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Отсутствуют столбцы: {missing_columns}"
        )

    # 3. Проверяем дубликаты
    duplicates = df.duplicated().sum()

    print(f"Найдено дубликатов: {duplicates}")

    # 4. Проверяем бинарные признаки
    binary_cols = ["is_canceled", "is_repeated_guest"]

    for col in binary_cols:
        if not df[col].isin([True, False]).all():
            raise ValueError(
                f"Некорректные значения в столбце {col}"
            )

    # 5. Проверяем количество строк
    if max_rows is not None and len(df) > max_rows:
        raise ValueError(
            f"Превышен лимит: {len(df)} строк, "
            f"максимум {max_rows}"
        )

    print("Validate: все обязательные проверки пройдены")

    return df
