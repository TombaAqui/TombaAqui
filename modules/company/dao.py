# dao.py

from sqlalchemy.orm import Session

from modules.company.modelo import Company


def get_company_by_id(db: Session, id_company: int):
    return db.query(Company).filter(Company.id == id_company).first()
