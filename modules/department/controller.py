from typing import List

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from depends import get_db_session, authenticate_ms_token
from modules.company.dao import get_company_by_id_or_404
from modules.department.dao import get_departments_by_company_id

department_router = APIRouter(prefix="/tomba")


@department_router.get("/api/v1/company/{id_company}/departments/", response_model=List[dict])
async def get_departments(id_company: int, token: str | None = Header(default=None), db_session: Session = Depends(get_db_session)):
    await authenticate_ms_token(token)
    get_company_by_id_or_404(db_session, id_company)
    departments = get_departments_by_company_id(db_session, id_company)
    response = [{"id": department.id, "name": department.name} for department in departments]
    return response
