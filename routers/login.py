from fastapi import APIRouter
from fastapi import  HTTPException
from fastapi.responses import JSONResponse
from utils.jwt_manager import create_token
from schemas.user import User


login_router = APIRouter()






# Crear una estructura de datos para almacenar usuarios
users = [
    {
        "email": "admin@gmail.com",
        "password": "admin"
    },
    {
        "email": "user1@gmail.com",
        "password": "password1"
    },
    {
        "email": "user2@gmail.com",
        "password": "password2"
    }
]

# Endpoint de login
@login_router.post('/login', tags=['auth'])
def login(user: User):
    # Buscar el usuario en la lista de usuarios
    found_user = None
    for stored_user in users:
        if stored_user["email"] == user.email and stored_user["password"] == user.password:
            found_user = stored_user
            break

    if found_user:
        token: str = create_token({"email": user.email})
        return JSONResponse(status_code=200, content=token)
    else:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
