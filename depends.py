import httpx
from fastapi.exceptions import HTTPException

from service.connect import Connect


async def authenticate_ms_token(token: str):
    auth_endpoint = "http://localhost:8000/user/api/v1/authentication/validation/"

    headers = {"Content-Type": "application/json"}
    payload = {"token": token}

    async with httpx.AsyncClient() as client:
        response = await client.post(auth_endpoint, json=payload, headers=headers)

    if response.status_code == 200:
        return True
    raise HTTPException(status_code=response.status_code, detail="Authentication failed")


def get_db_session():
    connection = Connect()
    try:
        session = connection.get_session()
        yield session  # garante que vai retorna e cair no finally
    finally:
        session.close()



