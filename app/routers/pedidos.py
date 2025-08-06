from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..models import PedidoDB, PedidoItemDB, ProductoDB, LocaleDB
from ..schemas.pedidos import Pedido, PedidoCreate, PedidoUpdate, PedidoItemCreate

router = APIRouter(
    prefix="/pedidos",
    tags=['Pedidos'],
    responses={404: {"description": "No encontrado"}},
)

@router.get("/", response_model=List[Pedido])
def get_pedidos(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    estado: Optional[str] = None,
    local_id: Optional[int] = None,
    usuario_id: Optional[int] = None
):
    """
    Obtiene una lista de pedidos con opciones de filtrado.
    """
    query = db.query(PedidoDB)
    
    # Aplicar filtros
    if estado:
        query = query.filter(PedidoDB.estado_pedido == estado)
    if local_id:
        query = query.filter(PedidoDB.id_local == local_id)
    if usuario_id is not None:
        query = query.filter(PedidoDB.id_usuario == usuario_id)
    
    pedidos = query.offset(skip).limit(limit).all()
    return pedidos

@router.post("/", response_model=Pedido, status_code=status.HTTP_201_CREATED)
def crear_pedido(
    pedido: PedidoCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo pedido.
    """
    # Verificar que el local existe
    db_local = db.query(LocaleDB).filter(LocaleDB.id == pedido.id_local).first()
    if not db_local:
        raise HTTPException(status_code=404, detail="Local no encontrado")
    
    # Verificar que hay al menos un ítem en el pedido
    if not pedido.items or len(pedido.items) == 0:
        raise HTTPException(
            status_code=400,
            detail="El pedido debe contener al menos un producto"
        )
    
    # Verificar que los productos existen y están disponibles
    total_pedido = 0
    items_pedido = []
    
    try:
        # Validar todos los productos
        for item in pedido.items:
            # Obtener el producto
            producto = db.query(ProductoDB).filter(
                ProductoDB.id == item.id_producto
            ).first()
            
            if not producto:
                raise HTTPException(
                    status_code=400,
                    detail=f"Producto con ID {item.id_producto} no encontrado"
                )
                
            if not producto.disponible:
                raise HTTPException(
                    status_code=400,
                    detail=f"El producto '{producto.nombre}' no está disponible"
                )
            
            # Calcular el total para este ítem
            total_por_item = float(producto.precio) * item.cantidad
            total_pedido += total_por_item
            
            # Crear el ítem del pedido
            db_item = PedidoItemDB(
                id_producto=item.id_producto,
                cantidad=item.cantidad,
                precio_unitario=producto.precio,  # Usar el precio actual del producto
                instrucciones_especiales=item.instrucciones_especiales
            )
            items_pedido.append(db_item)
        
        # Calcular tiempo estimado de preparación
        tiempo_estimado = 30 + (5 * len(items_pedido))
        
        # Crear el pedido (usando un ID de usuario fijo para pruebas)
        db_pedido = PedidoDB(
            id_usuario=1,  # TODO: Reemplazar con el ID del usuario autenticado
            id_local=pedido.id_local,
            total_pedido=total_pedido,
            instrucciones_especiales=pedido.instrucciones_especiales,
            tiempo_preparacion_estimado=tiempo_estimado,
            items=items_pedido,
            estado_pedido='pendiente'
        )
        
        db.add(db_pedido)
        db.commit()
        db.refresh(db_pedido)
        
        return db_pedido
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar el pedido: {str(e)}"
        )

@router.get("/{pedido_id}", response_model=Pedido)
def obtener_pedido(
    pedido_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene un pedido por su ID.
    """
    pedido = db.query(PedidoDB).filter(PedidoDB.id == pedido_id).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    # TODO: Agregar lógica de autenticación y autorización
    
    return pedido

@router.patch("/{pedido_id}", response_model=Pedido)
def actualizar_pedido(
    pedido_id: int,
    pedido_update: PedidoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza el estado de un pedido existente.
    """
    db_pedido = db.query(PedidoDB).filter(PedidoDB.id == pedido_id).first()
    
    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    # TODO: Agregar lógica de autenticación y autorización
    
    # Actualizar campos
    if pedido_update.estado_pedido:
        db_pedido.estado_pedido = pedido_update.estado_pedido
    if pedido_update.instrucciones_especiales is not None:
        db_pedido.instrucciones_especiales = pedido_update.instrucciones_especiales
    if pedido_update.tiempo_preparacion_estimado is not None:
        db_pedido.tiempo_preparacion_estimado = pedido_update.tiempo_preparacion_estimado
    
    db.commit()
    db.refresh(db_pedido)
    
    return db_pedido

@router.get("/usuario/{usuario_id}", response_model=List[Pedido])
def obtener_pedidos_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    estado: Optional[str] = None
):
    """
    Obtiene los pedidos de un usuario específico.
    """
    # TODO: Agregar verificación de autenticación
    
    query = db.query(PedidoDB).filter(PedidoDB.id_usuario == usuario_id)
    
    if estado:
        query = query.filter(PedidoDB.estado_pedido == estado)
    
    pedidos = query.offset(skip).limit(limit).all()
    return pedidos

@router.get("/local/{local_id}", response_model=List[Pedido])
def obtener_pedidos_local(
    local_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    estado: Optional[str] = None
):
    """
    Obtiene los pedidos de un local específico.
    """
    # Verificar que el local existe
    db_local = db.query(LocaleDB).filter(LocaleDB.id == local_id).first()
    if not db_local:
        raise HTTPException(status_code=404, detail="Local no encontrado")
    
    # TODO: Agregar verificación de autorización
    
    query = db.query(PedidoDB).filter(PedidoDB.id_local == local_id)
    
    if estado:
        query = query.filter(PedidoDB.estado_pedido == estado)
    
    pedidos = query.offset(skip).limit(limit).all()
    return pedidos
