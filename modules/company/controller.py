from typing import List

from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from modules.company.dao import get_departments_by_company_id, get_company_by_id
from depends import get_db_session, authenticate_ms_token
from modules.company.modelo import Company

company_router = APIRouter(prefix="/tomba")


@company_router.get('/api/v1/company/', response_model=List[dict])
async def get_companies(request: Request, db_session: Session = Depends(get_db_session)):
    payload = await request.json()
    token = payload.get("token")
    await authenticate_ms_token(token)
    companies = db_session.query(Company).all()
    response = []
    for company in companies:
        total_departments = len(company.departments)
        response.append(
            {
                "name": company.name,
                "sigla": company.sigla,
                "total_departments": total_departments,
            }
        )
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


@company_router.get("/api/v1/company/{company_id}/departments/", response_model=dict)
async def get_departments(request: Request, company_id: int, db_session: Session = Depends(get_db_session)):
    payload = await request.json()
    token = payload.get("token")
    await authenticate_ms_token(token)
    company = get_company_by_id(db_session, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    departments = get_departments_by_company_id(db_session, company_id)
    response_data = {"response": [{"id": department.id, "name": department.name} for department in departments]}
    return response_data

