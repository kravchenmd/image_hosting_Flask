from pathlib import Path

from src import db
from src import models
from src.libs.file_service import move_picture
from src.repository.users import find_by_id


def get_pictures_user(user_id: int):
    return db.session.query(models.Picture).where(models.Picture.user_id == user_id).all()


def upload_file_for_user(user_id: int, file_path: Path, description: str) -> None:
    user = find_by_id(user_id)
    user_subfolder = f"{user_id}_{user.username}"
    filename, size = move_picture(user_subfolder, file_path)
    picture = models.Picture(path=filename, description=description, user_id=user_id, size=size)
    db.session.add(picture)
    db.session.commit()
