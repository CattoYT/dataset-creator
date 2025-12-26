from requests.compat import str
import pandas as pd
from datasets import Dataset
from pandas_audio_methods import SFMethods

pd.api.extensions.register_series_accessor("sf")(SFMethods)


def create_parquet(list_file: str):
    # list_file = input("Give list file")

    rows = []
    with open(list_file, "r", encoding="utf-8") as f:
        for line in f:
            # Strip newline and split on first 3 pipes
            parts = line.strip().split(
                "|", 3
            )  # max 4 parts: path, character, language, transcript
            if len(parts) == 4:
                rows.append(parts)

    # Convert to DataFrame
    df = pd.DataFrame(rows, columns=["path", "character", "language", "text"])  # ty:ignore[invalid-argument-type]

    # Keep only audio path and transcript
    df = df[["path", "text"]]

    df["audio"] = df["path"].sf.open()
    df2 = df[["audio", "text"]]

    hf_dataset = Dataset.from_pandas(df2)
    parquet_file = list_file.replace("list", "parquet")
    hf_dataset.to_parquet(parquet_file)

    import os

    os.makedirs(f"exports/{parquet_file.replace('parquet', '')}", exist_ok=True)
    # shutil.copytree("Cyrene-cleaned", "exports/cyrene-cleaned/Cyrene-cleaned")
    os.rename(
        parquet_file, f"exports/{parquet_file.replace('parquet', '')}/{parquet_file}"
    )
