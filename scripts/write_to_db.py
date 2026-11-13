import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text

ROOT = Path(__file__).resolve().parent.parent
PARQUET = ROOT / "hotel_bookings.parquet"  # создаётся data_loader.py

N_ROWS = 100

# креды и параметры подключения берём из .env (файл не коммитится)
load_dotenv(ROOT / ".env")


def get_engine():
    url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_URL"],
        port=int(os.environ["DB_PORT"]),
        database=os.environ["DB_ROOT_BASE"],
    )
    return create_engine(url)


def prepare_data(n_rows=N_ROWS):
    df = pd.read_parquet(PARQUET).head(n_rows)

    # category в БД не существует — записываем такие столбцы как текст
    cat_cols = df.select_dtypes("category").columns
    df[cat_cols] = df[cat_cols].astype("string")
    return df


def write_table(df, engine, table_name):
    df.to_sql(table_name, engine, if_exists="replace", index=False)

    # проверка: читаем обратно число строк
    with engine.connect() as conn:
        count = conn.execute(text(f'SELECT COUNT(*) FROM "{table_name}"')).scalar()
    print(f"Таблица {table_name}: записано {count} строк")


if __name__ == "__main__":
    table_name = os.environ["TABLE_NAME"]
    engine = get_engine()
    df = prepare_data()
    write_table(df, engine, table_name)
