
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text


ROOT = Path(__file__).resolve().parents[2]

load_dotenv(ROOT / ".env")

N_ROWS = 100


def get_engine():
    """Создаёт подключение к PostgreSQL."""

    url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_URL"],
        port=int(os.environ["DB_PORT"]),
        database=os.environ["DB_ROOT_BASE"],
    )

    return create_engine(url)


def load_data(df, table_name, engine):
    """Записывает не более 100 строк DataFrame в БД."""

    # Ограничиваем количество записываемых строк
    df = df.head(N_ROWS).copy()

    # PostgreSQL не поддерживает pandas category
    cat_cols = df.select_dtypes("category").columns
    df[cat_cols] = df[cat_cols].astype("string")

    # Записываем данные в таблицу
    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    # Проверяем количество записанных строк
    with engine.connect() as conn:
        count = conn.execute(
            text(f'SELECT COUNT(*) FROM "{table_name}"')
        ).scalar()

    print(f"Load: в таблицу {table_name} записано {count} строк")

    if count != len(df):
        raise RuntimeError(
            f"Ошибка записи: ожидалось {len(df)}, получено {count}"
        )

    return count