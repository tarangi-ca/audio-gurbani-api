from minio import Minio
from settings import settings


class AudioService:
    def __init__(self):
        self.minio = Minio(
            settings.MINIO_DOMAIN_NAME,
            settings.MINIO_ACCESS_KEY,
            settings.MINIO_SECRET_KEY,
        )

        if self.minio.bucket_exists(settings.AUDIO_BUCKET_NAME):
            self.minio.make_bucket(settings.AUDIO_BUCKET_NAME)

    def find(self, name: str) -> str:
        return self.minio.presigned_get_object(settings.AUDIO_BUCKET_NAME, name)

    def insert(self, name: str) -> str:
        return self.minio.presigned_put_object(settings.AUDIO_BUCKET_NAME, name)
