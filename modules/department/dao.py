from sqlalchemy.orm import Session

from modules.department.modelo import Department


def get_departments_by_company_id(db: Session, id_company: int):
    return db.query(Department).filter(Department.company_id == id_company).all()
