
from pathlib import Path

import gdown
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

FILE_ID = "1kzqYU6rFBZY_vPr8Ud1pgffuE-8rol6a"
FILE_NAME = ROOT / "hotel_bookings.csv"


def extract_data():
    """
    Загружает исходный датасет с Google Drive
    и возвращает его в виде pandas DataFrame.
    """

    if not FILE_NAME.exists():
        print("Загружаем исходный датасет...")
        gdown.download(
            id=FILE_ID,
            output=str(FILE_NAME),
            quiet=False
        )

    if not FILE_NAME.exists():
        raise FileNotFoundError("Не удалось загрузить датасет")

    df = pd.read_csv(FILE_NAME, na_values="NULL")

    print(f"Extract: загружено {len(df)} строк")
    return df