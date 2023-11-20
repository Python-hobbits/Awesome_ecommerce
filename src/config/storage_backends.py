import uuid
from enum import Enum
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage


class StorageType(Enum):
    """Enumeration for different storage types."""

    STATIC = "Static"
    PUBLIC = "Public"
    PRIVATE = "Private"


class StaticStorage(S3Boto3Storage):
    """Storage class for static files on S3.

    - Location: "static"
    - ACL: public-read (Files are publicly readable)
    - Querystring Authentication: Disabled
    """

    location = "static"
    default_acl = "public-read"
    querystring_auth = False


class PublicMediaStorage(S3Boto3Storage):
    """Storage class for public media files on S3.

    - Location: "media"
    - ACL: public-read (Files are publicly readable)
    - File Overwrite: Disabled
    - Querystring Authentication: Disabled
    """

    location = "media"
    default_acl = "public-read"
    file_overwrite = False
    querystring_auth = False


class PrivateMediaStorage(S3Boto3Storage):
    """Storage class for private media files on S3.

    - Location: "private"
    - ACL: private (Files are not publicly readable)
    - File Overwrite: Disabled
    - Custom Domain: Disabled
    """

    location = "private"
    default_acl = "private"
    file_overwrite = False
    custom_domain = False


def get_static_storage():
    if settings.USE_MINIO:
        return StaticStorage()
    else:
        return FileSystemStorage()


def get_public_storage():
    if settings.USE_MINIO:
        return PublicMediaStorage()
    else:
        return FileSystemStorage()


def get_private_storage():
    if settings.USE_MINIO:
        return PrivateMediaStorage()
    else:
        return FileSystemStorage()


# Generate a UUID and use it as part of the filename
def profile_picture_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"profile_pictures/{filename}"
