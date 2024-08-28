from fastapi import APIRouter, File, Depends, Form, status, Header
from fastapi.responses import JSONResponse

from depends import get_db_session, authenticate_ms_token
from modules.company.dao import get_company_by_id_or_404
from modules.equipment.dao import *
from modules.equipment.schemas import EquipmentResponse

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
    get_department_by_id_or_404(db=db_session, department_id=department_id)
    equipment = create_equipment_in_db(description, department_id, image, db_session)
    equipment_response = EquipmentResponse.from_orm(equipment)
    return JSONResponse(content={"message": "Equipment created successfully.", "equipment": equipment_response.dict()}, status_code=status.HTTP_201_CREATED)


@equipment_router.get("/api/v1/company/{id_company}/equipments/")
async def get_equipments(id_company: int, token: str | None = Header(default=None), db_session: Session = Depends(get_db_session)):
    await authenticate_ms_token(token)
    get_company_by_id_or_404(db=db_session, company_id=id_company)
    equipments = get_equipments_by_company_id(db_session, id_company)
    response = [{'id': equipment.id, 'description': equipment.description, 'department': {'id': equipment.department.id, 'name': equipment.department.name}, 'image': equipment.image} for equipment in equipments]
    return response


@equipment_router.get("/api/v1/company/{id_company}/equipments/{id_department}/")
async def get_equipments_by_deparment(id_company: int, id_department: int, token: str | None = Header(default=None), db_session: Session = Depends(get_db_session)):
    await authenticate_ms_token(token)
    company = get_company_by_id_or_404(db=db_session, company_id=id_company)
    department = None
    for dept in company.departments:
        if dept.id == id_department:
            department = dept
            break
    if not department:
        raise HTTPException(status_code=404, detail='Department not found')
    return department.equipments


@equipment_router.put("/api/v1/equipment/{equipment_id}/")
async def update_equipment_by(equipment_id: int, token: str = Form(...), description: str = Form(...), department_id: int = Form(...), image: UploadFile = File(None), db_session: Session = Depends(get_db_session)):
    await authenticate_ms_token(token)
    equipment = get_equipment_by_id_or_404(db=db_session, equipment_id=equipment_id)
    # Se o departamento mudou, movimenta o equipamento e registra no histórico
    if equipment.department_id != department_id:
        try:
            validate_department_transfer(db=db_session, old_department_id=equipment.department_id,
                                         new_department_id=department_id)
            register_equipment_movement(db=db_session, equipment_id=equipment.id, department_id=department_id)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    updated_equipment = update_equipment(
        db=db_session,
        equipment=equipment,
        department_id=department_id,
        description=description,
        image=image)
    equipment_response = EquipmentResponse.from_orm(updated_equipment)
    return JSONResponse(content={"message": "Equipment updated successfully.", "equipment": equipment_response.dict()}, status_code=status.HTTP_200_OK)


@equipment_router.patch("/api/v1/equipment/{equipment_id}/move/")
async def move_equipment(equipment_id: int, new_department_id: int = Form(...), token: str = Form(...), db: Session = Depends(get_db_session)):
    await authenticate_ms_token(token)
    try:
        equipment = get_equipment_by_id_or_404(db=db, equipment_id=equipment_id)
        equipment = move_equipment_db(db, equipment, new_department_id)
        equipment_response = EquipmentResponse.from_orm(equipment)
        return JSONResponse(
            content={"message": "Equipment moved successfully.", "equipment": equipment_response.dict()},
            status_code=status.HTTP_200_OK)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
