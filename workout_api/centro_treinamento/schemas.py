from typing import Annotated
from pydantic import Field
from workout_api.contrib.schemas import BaseSchema

class CentroTreinamentoCategoria(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Centro do Treinamento', example='CT_King', max_length=20)]
    endereco: Annotated[str, Field(description='Endereço do Centro do Treinamento', example='Rua x quadra 2', max_length=60)]
    proprietario: Annotated[str, Field(description='Proprietario do Centro do Treinamento', example='Marcos', max_length=30)]