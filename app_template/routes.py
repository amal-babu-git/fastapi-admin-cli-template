"""
API routes for the ${app_name} app.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.core.db import get_session
from .models import ${model_name}
from .schemas import ${model_name}Read, ${model_name}Create, ${model_name}Update
from .services import ${model_name}Service

router = APIRouter()
service = ${model_name}Service()


@router.get("/", response_model=List[${model_name}Read])
async def get_${app_name_lowercase}s(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    """Get list of ${app_name} items."""
    return await service.get_all(session=session, skip=skip, limit=limit)


@router.get("/{item_id}", response_model=${model_name}Read)
async def get_${app_name_lowercase}(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    """Get ${app_name} by ID."""
    item = await service.get_by_id(item_id=item_id, session=session)
    if item is None:
        raise HTTPException(status_code=404, detail="${model_name} not found")
    return item


@router.post("/", response_model=${model_name}Read, status_code=status.HTTP_201_CREATED)
async def create_${app_name_lowercase}(
    item: ${model_name}Create,
    session: AsyncSession = Depends(get_session)
):
    """Create new ${app_name}."""
    return await service.create(data=item, session=session)


@router.put("/{item_id}", response_model=${model_name}Read)
async def update_${app_name_lowercase}(
    item_id: uuid.UUID,
    item: ${model_name}Update,
    session: AsyncSession = Depends(get_session)
):
    """Update ${app_name} by ID."""
    updated_item = await service.update(item_id=item_id, data=item, session=session)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="${model_name} not found")
    return updated_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_${app_name_lowercase}(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    """Delete ${app_name} by ID."""
    deleted = await service.delete(item_id=item_id, session=session)
    if not deleted:
        raise HTTPException(status_code=404, detail="${model_name} not found")
    return None
