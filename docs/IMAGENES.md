# Manejo de Imágenes con Cloudinary

## Configuración Necesaria

1. Crear cuenta en [Cloudinary](https://cloudinary.com/)
2. Obtener credenciales:
   - Cloud name
   - API Key
   - API Secret


## Estructura de Carpetas

```
cloudinary://
└── foodplaza/
    ├── usuarios/
    ├── plazas/
    ├── locales/
    ├── menus/
    └── productos/
```

## Campos en Base de Datos

Para cada entidad que necesite imágenes, agregar:
- `imagen_url` (String, nullable)
- `imagen_public_id` (String, nullable) - ID de Cloudinary para gestión

## Endpoints

### Subir Imagen
```
POST /api/{entidad}/{id}/imagen
Content-Type: multipart/form-data
```

### Eliminar Imagen
```
DELETE /api/{entidad}/{id}/imagen
```

## Validaciones
- Tipos permitidos: jpg, jpeg, png, webp
- Tamaño máximo: 5MB
- Dimensiones máximas: 4000x4000px

## Variables de Entorno
```
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
```

## Flujo de Trabajo
1. Validar archivo en frontend
2. Subir a Cloudinary
3. Guardar URL en base de datos
4. Usar URL para mostrar imágenes

## Consideraciones
- Usar transformaciones de Cloudinary para optimización
- Implementar manejo de errores
- Considerar caché de imágenes
- Monitorear uso de la cuota gratuita
