from app import photos
import os


def do_upload(file_to_upload):
    filename = photos.save(file_to_upload)
    url = photos.url(filename)
    url = url.replace('_uploads/photos', os.environ.get('UPLOADED_PHOTOS_DEST'))
    return url