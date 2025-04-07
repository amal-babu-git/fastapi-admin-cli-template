"""
Service functions for the ${app_name} app.
"""
from typing import Optional, List, Any, Dict
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import uuid
import logging

from .models import ${model_name}
from .schemas import ${model_name}Create, ${model_name}Update, ${model_name}Read

logger = logging.getLogger(__name__)

class ${model_name}Service:
    """Service for managing ${model_name} operations."""
    
    async def get_all(self, 
                     session: AsyncSession,
                     skip: int = 0,
                     limit: int = 100,
                     ) -> List[${model_name}]:
        """
        Retrieve all items with pagination.
        
        Args:
            session: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of items
        """
        query = select(${model_name}).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, 
                       item_id: uuid.UUID,
                       session: AsyncSession
                       ) -> Optional[${model_name}]:
        """
        Retrieve an item by ID.
        
        Args:
            item_id: The item's unique ID
            session: Database session
            
        Returns:
            The item if found, None otherwise
        """
        query = select(${model_name}).where(${model_name}.id == item_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
    
    async def create(self, 
                    data: ${model_name}Create,
                    session: AsyncSession
                    ) -> ${model_name}:
        """
        Create a new item.
        
        Args:
            data: The item data
            session: Database session
            
        Returns:
            The created item
            
        Raises:
            SQLAlchemyError: If there's a database error
        """
        try:
            db_item = ${model_name}(**data.model_dump())
            session.add(db_item)
            await session.commit()
            await session.refresh(db_item)
            return db_item
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Error creating ${model_name}: {str(e)}")
            raise
    
    async def update(self, 
                    item_id: uuid.UUID,
                    data: ${model_name}Update,
                    session: AsyncSession
                    ) -> Optional[${model_name}]:
        """
        Update an existing item.
        
        Args:
            item_id: The item's unique ID
            data: The update data
            session: Database session
            
        Returns:
            The updated item if found, None otherwise
            
        Raises:
            SQLAlchemyError: If there's a database error
        """
        try:
            db_item = await self.get_by_id(item_id, session)
            if not db_item:
                return None
                
            # Update only fields that are provided
            update_data = data.model_dump(exclude_unset=True)
            
            for key, value in update_data.items():
                setattr(db_item, key, value)
            
            # Update the timestamp
            db_item.updated_at = datetime.utcnow()
                
            await session.commit()
            await session.refresh(db_item)
            return db_item
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Error updating ${model_name} {item_id}: {str(e)}")
            raise
    
    async def delete(self, 
                    item_id: uuid.UUID,
                    session: AsyncSession
                    ) -> bool:
        """
        Delete an item.
        
        Args:
            item_id: The item's unique ID
            session: Database session
            
        Returns:
            True if the item was deleted, False if it wasn't found
            
        Raises:
            SQLAlchemyError: If there's a database error
        """
        try:
            db_item = await self.get_by_id(item_id, session)
            if not db_item:
                return False
            
            await session.delete(db_item)
            await session.commit()
            return True
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Error deleting ${model_name} {item_id}: {str(e)}")
            raise
