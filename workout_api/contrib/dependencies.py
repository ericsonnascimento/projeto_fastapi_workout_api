from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from workout_api.configs.database import get_session

#Aqui significa que o nosso controler depende de uma sessão para funcionar
DatabaseDependency = Annotated[AsyncSession, Depends(get_session)]