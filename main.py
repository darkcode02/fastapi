# Importa las clases FastAPI y HTMLResponse desde el módulo fastapi
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Crea una instancia de FastAPI
app = FastAPI()

# Define el título y la versión de la aplicación
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

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
@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world<h1/>')

# Ruta para obtener la lista de películas
@app.get('/movies', tags=['movies'])
def get_movies():
    return movies

# Ruta para obtener detalles de una película por su ID
@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int):
    for item in movies:
        if item["id"] == id:
            return item
    return []

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str, year:int):
    for item in movies:
        if item["category"].lower() == category:
            return item
    return []