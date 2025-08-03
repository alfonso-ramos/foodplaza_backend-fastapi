from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import models
from ..database import get_db
from ..models import Pedido, PedidoCreate, PedidoUpdate, PedidoItem, PedidoItemCreate

router = APIRouter(
    prefix="/pedidos",
    tags=['Pedidos']
)

# Obtener todos los pedidos (solo administradores o gerentes)
@router.get("/", response_model=List[Pedido])
def get_pedidos(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    estado: Optional[str] = None,
    local_id: Optional[int] = None,
    usuario_id: Optional[int] = None
):
    # Solo administradores o gerentes pueden ver todos los pedidos
    if current_user.rol not in ["administrador", "gerente"]:
        # Usuarios normales solo pueden ver sus propios pedidos
        if usuario_id and usuario_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para ver estos pedidos"
            )
        usuario_id = current_user.id
    
    query = db.query(models.PedidoDB)
    
    # Aplicar filtros
    if estado:
        query = query.filter(models.PedidoDB.estado_pedido == estado)
    if local_id:
        query = query.filter(models.PedidoDB.id_local == local_id)
    if usuario_id:
        query = query.filter(models.PedidoDB.id_usuario == usuario_id)
    
    pedidos = query.offset(skip).limit(limit).all()
    return pedidos

# Crear un nuevo pedido
@router.post("/", response_model=Pedido, status_code=status.HTTP_201_CREATED)
def crear_pedido(
    pedido: PedidoCreate,
    db: Session = Depends(get_db)
):
    # Iniciar una transacción
    try:
        # Verificar que el local existe
        db_local = db.query(models.LocaleDB).filter(models.LocaleDB.id == pedido.id_local).first()
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
        
        # Validar todos los productos
        for item in pedido.items:
            # Obtener el producto
            producto = db.query(models.ProductoDB).filter(
                models.ProductoDB.id == item.id_producto
            ).first()
            
            if not producto:
                raise HTTPException(
                    status_code=400,
                    detail=f"Producto con ID {item.id_producto} no encontrado"
                )
                
            if not producto.disponible:
                raise HTTPException(
                    status_code=400,
                    detail=f"El producto '{producto.nombre}' no está disponible actualmente"
                )
            
            # Validar que el precio no haya cambiado
            if float(item.precio_unitario) != float(producto.precio):
                raise HTTPException(
                    status_code=400,
                    detail=f"El precio del producto '{producto.nombre}' ha cambiado. Por favor, actualice su carrito."
                )
            
            # Calcular el total para este ítem
            total_por_item = float(item.precio_unitario) * item.cantidad
            total_pedido += total_por_item
            
            # Crear el ítem del pedido
            db_item = models.PedidoItemDB(
                id_producto=item.id_producto,
                cantidad=item.cantidad,
                precio_unitario=item.precio_unitario,
                instrucciones_especiales=item.instrucciones_especiales
            )
            items_pedido.append(db_item)
        
        # Calcular tiempo estimado de preparación (por defecto 30 minutos + 5 minutos por ítem)
        tiempo_estimado = 30 + (5 * len(items_pedido))
        
        # Crear el pedido
        db_pedido = models.PedidoDB(
            id_usuario=current_user.id,
            id_local=pedido.id_local,
            total_pedido=total_pedido,
            instrucciones_especiales=pedido.instrucciones_especiales,
            tiempo_preparacion_estimado=tiempo_estimado,
            items=items_pedido,
            estado_pedido='pendiente'  # Estado inicial del pedido
        )
        
        db.add(db_pedido)
        db.commit()
        db.refresh(db_pedido)
        
        return db_pedido
        
    except HTTPException as he:
        db.rollback()
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar el pedido: {str(e)}"
        )

# Obtener un pedido por ID
@router.get("/{pedido_id}", response_model=Pedido)
def obtener_pedido(
    pedido_id: int,
    db: Session = Depends(get_db)
):
    pedido = db.query(models.PedidoDB).filter(models.PedidoDB.id == pedido_id).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    # Solo el usuario que hizo el pedido, un administrador o el gerente del local pueden verlo
    if (current_user.rol not in ["administrador", "gerente"] and 
        pedido.id_usuario != current_user.id and 
        (hasattr(pedido.local, 'id_gerente') and pedido.local.id_gerente != current_user.id)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver este pedido"
        )
    
    return pedido

# Actualizar el estado de un pedido
@router.patch("/{pedido_id}", response_model=Pedido)
def actualizar_pedido(
    pedido_id: int,
    pedido_update: PedidoUpdate,
    db: Session = Depends(get_db)
):
    db_pedido = db.query(models.PedidoDB).filter(models.PedidoDB.id == pedido_id).first()
    
    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    # Solo el gerente del local o un administrador pueden actualizar el estado
    if current_user.rol not in ["administrador", "gerente"] or \
       (current_user.rol == "gerente" and hasattr(db_pedido.local, 'id_gerente') and db_pedido.local.id_gerente != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para actualizar este pedido"
        )
    
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

# Obtener pedidos de un usuario específico
@router.get("/usuario/{usuario_id}", response_model=List[Pedido])
def obtener_pedidos_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    estado: Optional[str] = None
):
    # Un usuario solo puede ver sus propios pedidos, a menos que sea administrador
    if current_user.id != usuario_id and current_user.rol != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes ver tus propios pedidos"
        )
    
    query = db.query(models.PedidoDB).filter(models.PedidoDB.id_usuario == usuario_id)
    
    if estado:
        query = query.filter(models.PedidoDB.estado_pedido == estado)
    
    pedidos = query.offset(skip).limit(limit).all()
    return pedidos

# Obtener pedidos de un local específico
@router.get("/local/{local_id}", response_model=List[Pedido])
def obtener_pedidos_local(
    local_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    estado: Optional[str] = None
):
    # Verificar que el local existe
    db_local = db.query(models.LocaleDB).filter(models.LocaleDB.id == local_id).first()
    if not db_local:
        raise HTTPException(status_code=404, detail="Local no encontrado")
    
    # Solo el gerente del local o un administrador pueden ver los pedidos
    if current_user.rol not in ["administrador", "gerente"] or \
       (current_user.rol == "gerente" and hasattr(db_local, 'id_gerente') and db_local.id_gerente != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver los pedidos de este local"
        )
    
    query = db.query(models.PedidoDB).filter(models.PedidoDB.id_local == local_id)
    
    if estado:
        query = query.filter(models.PedidoDB.estado_pedido == estado)
    
    pedidos = query.offset(skip).limit(limit).all()
    return pedidos
