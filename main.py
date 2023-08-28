from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

# Crea una instancia de FastAPI
app = FastAPI()
app.title = "Mi aplicación con FastAPI"
app.version = "0.0.1"

# Crea las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

# Define una clase personalizada para manejar la autenticación JWT
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")

# Define una clase Pydantic para validar la entrada de usuario en el endpoint de login
class User(BaseModel):
    email: str
    password: str

# Define una clase Pydantic para representar los datos de una película
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=30)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi película",
                "overview": "Descripción de la película",
                "year": 2022,
                "rating": 9.8,
                "category": "Acción"
            }
        }

# Datos de ejemplo para las películas
movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },
    {
        "id": 2,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    }
]

# Ruta para mostrar un mensaje en la página de inicio
@app.get('/', response_class=HTMLResponse, tags=['home'])
def message():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        /* Estilos CSS para la página de inicio */
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f2f2f2;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            padding: 20px;
            width: 80%;
            max-width: 600px;
        }
        h1 {
            font-size: 24px;
            margin-bottom: 10px;
            color: #333;
        }
        p {
            font-size: 16px;
            line-height: 1.5;
            color: #666;
        }
        .method {
            font-weight: bold;
            color: #3498db;
            margin-bottom: 10px;
        }
    </style>
    <title>FastAPI - Métodos HTTP</title>
</head>
<body>
    <div class="container">
        <h1>Explorando Métodos HTTP en FastAPI</h1>
        <p>FastAPI es un marco web de Python que permite crear API REST de manera eficiente. A continuación, se explican los métodos HTTP más comunes:</p>
        
        <div class="method">
            <h2>GET</h2>
            <p>El método GET se utiliza para solicitar datos de un recurso específico. Es seguro y no debe cambiar el estado del servidor.</p>
        </div>
        
        <div class="method">
            <h2>POST</h2>
            <p>El método POST se utiliza para enviar datos al servidor para crear un nuevo recurso. Puede cambiar el estado del servidor.</p>
        </div>
        
        <div class="method">
            <h2>PUT</h2>
            <p>El método PUT se utiliza para actualizar un recurso existente en el servidor con los datos proporcionados. Debería ser idempotente.</p>
        </div>
        
        <div class="method">
            <h2>DELETE</h2>
            <p>El método DELETE se utiliza para eliminar un recurso del servidor. Debería ser idempotente y seguro.</p>
        </div>
    </div>
</body>
</html>

    """

# Endpoint de login
@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

# Endpoint para obtener la lista de películas
@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# Endpoint para obtener una película por su ID
@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db =  Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
            return JSONResponse(status_code=404, content={'message':"Id no encontrado"})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))
    

# Endpoint para obtener películas por categoría
@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db =  Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
            return JSONResponse(status_code=404, content={'message':"categoria no encontrada"})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))
# Endpoint para crear una película
@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})

# Endpoint para actualizar una película por su ID
@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message':'Id no encontrado'})
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    return JSONResponse(status_code=200, content={'message':'Se ha modificado la pelicula'})

# Endpoint para eliminar una película por su ID
@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message':'Id no encontrado'})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={'message':'Se ha eliminado la pelicula'})