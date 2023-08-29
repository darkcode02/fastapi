from pydantic import BaseModel, Field
from typing import Optional, List

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