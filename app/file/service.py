from file.schemas import FileFolder
from minio import Minio
from utilities.settings import settings


class FileService:
    def __init__(self):
        self.minio = Minio(
            settings.MINIO_DOMAIN_NAME,
            settings.MINIO_ACCESS_KEY,
            settings.MINIO_SECRET_KEY,
            secure=False,
        )

        if not self.minio.bucket_exists(settings.APP_BUCKET_NAME):
            self.minio.make_bucket(settings.APP_BUCKET_NAME)

    def find(self, folder: FileFolder, name: str) -> str:
        return self.minio.presigned_get_object(
            settings.APP_BUCKET_NAME, f"{folder.value}/{name}"
        )

    def insert(self, folder: FileFolder, name: str) -> str:
        return self.minio.presigned_put_object(
            settings.APP_BUCKET_NAME, f"{folder.value}/{name}"
        )
