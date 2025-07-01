import os
import boto3
# from botocore.exceptions import ClientError
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


def generate_signed_url(s3_key: str, expires_in: int = 600):
    url = get_s3_client().generate_presigned_url(ClientMethod='get_object',
                                                 Params={
                                                     'Bucket': YANDEX_BUCKET,
                                                     'Key': s3_key
                                                 },
                                                 ExpiresIn=expires_in)
    """
    Генерирует временную ссылку для скачивания файла из S3.

    :param s3_key: Путь к файлу в бакете
    :param expires_in: Время жизни ссылки в секундах
    :return: URL-строка
    """
    return url