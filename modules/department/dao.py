from fastapi import HTTPException
from sqlalchemy.orm import Session

from modules.department.modelo import Department


def get_departments_by_company_id(db: Session, id_company: int):
    return db.query(Department).filter(Department.company_id == id_company).all()


def get_department_by_id(db: Session, department_id: int):
    return db.query(Department).filter(Department.id == department_id).first()


def get_department_by_id_or_404(db: Session, department_id: int, detail: str = "Department not found"):
    """
    Fetches a department by its ID from the database.

    If the department is not found, raises a 404 HTTPException with a custom detail message.

    Args:
        db (Session): The database session used to perform the query.
        department_id (int): The ID of the department to be fetched.
        detail (str): Custom detail message for the HTTPException.

    Returns:
        Department: The department instance if found.

    Raises:
        HTTPException: If the department is not found, a 404 error is raised with the provided detail message.
    """
    if not (department := get_department_by_id(db=db, department_id=department_id)):
        raise HTTPException(status_code=404, detail=detail)
    return department

