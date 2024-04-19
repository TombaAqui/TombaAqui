# dao.py

from sqlalchemy.orm import Session

from modules.company.modelo import Company
from modules.department.modelo import Department


def get_departments_by_company_id(db: Session, company_id: int):
    return db.query(Department).filter(Department.company_id == company_id).all()


def get_company_by_id(db: Session, company_id: int):
    return db.query(Company).filter(Company.id == company_id).first()
