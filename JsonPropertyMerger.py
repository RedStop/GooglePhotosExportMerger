# Author: C.F. Wagner
# Date: 2022/09/24
# Title: JsonPropertyMerger

import json


class JsonPropertyMerger:
    def __init__(this):
        pass

    @staticmethod
    def ExtracJsonData(jsonFile=""):
        data = None
        try:
            with open(jsonFile, mode="r") as file:
                data = json.load(file)
        except Exception as e:
            print("Failed to open file:", jsonFile, " Error:", e)

        if (data is not None):
            print("Data extracted:", data)

        return data


if __name__ == "__main__":
    JsonPropertyMerger.ExtracJsonData("TestPhotos/IMG_20220102_094708117.jpg.json")
    JsonPropertyMerger.ExtracJsonData("TestPhotos/IMG_20220102_094728921.jpg.json")
