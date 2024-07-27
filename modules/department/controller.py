from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from depends import get_db_session, authenticate_ms_token
from modules.company.dao import get_departments_by_company_id, get_company_by_id

department_router = APIRouter(prefix="/tomba")


@department_router.get("/api/v1/company/{company_id}/departments/", response_model=dict)
async def get_departments(company_id: int, token: str | None = Header(default=None), db_session: Session = Depends(get_db_session)):
    await authenticate_ms_token(token)
    company = get_company_by_id(db_session, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    departments = get_departments_by_company_id(db_session, company_id)
    response_data = {"response": [{"id": department.id, "name": department.name} for department in departments]}
    return response_data

