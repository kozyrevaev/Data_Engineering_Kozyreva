
import argparse
import os

from etl.extract import extract_data
from etl.transform import transform_data
from etl.validate import validate_data
from etl.load import get_engine, load_data


def main():
    # Аргументы командной строки
    parser = argparse.ArgumentParser(
        description="ETL pipeline для Hotel Booking Demand"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Количество строк для загрузки в БД (максимум 100)"
    )

    args = parser.parse_args()

    if args.limit < 1 or args.limit > 100:
        parser.error("--limit должен быть от 1 до 100")

    # Получаем название таблицы из .env
    table_name = os.getenv("TABLE_NAME")

    if not table_name:
        parser.error("Не задано название таблицы TABLE_NAME в .env")

    print("\nНачало ETL-процесса")
    print("-" * 40)

    # 1. Extract
    print("\nЭтап 1: Extract")
    df = extract_data()

    # 2. Transform
    print("\nЭтап 2: Transform")
    df = transform_data(df)

    # 3. Validate
    print("\nЭтап 3: Validate")
    df_to_load = df.head(args.limit).copy()
    validate_data(df_to_load, max_rows=100)

    # 4. Load
    print("\nЭтап 4: Load")
    engine = get_engine()

    try:
        load_data(
            df=df_to_load,
            table_name=table_name,
            engine=engine
        )
    finally:
        engine.dispose()

    print("\n" + "-" * 40)
    print("ETL-процесс успешно завершён!")


if __name__ == "__main__":
    main()