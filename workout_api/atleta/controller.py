import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from workout_api.atleta.schemas import AtletaIn, AtletaOut
from workout_api.atleta.models import AtletaModel
from workout_api.categorias.models import CategoriaModel
from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select

router = APIRouter()

@router.post(
    '/',
    summary='Criar novo atleta',
    status_code=status.HTTP_201_CREATED
)

async def post(
    db_session: DatabaseDependency,
    atleta_in: AtletaIn = Body(...)
):
    categoria_name = atleta_in.categoria.nome

    categoria = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=categoria_name))
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'(A categoria {categoria_name} não foi encontrada!)'
        )

    atleta_out = AtletaOut(id=uuid4(),created_at=datetime.utcnow(), **atleta_in.model_dump())
    atleta_model = AtletaModel(**atleta_out.model_dump())
    db_session.add(atleta_model)
    await db_session.commit()

    return atleta_out