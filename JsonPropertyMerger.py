# Author: C.F. Wagner
# Date: 2022/09/24
# Title: JsonPropertyMerger

import json
import exiftool
import datetime
from typing import Any, Union, Optional, List, Dict


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
            print("Failed to open file:", jsonFile, "Error:", e)

        if (data is not None):
            print("Data extracted:", data)

        return data

    @staticmethod
    def ExtractMetaData(file: Union[str, List[str]] = ""):
        metadata = None
        try:
            with exiftool.ExifToolHelper() as et:
                metadata = et.get_metadata(file)
        except Exception as e:
            print("Failed to extract metadata from file:", file, "Error:", e)

        if (metadata is not None):
            print(metadata)

        if (type(file) == "str" and len(metadata) == 1):
            return metadata[0]
        else:
            return metadata

    @staticmethod
    def UpdateImageMetaDataWithJson(imagefile: str, googleMetadata: json):
        description = googleMetadata.get("description")
        photoTakenTime = googleMetadata.get("photoTakenTime")
        if (description is not None and len(description) > 0):
            print("Description:", description)

        if (photoTakenTime is not None):
            photoTakenTimeEpoch = photoTakenTime.get("timestamp")
            if (photoTakenTimeEpoch is not None):
                print("PhotoTakenTimeEpoch:", photoTakenTimeEpoch)


if __name__ == "__main__":
    json = JsonPropertyMerger.ExtracJsonData("TestPhotos/IMG_20220102_094708117.jpg.json")
    # JsonPropertyMerger.ExtracJsonData("TestPhotos/IMG_20220102_094728921.jpg.json")

    JsonPropertyMerger.UpdateImageMetaDataWithJson("", json)

    # JsonPropertyMerger.ExtractMetaData(["TestPhotos/IMG_20220102_094708117.jpg", "TestPhotos/IMG_20221001_091508974.jpg"])

    JsonPropertyMerger.ExtractMetaData("TestPhotos/IMG_20220102_094728921.jpg")

    # JsonPropertyMerger.ExtractMetaData(["TestPhotos/IMG_20220102_094728921.jpg", "TestPhotos/IMG_20220102_094708117.jpg"])
