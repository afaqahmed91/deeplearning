import pandas as pd
from typing import Dict


def load(path_to_data_folder):
    weather = pd.read_csv(
        path_to_data_folder + "data/raw/weather_data.csv",
        index_col="datetime",
    )
    ahu = pd.read_csv(
        path_to_data_folder + "data/raw/ahu_data.csv",
        index_col="datetime",
    )
    sensor = pd.read_csv(
        path_to_data_folder + "data/raw/sensor_data.csv",
        index_col="datetime",
    )
    hwl = pd.read_csv(
        path_to_data_folder + "data/raw/hwl_data.csv",
        index_col="datetime",
    )
    data = {
        "weather": weather,
        "ahu": ahu,
        "sensor": sensor,
        "hwl": hwl,
    }
    for key in data:
        data[key].index = pd.to_datetime(data[key].index, utc=True)
    return data


def combine(data: Dict[str, pd.DataFrame]):
    combined_df = pd.DataFrame()
    for key in ["ahu", "hwl"]:
        combined_df = pd.concat([combined_df, data[key]], axis=1)
    combined_df = pd.concat(
        [
            combined_df,
            data["weather"][["DD", "FH", "temperature", "ghi", "R", "S", "U"]],
        ],
        axis=1,
    )
    avg_sensor = data["sensor"].mean(1)
    combined_df = pd.concat(
        [combined_df, pd.DataFrame(avg_sensor, columns=["ZAT"])], axis=1
    )
    combined_df = combined_df.ffill(axis=1)
    combined_df = combined_df.bfill(axis=1)
    combined_df = combined_df.asfreq("h")
    return combined_df
