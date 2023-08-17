from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

movies= [
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


@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world<h1/>')


@app.get('/movies', tags=['movies'])
def get_movies():
    return movies