# Importa las clases FastAPI y HTMLResponse desde el módulo fastapi
from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

# Crea una instancia de FastAPI
app = FastAPI()

# Define el título y la versión de la aplicación
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"


#creacion de esquemas
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview : str=Field(min_length=15, max_length=50)
    year: int  = Field(le=2023)
    rating: float = Field(ge=1,Le=10)
    category: str= Field(min_length=3, max_length=20)

    class Config:
        schema_extra = {
            "example":{
                "id":1,
                "title":"Mi pelicula",
                "overview": "Descripcion de la pelicula",
                "year":2023,
                "rating":9.8,
                "category":"Accion"

            }
        }



# Lista de películas en forma de diccionarios
movies = [
    {
        "id": 1,
        "title": "Aventuras en la Montaña",
        "overview": "Un grupo de amigos se embarca en una emocionante expedición por las montañas en busca de tesoros ocultos.",
        "year": 2022,
        "rating": 8.2,
        "category": "Aventura"
    },
    {
        "id": 2,
        "title": "El Misterio del Abismo",
        "overview": "Un detective debe resolver el misterio detrás de una serie de desapariciones inexplicables en un pequeño pueblo costero.",
        "year": 2023,
        "rating": 7.9,
        "category": "Misterio"
    },
    {
        "id": 3,
        "title": "Amor en la Ciudad",
        "overview": "Dos almas solitarias se encuentran en medio del ajetreo de la ciudad y descubren el verdadero significado del amor.",
        "year": 2021,
        "rating": 6.8,
        "category": "Romance"
    }
    # Puedes agregar más películas aquí en el mismo formato
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
      body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        background-color: #f2f2f2;
      }
      .container {
        background-color: #fff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        width: 80%;
        max-width: 600px;
      }
      h1 {
        font-size: 24px;
        margin-bottom: 10px;
      }
      p {
        font-size: 16px;
        line-height: 1.5;
      }
      .method {
        font-weight: bold;
        color: #3498db;
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


# Ruta para obtener la lista de películas
@app.get('/movies', tags=['movies'])
def get_movies():
    return movies

# Ruta para obtener detalles de una película por su ID
@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int = Path(ge=1, Le=2000)):
    for item in movies:
        if item["id"] == id:
            return item
    return []

# Ruta para obtener películas por categoría y año
@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    return [item for item in movies if item["category"].lower() == category]

# Ruta para crear una película mediante el método POST
@app.post('/movies', tags=['movies'])
def create_movie(movie:Movie):
    movies.append(movie)
    return movies

# Ruta para actualizar una película mediante el método PUT
@app.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, movie:Movie):
    for item in movies:
        if item["id"] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return movies

# Ruta para eliminar una película mediante el método DELETE
@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return movies
