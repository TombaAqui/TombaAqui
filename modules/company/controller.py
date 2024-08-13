from typing import List

from fastapi import APIRouter, Depends, status, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from depends import get_db_session, authenticate_ms_token
from modules.company.modelo import Company

company_router = APIRouter(prefix="/tomba")


@company_router.get('/api/v1/company/', response_model=List[dict])
async def get_companies(token: str | None = Header(default=None), db_session: Session = Depends(get_db_session)):
    await authenticate_ms_token(token)
    companies = db_session.query(Company).all()

    response = [{
        "id": company.id,
        "name": company.name,
        "sigla": company.sigla,
        "total_departments": len(company.departments),
    } for company in companies]

    return JSONResponse(content=response, status_code=status.HTTP_200_OK)
