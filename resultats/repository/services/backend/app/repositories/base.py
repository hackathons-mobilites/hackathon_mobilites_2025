"""
Repository de base avec méthodes CRUD génériques
"""
from typing import TypeVar, Generic, List, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase

T = TypeVar('T', bound=DeclarativeBase)


class BaseRepository(Generic[T]):
    """Repository de base avec opérations CRUD communes"""
    
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model
    
    async def get_by_id(self, id: int) -> Optional[T]:
        """Récupère un élément par son ID"""
        return await self.session.get(self.model, id)
    
    async def get_all(self) -> List[T]:
        """Récupère tous les éléments"""
        result = await self.session.execute(select(self.model))
        return list(result.scalars().all())
    
    async def create(self, **kwargs) -> T:
        """Crée un nouvel élément"""
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance
    
    async def delete(self, id: int) -> bool:
        """Supprime un élément par son ID"""
        instance = await self.get_by_id(id)
        if instance:
            await self.session.delete(instance)
            await self.session.commit()
            return True
        return False