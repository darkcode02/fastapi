from fastapi import  FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from utils.jwt_manager import create_token
from config.database import  engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.login import login_router


# Crea una instancia de FastAPI
app = FastAPI()
app.title = "Mi aplicación con FastAPI"
app.version = "0.0.1"
app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(login_router)

# Crea las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

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


