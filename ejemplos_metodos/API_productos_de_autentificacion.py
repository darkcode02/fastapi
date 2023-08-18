from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

# Modelo de datos para un producto
class Product(BaseModel):
    name: str
    price: float

# Lista para almacenar productos
products = []

# Modelo de datos para un usuario
class User(BaseModel):
    username: str
    password: str

# Lista para almacenar usuarios (simulación)
users = []

# Simulación de base de datos de usuarios
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "password": "testpassword"
    }
}

# Configuración del esquema de autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Ruta para obtener un token de acceso (simulación de autenticación)
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if user is None or user["password"] != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user["username"], "token_type": "bearer"}

# Ruta para crear un producto con autenticación
@app.post("/products/", response_model=Product)
def create_product(product: Product, token: str = Depends(oauth2_scheme)):
    if token not in fake_users_db:
        raise HTTPException(status_code=401, detail="Unauthorized")
    products.append(product)
    return product

# Ruta para obtener todos los productos
@app.get("/products/", response_model=list)
def get_products():
    return products
