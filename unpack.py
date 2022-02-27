import os
import json
from typing import Any, Dict
from urllib.parse import urlparse
import shutil
import gzip
import requests


class Unpacker:

    def __init__(self, baseurl: str, target_dir: str, is_verbose: bool = False):
        self.baseurl = baseurl
        self.target_dir = target_dir
        self.locale = "en"  # TODO: assume en for now
        self.is_verbose = is_verbose

    def unpack_level(self, name: str):
        res_url = self.__get_absolute_url(f"levels/{name}")
        response = requests.get(res_url)
        if self.is_verbose:
            print(f"{response.status_code} - {res_url}")
        data = response.json()

        res_dir = os.path.join(self.target_dir, f"levels/{name}")
        os.makedirs(res_dir, exist_ok=True)

        with open(os.path.join(res_dir, "info.json"), "w") as f:
            json.dump({
                "version": data["item"]["version"],
                "rating": data["item"]["rating"],
                "engine": data["item"]["engine"]["name"],
                "useSkin": data["item"]["useSkin"],
                "useBackground": data["item"]["useBackground"],
                "useEffect": data["item"]["useEffect"],
                "useParticle": data["item"]["useParticle"],
                "title": self.__convert_to_localization_text(data["item"]["title"]),
                "artists": self.__convert_to_localization_text(data["item"]["artists"]),
                "author": self.__convert_to_localization_text(data["item"]["author"]),
                "description": self.__convert_to_localization_text(data["description"]),
            }, f, indent=2)

        cover_url = self.__get_absolute_url(data["item"]["cover"]["url"])
        download_file(cover_url, os.path.join(res_dir, "cover.png"))

        bgm_url = self.__get_absolute_url(data["item"]["bgm"]["url"])
        download_file(bgm_url, os.path.join(res_dir, "bgm.mp3"))

        if "preview" in data["item"]:
            preview_url = self.__get_absolute_url(
                data["item"]["preview"]["url"])
            download_file(preview_url, os.path.join(res_dir, "preview.mp3"))

        data_url = self.__get_absolute_url(data["item"]["data"]["url"])
        download_unzip_file(data_url, os.path.join(res_dir, "data.json"))

    def unpack_skin(self, name: str):
        res_url = self.__get_absolute_url(f"skins/{name}")
        response = requests.get(res_url)
        if self.is_verbose:
            print(f"{response.status_code} - {res_url}")
        data = response.json()

        res_dir = os.path.join(self.target_dir, f"skins/{name}")
        os.makedirs(res_dir, exist_ok=True)

        with open(os.path.join(res_dir, "info.json"), "w") as f:
            json.dump({
                "version": data["item"]["version"],
                "title": self.__convert_to_localization_text(data["item"]["title"]),
                "subtitle": self.__convert_to_localization_text(data["item"]["subtitle"]),
                "author": self.__convert_to_localization_text(data["item"]["author"]),
                "description": self.__convert_to_localization_text(data["description"]),
            }, f, indent=2)

        thumbnail_url = self.__get_absolute_url(
            data["item"]["thumbnail"]["url"]
        )
        download_file(thumbnail_url, os.path.join(res_dir, "thumbnail.png"))

        data_url = self.__get_absolute_url(data["item"]["data"]["url"])
        download_unzip_file(data_url, os.path.join(res_dir, "data.json"))

        texture_url = self.__get_absolute_url(data["item"]["texture"]["url"])
        download_file(texture_url, os.path.join(res_dir, "texture.png"))

    def unpack_background(self, name: str):
        res_url = self.__get_absolute_url(f"backgrounds/{name}")
        response = requests.get(res_url)
        if self.is_verbose:
            print(f"{response.status_code} - {res_url}")
        data = response.json()

        res_dir = os.path.join(self.target_dir, f"backgrounds/{name}")
        os.makedirs(res_dir, exist_ok=True)

        with open(os.path.join(res_dir, "info.json"), "w") as f:
            json.dump({
                "version": data["item"]["version"],
                "title": self.__convert_to_localization_text(data["item"]["title"]),
                "subtitle": self.__convert_to_localization_text(data["item"]["subtitle"]),
                "author": self.__convert_to_localization_text(data["item"]["author"]),
                "description": self.__convert_to_localization_text(data["description"]),
            }, f, indent=2)

        thumbnail_url = self.__get_absolute_url(
            data["item"]["thumbnail"]["url"]
        )
        download_file(thumbnail_url, os.path.join(res_dir, "thumbnail.png"))

        data_url = self.__get_absolute_url(data["item"]["data"]["url"])
        download_unzip_file(data_url, os.path.join(res_dir, "data.json"))

        image_url = self.__get_absolute_url(data["item"]["image"]["url"])
        download_file(image_url, os.path.join(res_dir, "image.png"))

        configuration_url = self.__get_absolute_url(
            data["item"]["configuration"]["url"]
        )
        download_unzip_file(
            configuration_url,
            os.path.join(res_dir, "configuration.json")
        )

    def unpack_effect(self, name: str):
        res_url = self.__get_absolute_url(f"effects/{name}")
        response = requests.get(res_url)
        if self.is_verbose:
            print(f"{response.status_code} - {res_url}")
        data = response.json()

        res_dir = os.path.join(self.target_dir, f"effects/{name}")
        os.makedirs(res_dir, exist_ok=True)

        with open(os.path.join(res_dir, "info.json"), "w") as f:
            json.dump({
                "version": data["item"]["version"],
                "title": self.__convert_to_localization_text(data["item"]["title"]),
                "subtitle": self.__convert_to_localization_text(data["item"]["subtitle"]),
                "author": self.__convert_to_localization_text(data["item"]["author"]),
                "description": self.__convert_to_localization_text(data["description"]),
            }, f, indent=2)

        thumbnail_url = self.__get_absolute_url(
            data["item"]["thumbnail"]["url"]
        )
        download_file(thumbnail_url, os.path.join(res_dir, "thumbnail.png"))

        data_url = self.__get_absolute_url(data["item"]["data"]["url"])
        data_filename = os.path.join(res_dir, "data.json")
        download_unzip_file(data_url, data_filename)

        # Convert clip paths
        clips = []
        with open(data_filename, "r") as f:
            d = json.load(f)
            for clip in d["clips"]:
                clip_url = self.__get_absolute_url(
                    clip["clip"]["url"]
                )
                download_file(
                    clip_url,
                    os.path.join(
                        res_dir, os.path.basename(clip["clip"]["url"])
                    )
                )
                clips.append({
                    "id": clip["id"],
                    "clip": os.path.basename(clip["clip"]["url"])
                })
        with open(data_filename, "w") as f:
            json.dump({"clips": clips}, f)

    def unpack_particle(self, name: str):
        res_url = self.__get_absolute_url(f"particles/{name}")
        response = requests.get(res_url)
        if self.is_verbose:
            print(f"{response.status_code} - {res_url}")
        data = response.json()

        res_dir = os.path.join(self.target_dir, f"particles/{name}")
        os.makedirs(res_dir, exist_ok=True)

        with open(os.path.join(res_dir, "info.json"), "w") as f:
            json.dump({
                "version": data["item"]["version"],
                "title": self.__convert_to_localization_text(data["item"]["title"]),
                "subtitle": self.__convert_to_localization_text(data["item"]["subtitle"]),
                "author": self.__convert_to_localization_text(data["item"]["author"]),
                "description": self.__convert_to_localization_text(data["description"]),
            }, f, indent=2)

        thumbnail_url = self.__get_absolute_url(
            data["item"]["thumbnail"]["url"]
        )
        download_file(thumbnail_url, os.path.join(res_dir, "thumbnail.png"))

        data_url = self.__get_absolute_url(data["item"]["data"]["url"])
        download_unzip_file(data_url, os.path.join(res_dir, "data.json"))

        texture_url = self.__get_absolute_url(data["item"]["texture"]["url"])
        download_file(texture_url, os.path.join(res_dir, "texture.png"))

    def unpack_engine(self, name: str, is_recursive: bool = False):
        res_url = self.__get_absolute_url(f"engines/{name}")
        response = requests.get(res_url)
        if self.is_verbose:
            print(f"{response.status_code} - {res_url}")
        data = response.json()

        res_dir = os.path.join(self.target_dir, f"engines/{name}")
        os.makedirs(res_dir, exist_ok=True)

        with open(os.path.join(res_dir, "info.json"), "w") as f:
            json.dump({
                "version": data["item"]["version"],
                "title": self.__convert_to_localization_text(data["item"]["title"]),
                "subtitle": self.__convert_to_localization_text(data["item"]["subtitle"]),
                "author": self.__convert_to_localization_text(data["item"]["author"]),
                "description": self.__convert_to_localization_text(data["description"]),
                "skin": data["item"]["skin"]["name"],
                "background": data["item"]["background"]["name"],
                "effect": data["item"]["effect"]["name"],
                "particle": data["item"]["particle"]["name"],
            }, f, indent=2)

        thumbnail_url = self.__get_absolute_url(
            data["item"]["thumbnail"]["url"]
        )
        download_file(thumbnail_url, os.path.join(res_dir, "thumbnail.png"))

        data_url = self.__get_absolute_url(data["item"]["data"]["url"])
        download_unzip_file(data_url, os.path.join(res_dir, "data.json"))

        if "rom" in data["item"]["configuration"]:
            rom_url = self.__get_absolute_url(
                data["item"]["configuration"]["rom"]
            )
            download_unzip_file(
                rom_url,
                os.path.join(res_dir, "rom.bin")
            )

        configuration_url = self.__get_absolute_url(
            data["item"]["configuration"]["url"]
        )
        download_unzip_file(
            configuration_url,
            os.path.join(res_dir, "configuration.json")
        )

        if is_recursive:
            self.unpack_skin(data["item"]["skin"]["name"])
            self.unpack_background(data["item"]["background"]["name"])
            self.unpack_effect(data["item"]["effect"]["name"])
            self.unpack_particle(data["item"]["particle"]["name"])

    def __get_absolute_url(self, url: str) -> str:
        if len(urlparse(url).scheme) > 0:
            return url
        else:
            url = url.strip("/")
            return os.path.join(self.baseurl, url).replace("\\", "/")

    def __convert_to_localization_text(self, data: Any) -> Dict[str, str]:
        if type(data) == str:
            return {
                self.locale: data
            }
        else:
            return data


def download_file(url: str, target_filename: str):
    """Downloads a file.
    https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
    """
    with requests.get(url, stream=True) as r:
        with open(target_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)


def download_unzip_file(url: str, target_filename: str):
    """Downloads and unzips a file.
    """
    archive_filename = target_filename + ".gz"
    download_file(url, archive_filename)
    with gzip.open(archive_filename, "rb") as f_in:
        with open(target_filename, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(archive_filename)
