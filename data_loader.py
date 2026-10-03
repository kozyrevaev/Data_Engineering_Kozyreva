import os
import gdown
import pandas as pd

file_ID = "1kzqYU6rFBZY_vPr8Ud1pgffuE-8rol6a"
file_name = "hotel_bookings.csv"

def load_data():
    if not os.path.exists(file_name):
        gdown.download(id=file_ID, output=file_name)
        df = pd.read_csv(file_name)
        print (df.head(10))

if __name__ == "__main__":
    load_data()