from fastapi import APIRouter, UploadFile, File, Depends, Form, status, Header, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from depends import get_db_session, authenticate_ms_token
from modules.company.dao import get_company_by_id
from modules.department.modelo import Department
from modules.equipment.dao import create_equipment_in_db, get_equipment_by_company_id

equipment_router = APIRouter(prefix="/tomba")


@equipment_router.post("/resgister/api/v1/equipment/")
async def create_equipment(token: str = Form(...), description: str = Form(...), department_id: int = Form(...),
                           image: UploadFile = File(None), db_session: Session = Depends(get_db_session)):
    await authenticate_ms_token(token)
    if image is None or image.filename == "" or image.size == 0:
        return JSONResponse({"error": "No image provided or corrupted file"}, status_code=status.HTTP_400_BAD_REQUEST)
    if not any(ext in image.filename.lower() for ext in ('.jpg', '.jpeg', '.png')):
        return JSONResponse({"error": "Unsupported file type. Please upload only jpg, jpeg, or png files."},
                            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    department = db_session.query(Department).filter(Department.id == department_id).first()
    if not department:
        return JSONResponse({"error": f"Department with ID {department_id} not found"},
                            status_code=status.HTTP_404_NOT_FOUND)
    create_equipment_in_db(description, department_id, image, db_session)
    return JSONResponse(content={"message": "Equipment created successfully."}, status_code=status.HTTP_201_CREATED)


@equipment_router.get("/api/v1/company/{id_company}/equipments/")
async def get_equipments(id_company: int, token: str | None = Header(default=None),
                         db_session: Session = Depends(get_db_session)):
    await authenticate_ms_token(token)
    company = get_company_by_id(db=db_session, id_company=id_company)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    equipments = get_equipment_by_company_id(db_session, id_company)
    response_data = {'response': [{'id': equipment.id, 'description': equipment.description,
                                   'department': {'id': equipment.department.id, 'name': equipment.department.name},
                                   'image': equipment.image} for equipment in equipments]}
    return response_data


@equipment_router.get("/api/v1/company/{id_company}/equipments/{id_department}/")
async def get_equipments_by_deparment(id_company: int, id_department: int, token: str | None = Header(default=None), db_session: Session = Depends(get_db_session)):
    await authenticate_ms_token(token)
    company = get_company_by_id(db=db_session, id_company=id_company)
    if not company:
        raise HTTPException(status_code=404, detail='Company not found')
    department = None
    for dept in company.departments:
        if dept.id == id_department:
            department = dept
            break
    if not department:
        raise HTTPException(status_code=404, detail='Department not found')
    return {"response": department.equipments}

