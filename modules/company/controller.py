import http.client
import json
from typing import List

from fastapi import APIRouter, requests

from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from depends import get_db_session, authenticate_ms_token
from modules.company.modelo import Company

company_router = APIRouter(prefix="/company", dependencies=[Depends(authenticate_ms_token)])


@company_router.get('/api/v1/company/', response_model=List[dict])
def get_companies(db_session: Session = Depends(get_db_session)):
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
    return response
