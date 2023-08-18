from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# Crea una instancia de FastAPI
app = FastAPI()

# Configuración de CORS (Cross-Origin Resource Sharing) para permitir solicitudes desde cualquier origen
origins = ["*"]  # En un entorno de producción, debes limitar los orígenes permitidos
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])

# Lista de películas en una base de datos o almacenamiento persistente
class MovieDB:
    def __init__(self):
        self.movies = [
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
        self.next_id = 4  # Para asignar IDs a nuevas películas

db = MovieDB()

# Ruta para mostrar un mensaje en la página de inicio
@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world<h1/>')

# Ruta para obtener la lista de películas
@app.get('/movies', tags=['movies'])
def get_movies():
    return db.movies

# Ruta para obtener detalles de una película por su ID
@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int):
    for item in db.movies:
        if item["id"] == id:
            return item
    return []

# Ruta para obtener películas por categoría y año
@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str, year: int):
    return [item for item in db.movies if item["category"].lower() == category]

# Ruta para crear una película mediante el método POST
@app.post('/movies', tags=['movies'])
def create_movie(movie: dict = Body()):
    movie["id"] = db.next_id
    db.next_id += 1
    db.movies.append(movie)
    return movie

# Ruta para actualizar una película mediante el método PUT
@app.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, movie: dict = Body()):
    for item in db.movies:
        if item["id"] == id:
            for key in movie:
                item[key] = movie[key]
            return item
    return []

# Ruta para eliminar una película mediante el método DELETE
@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    for item in db.movies:
        if item["id"] == id:
            db.movies.remove(item)
            return db.movies
    return []

# Estructura para correr la aplicación en producción
if __name__ == "__main__":
    import uvicorn
    
    # Configuración para el servidor ASGI (uvicorn en este caso)
    uvicorn.run(app, host="0.0.0.0", port=8000)
