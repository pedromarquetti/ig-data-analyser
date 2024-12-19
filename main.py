import pandas as pd 
import os 
import json 
from time import strftime,localtime

DEFAULT_FILEPATH = "./data/"
WRITE_FILE = "data.csv"
data = []


def read_files():
    directory = os.fsencode(DEFAULT_FILEPATH)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        if filename.endswith(".json"):

            with open(f"{DEFAULT_FILEPATH}/{filename}") as fread:
                json_data = json.load(fread)
                data.extend(json_data["messages"])

def write_to_file():
    with open(WRITE_FILE,"w") as fwrite:
        pass

def main():
    read_files()
    df = pd.DataFrame(data)
    df["timestamp_ms"] = pd.to_datetime(df["timestamp_ms"],unit="ms")

    # save data to csv
    df.to_csv("dados.csv")

if __name__ == "__main__":
    main()
