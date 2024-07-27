import os

from fastapi import UploadFile
from sqlalchemy import select

from modules.company.modelo import Company
from modules.department.modelo import Department
from modules.equipment.modelo import Equipment
from sqlalchemy.orm import Session


def create_equipment_in_db(description: str, id_department: int, image: UploadFile, db: Session):
    file_save_path = "./images/" + image.filename
    if not os.path.exists("./images"):
        os.makedirs("./images")
    with open(file_save_path, "wb") as f:
        f.write(image.file.read())
    db_equipment = Equipment(description=description, department_id=id_department, image=file_save_path)
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment


def get_equipment_by_company_id(db: Session, id_company: int):
    stmt = select(Equipment).join(Department).join(Company).where(Company.id == id_company)
    results = db.execute(stmt).scalars().all()

    return results
