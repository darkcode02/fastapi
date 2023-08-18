from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Modelo de datos para un usuario
class User(BaseModel):
    username: str
    email: str

# Lista para almacenar usuarios
users = []

# Ruta para crear un usuario
@app.post("/users/", response_model=User)
def create_user(user: User):
    users.append(user)
    return user

# Ruta para obtener todos los usuarios
@app.get("/users/", response_model=list)
def get_users():
    return users

# Ruta para obtener un usuario por su ID
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    if user_id < len(users):
        return users[user_id]
    raise HTTPException(status_code=404, detail="User not found")
