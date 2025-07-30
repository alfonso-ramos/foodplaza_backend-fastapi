# Implementación de Gestión de Imágenes

## Estructura de Base de Datos
- [ ] Crear migración para la tabla `imagenes`
  ```sql
  CREATE TABLE imagenes (
      id SERIAL PRIMARY KEY,
      url VARCHAR(500) NOT NULL,
      tipo_entidad VARCHAR(20) NOT NULL,  -- 'plaza', 'local', 'producto', 'usuario'
      entidad_id INTEGER NOT NULL,
      es_principal BOOLEAN DEFAULT FALSE,
      orden INTEGER DEFAULT 0,
      fecha_subida TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      metadata JSONB,
      CONSTRAINT fk_entidad UNIQUE (tipo_entidad, entidad_id, es_principal) WHERE es_principal = TRUE
  );
  
  CREATE INDEX idx_imagenes_entidad ON imagenes(tipo_entidad, entidad_id);
  CREATE INDEX idx_imagenes_principal ON imagenes(tipo_entidad, entidad_id, es_principal);
  ```

## Modelos y Esquemas
- [ ] Crear modelo SQLAlchemy en `app/models/imagenes.py`
- [ ] Crear esquemas Pydantic en `app/schemas/imagenes.py`
- [ ] Actualizar `app/models/__init__.py` para exportar los nuevos modelos
- [ ] Actualizar `app/schemas/__init__.py` para exportar los nuevos esquemas

## Operaciones CRUD
- [ ] Implementar operaciones CRUD en `app/crud/imagenes.py`
  - Crear imagen
  - Obtener imágenes por entidad
  - Actualizar imagen (marcar como principal, cambiar orden)
  - Eliminar imagen
  - Obtener imagen principal

## Endpoints
- [ ] Crear router en `app/routers/imagenes.py` con los siguientes endpoints:
  - `POST /api/imagenes/` - Subir nueva imagen
  - `GET /api/imagenes/{tipo_entidad}/{entidad_id}` - Obtener imágenes de una entidad
  - `PUT /api/imagenes/{imagen_id}` - Actualizar imagen
  - `DELETE /api/imagenes/{imagen_id}` - Eliminar imagen
  - `GET /api/imagenes/{tipo_entidad}/{entidad_id}/principal` - Obtener imagen principal

## Configuración
- [ ] Configurar almacenamiento local en `app/core/config.py`
- [ ] Configurar servicio de almacenamiento en `app/services/storage.py`
- [ ] Actualizar `app/main.py` para servir archivos estáticos

## Documentación
- [ ] Actualizar documentación de la API
- [ ] Documentar los nuevos endpoints
- [ ] Agregar ejemplos de solicitud/respuesta

## Pruebas
- [ ] Crear pruebas unitarias
- [ ] Probar carga de imágenes
- [ ] Probar actualización/eliminación
- [ ] Probar validaciones

## Tareas Adicionales
- [ ] Implementar procesamiento de imágenes (redimensionamiento, optimización)
- [ ] Agregar soporte para almacenamiento en la nube (S3, Google Cloud Storage)
- [ ] Implementar límites de tamaño y tipos de archivo
- [ ] Agregar autenticación/autorización a los endpoints
- [ ] Configurar CDN para servir las imágenes

## Notas
- Las imágenes se almacenarán localmente en la carpeta `uploads/`
- Cada imagen estará asociada a una entidad específica (plaza, local, producto, usuario)
- Solo una imagen puede ser marcada como principal por entidad
- Los metadatos de la imagen (tamaño, dimensiones, etc.) se almacenarán en el campo `metadata`
