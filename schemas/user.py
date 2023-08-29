from pydantic import BaseModel

# Define una clase Pydantic para validar la entrada de usuario en el endpoint de login
class User(BaseModel):
    email: str
    password: str