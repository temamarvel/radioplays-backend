import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from colored import Fore, Back, Style


load_dotenv()


YANDEX_KEY_ID = os.getenv("YANDEX_KEY_ID")
YANDEX_KEY_SECRET = os.getenv("YANDEX_KEY_SECRET")
YANDEX_BUCKET = os.getenv("YANDEX_BUCKET")


_s3_client = boto3.client(service_name="s3",
                          endpoint_url="https://storage.yandexcloud.net",
                          aws_access_key_id=YANDEX_KEY_ID,
                          aws_secret_access_key=YANDEX_KEY_SECRET)


def get_s3_client():
    return _s3_client


def get_objects(s3_folder_key: str):
    response = get_s3_client().list_objects_v2(Bucket=YANDEX_BUCKET, Prefix=s3_folder_key)
    return response["Contents"]


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


def get_signed_urls(files, file_type: str) -> list[str]:
    files_of_type = (file["Key"] for file in files if file["Key"].endswith(file_type))

    urls = []
    for file in files_of_type:
        urls.append(generate_signed_url(file))

    return urls


def is_folder_exists(s3_key: str) -> bool:
    if get_objects(s3_key):
        return True
    else:
        return False