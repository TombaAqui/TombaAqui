import os

from fastapi import UploadFile, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.company.modelo import Company
from modules.department.dao import get_department_by_id_or_404
from modules.department.modelo import Department
from modules.equipment.modelo import Equipment
from modules.equipment_movement.modelo import EquipmentMovement, get_brasilia_time


def move_equipment_db(db: Session, equipment, new_department_id: int):
    validate_department_transfer(db=db, old_department_id=equipment.department_id, new_department_id=new_department_id)
    # Atualiza o departamento do equipamento
    equipment.department_id = new_department_id
    # Registra a movimentação
    movement = EquipmentMovement(
        equipment_id=equipment.id,
        department_id=new_department_id,
        created_at=get_brasilia_time()
    )
    db.add(movement)
    # Salva as alterações no banco de dados
    db.commit()
    db.refresh(equipment)
    return equipment


def get_equipment_by_id_or_404(db: Session, equipment_id: int):
    """
    Fetches an equipment by its ID from the database.

    If the equipment is not found, raises a 404 HTTPException.

    Args:
        db (Session): The database session used to perform the query.
        equipment_id (int): The ID of the equipment to be fetched.

    Returns:
        The equipment instance if found.

    Raises:
        HTTPException: If the equipment is not found, a 404 error is raised with the message "Equipment not found"
    """
    if not (equipment := get_equipment_by_id(db=db, equipment_id=equipment_id)):
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment


def update_equipment(db: Session, equipment, description: str, department_id: int, image: UploadFile):
    equipment.description = description
    equipment.department_id = department_id
    if image:
        equipment.image = save_image(image)
    db.commit()
    db.refresh(equipment)
    return equipment


def create_equipment_in_db(description: str, department_id: int, image: UploadFile, db: Session):
    file_save_path = save_image(image)
    db_equipment = Equipment(description=description, department_id=department_id, image=file_save_path)
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    register_equipment_movement(db=db, equipment_id=db_equipment.id, department_id=department_id)
    return db_equipment


def register_equipment_movement(db: Session, equipment_id: int, department_id: int):
    movement = EquipmentMovement(
        equipment_id=equipment_id,
        department_id=department_id,
        created_at=get_brasilia_time()
    )
    db.add(movement)
    db.commit()


def validate_department_transfer(db: Session, old_department_id: int, new_department_id: int):
    new_department = get_department_by_id_or_404(db=db, department_id=new_department_id, detail="New department not found")
    old_department = get_department_by_id_or_404(db=db, department_id=old_department_id, detail="Old department not found")
    # Verifica se o departamento do equipamento é da mesma company que o novo departamento
    if old_department.company_id != new_department.company_id:
        raise HTTPException(status_code=400, detail="Departments belong to different companies")
    return


def get_equipments_by_company_id(db: Session, company_id: int):
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

