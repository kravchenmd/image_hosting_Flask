from pathlib import Path

from src import db
from src import models
from src.libs.file_service import move_picture
from src.repository.users import find_by_id
from sqlalchemy import and_


def get_one_picture(pict_id: int, user_id: int):
    return db.session.query(models.Picture).where(and_(
        models.Picture.id == pict_id, models.Picture.user_id == user_id)).one()


def get_all_pictures(user_id: int):
    return db.session.query(models.Picture).where(models.Picture.user_id == user_id).all()


def upload_file_for_user(user_id: int, file_path: Path, description: str) -> None:
    user = find_by_id(user_id)
    user_subfolder = f"{user_id}_{user.username}"
    filename, size = move_picture(user_subfolder, file_path)
    picture = models.Picture(path=filename, description=description, user_id=user_id, size=size)
    db.session.add(picture)
    db.session.commit()


def update_picture(pic_id: int, user_id: int, description: str):
    picture = get_one_picture(pic_id, user_id)
    picture.description = description
    db.session.commit()
