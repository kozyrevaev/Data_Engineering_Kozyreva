import os

import gdown
import pandas as pd

FILE_ID = "1kzqYU6rFBZY_vPr8Ud1pgffuE-8rol6a"
FILE_NAME = "hotel_bookings.csv"


def load_data():
    if not os.path.exists(FILE_NAME):
        gdown.download(id=FILE_ID, output=FILE_NAME)

    df = pd.read_csv(FILE_NAME)
    print(df.head(10))
    return df


if __name__ == "__main__":
    load_data()