from typing import Annotated
from pydantic import Field
from workout_api.contrib.schemas import BaseSchema

class Categoria(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Categotia', example='Scale', max_length=10)]