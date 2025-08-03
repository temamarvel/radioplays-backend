import os
from enum import Enum

import boto3
import requests
import fastapi
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from colored import Fore, Back, Style
import urllib.parse
import alchemy_models
import pydentic_models

load_dotenv()


YANDEX_KEY_ID = os.getenv("YANDEX_KEY_ID")
YANDEX_KEY_SECRET = os.getenv("YANDEX_KEY_SECRET")
YANDEX_BUCKET = os.getenv("YANDEX_BUCKET")

class FileKind(Enum):
    AUDIO = ""
    ORIGINAL = "Originals"
    THUMBNAIL = "Thumbnails"

    def get_info(self):
        match self:
            case FileKind.AUDIO:
                return (self.value, ".mp3")
            case FileKind.ORIGINAL:
                return (self.value, ".webp")
            case FileKind.THUMBNAIL:
                return (self.value, ".webp")
        return None


_s3_client = boto3.client(service_name="s3",
                          endpoint_url="https://storage.yandexcloud.net",
                          aws_access_key_id=YANDEX_KEY_ID,
                          aws_secret_access_key=YANDEX_KEY_SECRET)


def get_s3_client():
    return _s3_client


def get_objects(s3_folder_key: str):
    response = get_s3_client().list_objects_v2(Bucket=YANDEX_BUCKET, Prefix=s3_folder_key)
    return response.get("Contents")


def is_item_uploaded(s3_key: str):
    try:
        get_s3_client().head_object(Bucket=YANDEX_BUCKET, Key=s3_key)
        print(f"{Fore.green}The file {Style.bold}[{s3_key}]{Style.reset}{Fore.green} is existed in the bucket.{Style.reset}")
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            print(f"{Fore.yellow}The file {Style.bold}[{s3_key}]{Style.reset}{Fore.yellow} isn't existed in the bucket.{Style.reset}")
        else:
            print(f"{Fore.red}Error: {e}{Style.reset}")
    return False


def generate_signed_url(s3_key: str, expires_in: int = 600):
    url = get_s3_client().generate_presigned_url(ClientMethod='get_object',
                                                 Params={
                                                     'Bucket': YANDEX_BUCKET,
                                                     'Key': s3_key
                                                 },
                                                 ExpiresIn=expires_in)

    return url

def get_proxy_url(signed_url: str) -> fastapi.responses.StreamingResponse:
    response = requests.get(signed_url, stream=True)

    if response.status_code != 200:
        raise fastapi.HTTPException(status_code=404, detail="Файл не найден в хранилище")

    clean_url = urllib.parse.unquote(urllib.parse.urlparse(signed_url).path)
    file_name = os.path.basename(clean_url)
    # todo StreamingResponse can't work with cyrillic characters
    # do something with it in the future
    proxy_url = fastapi.responses.StreamingResponse(response.iter_content(chunk_size=8192),
                                                    media_type="audio/mpeg",
                                                    headers={"Accept-Ranges": "bytes",
                                                             "Content-Disposition": f'inline; filename=Test_audio'})

    return proxy_url

def get_signed_urls(files: list[alchemy_models.S3File], file_kind: FileKind) -> list[str]:
    urls = []

    if not files:
        return urls

    file_info = file_kind.get_info()
    file_prefix = file_info[0]
    file_type = file_info[1]
    files_of_type = (file.s3_key for file in files if file_prefix in file.s3_prefix and file.type == file_type)

    for file in files_of_type:
        signed_url = generate_signed_url(file)
        urls.append(signed_url)

    return urls


def is_folder_exists(s3_key: str) -> bool:
    if get_objects(s3_key):
        return True
    else:
        return False


# todo may be it have to be moved to separate file
# todo think & do it with router refactoring
def fill_play_properties(db_play: alchemy_models.Play)-> pydentic_models.Play:
    response_play = pydentic_models.Play(id=db_play.id, name=db_play.title)
    # todo uncomment for prod
    # response_play.audio_urls = get_signed_urls(db_play.files, FileKind.AUDIO)
    # response_play.cover_urls = get_signed_urls(db_play.files, FileKind.ORIGINAL)
    # response_play.thumbnail_urls = get_signed_urls(db_play.files, FileKind.THUMBNAIL)

    return response_play