from typing import List

from fastapi import APIRouter, Depends, status, HTTPException, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from depends import get_db_session, authenticate_ms_token
from modules.company.dao import get_departments_by_company_id, get_company_by_id
from modules.company.modelo import Company

company_router = APIRouter(prefix="/tomba")


@company_router.get('/api/v1/company/', response_model=List[dict])
async def get_companies(token: str | None = Header(default=None), db_session: Session = Depends(get_db_session)):
    await authenticate_ms_token(token)
    companies = db_session.query(Company).all()
    response = {
        'response': []
    }
    for company in companies:
        total_departments = len(company.departments)
        response['response'].append(
            {
                "id": company.id,
                "name": company.name,
                "sigla": company.sigla,
                "total_departments": total_departments,
            }
        )
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)
