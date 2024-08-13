from fastapi import HTTPException
from sqlalchemy.orm import Session

from modules.company.modelo import Company


def get_company_by_id_or_404(db: Session, company_id: int):
    """
    Fetches an company by its ID from the database.

    If the company is not found, raises a 404 HTTPException.

    Args:
        db (Session): The database session used to perform the query.
        company_id (int): The ID of the company to be fetched.

    Returns:
        The company instance if found.

    Raises:
        HTTPException: If the company is not found, a 404 error is raised with the message "Company not found"
    """
    if not (company := get_company_by_id(db=db, id_company=company_id)):
        raise HTTPException(status_code=404, detail="Company not found")
    return company


def get_company_by_id(db: Session, id_company: int):
    return db.query(Company).filter(Company.id == id_company).first()


def get_all_companies(db_session: Session):
    return db_session.query(Company).all()
