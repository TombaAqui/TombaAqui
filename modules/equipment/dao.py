import os

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.company.modelo import Company
from modules.department.modelo import Department
from modules.equipment.modelo import Equipment


def update_equipment(db: Session, equipment, description: str, department_id: int, image: UploadFile):
    equipment.description = description
    equipment.department_id = department_id
    if image:
        equipment.image = save_image(image)
    db.commit()
    db.refresh(equipment)
    return equipment


def create_equipment_in_db(description: str, id_department: int, image: UploadFile, db: Session):
    file_save_path = save_image(image)
    db_equipment = Equipment(description=description, department_id=id_department, image=file_save_path)
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment


def get_equipment_by_company_id(db: Session, company_id: int):
    stmt = select(Equipment).join(Department).join(Company).where(Company.id == company_id)
    results = db.execute(stmt).scalars().all()
    return results


def get_equipment_by_id(db: Session, equipment_id: int):
    return db.query(Equipment).filter(Equipment.id == equipment_id).first()


def save_image(image: UploadFile) -> str:
    file_save_path = f"./images/{image.filename}"
    if not os.path.exists("./images"):
        os.makedirs("./images")
    with open(file_save_path, "wb") as f:
        f.write(image.file.read())
    return file_save_path

