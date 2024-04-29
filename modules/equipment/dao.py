import os

from fastapi import UploadFile

from modules.equipment.modelo import Equipment
from sqlalchemy.orm import Session


def create_equipment_in_db(description: str, department_id: int, image: UploadFile, db: Session):
    file_save_path = "./images/" + image.filename
    if not os.path.exists("./images"):
        os.makedirs("./images")
    with open(file_save_path, "wb") as f:
        f.write(image.file.read())

    db_equipment = Equipment(description=description, department_id=department_id, image=file_save_path)
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment
