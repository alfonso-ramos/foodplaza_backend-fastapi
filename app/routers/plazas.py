from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models import Plaza, PlazaCreate
from app.crud.plazas import (
    get_plaza,
    get_plazas,
    create_plaza,
    update_plaza as crud_update_plaza,
    delete_plaza as crud_delete_plaza
)

router = APIRouter(prefix="", tags=["plazas"])

@router.get("/{plaza_id}", response_model=Plaza)
def read_plaza(plaza_id: int, db: Session = Depends(get_db)):
    db_plaza = get_plaza(db, plaza_id=plaza_id)
    if db_plaza is None:
        raise HTTPException(status_code=404, detail="Plaza no encontrada")
    return db_plaza

@router.get("/", response_model=List[Plaza])
def read_plazas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_plazas(db, skip=skip, limit=limit)

@router.post("/", response_model=Plaza, status_code=status.HTTP_201_CREATED)
def create_new_plaza(plaza: PlazaCreate, db: Session = Depends(get_db)):
    return create_plaza(db=db, plaza=plaza)

@router.put("/{plaza_id}", response_model=Plaza)
def update_plaza(plaza_id: int, plaza: PlazaCreate, db: Session = Depends(get_db)):
    db_plaza = crud_update_plaza(db, plaza_id=plaza_id, plaza_data=plaza.dict(exclude_unset=True))
    if db_plaza is None:
        raise HTTPException(status_code=404, detail="Plaza no encontrada")
    return db_plaza

@router.delete("/{plaza_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plaza(plaza_id: int, db: Session = Depends(get_db)):
    success = crud_delete_plaza(db, plaza_id=plaza_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plaza no encontrada")
    return None
