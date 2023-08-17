# Mi Aplicación con FastAPI

Esta es una aplicación de ejemplo que utiliza FastAPI para crear una API web simple que muestra información sobre películas.

## Instalación

1. Clona este repositorio en tu máquina local.
2. Navega a la carpeta del proyecto:

   ```sh
   cd mi-aplicacion-fastapi
python -m venv venv
source venv/bin/activate  # En sistemas basados en Unix
venv\Scripts\activate     # En Windows
pip install -r requirements.txt

uvicorn main:app --reload

