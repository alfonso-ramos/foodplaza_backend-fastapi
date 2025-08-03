create database poobdd_ponchov;
drop database poobdd_ponchov;
use poobdd_ponchov;
show tables from poobdd_ponchov;

DELIMITER $$

CREATE TABLE plazas (
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nombre varchar(255) NOT NULL,
  direccion varchar(255) NOT NULL,
  estado enum('activo','inactivo') NOT NULL DEFAULT 'activo'
);

CREATE TABLE tipos_comercio (
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nombre_tipo varchar(50) NOT NULL,
  UNIQUE KEY nombre_tipo (nombre_tipo)
);

CREATE TABLE usuarios (
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nombre varchar(100) NOT NULL,
  password varchar(255) NOT NULL,
  rol enum('usuario','gerente','administrador') NOT NULL DEFAULT 'usuario',
  estado enum('activo','inactivo') NOT NULL DEFAULT 'activo'
);

CREATE TABLE telefonos_usuario (
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  id_usuario int NOT NULL,
  telefono varchar(20) NOT NULL,
  FOREIGN KEY (id_usuario) REFERENCES usuarios (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE correos_usuario (
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  id_usuario int NOT NULL,
  email varchar(100) NOT NULL,
  UNIQUE KEY email (email),
  FOREIGN KEY (id_usuario) REFERENCES usuarios (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE locales (
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nombre varchar(100) NOT NULL,
  id_tipo_comercio int DEFAULT NULL,
  direccion varchar(255) NOT NULL,
  horario_apertura time NOT NULL,
  horario_cierre time NOT NULL,
  estado enum('activo','inactivo') NOT NULL DEFAULT 'activo',
  fecha_registro datetime DEFAULT CURRENT_TIMESTAMP,
  gerente_id int DEFAULT NULL,
  id_plaza int DEFAULT NULL,
  FOREIGN KEY (gerente_id) REFERENCES usuarios (id) ON DELETE SET NULL ON UPDATE CASCADE,
  FOREIGN KEY (id_plaza) REFERENCES plazas (id) ON DELETE SET NULL ON UPDATE CASCADE,
  FOREIGN KEY (id_tipo_comercio) REFERENCES tipos_comercio (id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE telefonos_local (
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  id_local int NOT NULL,
  telefono varchar(20) NOT NULL,
  FOREIGN KEY (id_local) REFERENCES locales (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE menus (
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  id_local int NOT NULL,
  nombre_menu varchar(100) NOT NULL,
  descripcion varchar(255) DEFAULT NULL,
  FOREIGN KEY (id_local) REFERENCES locales (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE productos (
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nombre varchar(100) NOT NULL,
  descripcion text,
  precio decimal(10,2) NOT NULL,
  id_menu int NOT NULL,
  disponible tinyint(1) NOT NULL,
  categoria varchar(50) DEFAULT NULL,
  FOREIGN KEY (id_menu) REFERENCES menus (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE estados_pedido (
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nombre_estado varchar(50) NOT NULL,
  UNIQUE KEY nombre_estado (nombre_estado)
);

CREATE TABLE metodos_pago (
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nombre_metodo varchar(100) NOT NULL,
  UNIQUE KEY nombre_metodo (nombre_metodo)
);

CREATE TABLE pedidos (
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  id_usuario int NOT NULL,
  id_local int NOT NULL,
  fecha_pedido datetime DEFAULT CURRENT_TIMESTAMP,
  estado_pedido enum('pendiente','en_preparacion','listo_para_recoger','completado','cancelado') NOT NULL DEFAULT 'pendiente',
  total_pedido decimal(10,2) NOT NULL,
  instrucciones_especiales text,
  tiempo_preparacion_estimado int NOT NULL,
  FOREIGN KEY (id_usuario) REFERENCES usuarios (id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (id_local) REFERENCES locales (id) ON DELETE CASCADE ON UPDATE CASCADE,
);


CREATE TABLE pagos (
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  id_pedido int NOT NULL,
  id_metodo_pago int NOT NULL,
  monto decimal(10,2) NOT NULL,
  fecha_pago datetime DEFAULT CURRENT_TIMESTAMP,
  transaction_id varchar(100) DEFAULT NULL,
  UNIQUE KEY transaction_id (transaction_id),
  FOREIGN KEY (id_pedido) REFERENCES pedidos (id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (id_metodo_pago) REFERENCES metodos_pago (id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS auditoria_usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    accion VARCHAR(10) NOT NULL,
    detalles_cambio TEXT,
    fecha DATETIME NOT NULL,
    usuario_modificador VARCHAR(100),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS auditoria_locales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    local_id INT NOT NULL,
    accion VARCHAR(20) NOT NULL,
    detalles TEXT,
    fecha DATETIME NOT NULL,
    FOREIGN KEY (local_id) REFERENCES locales(id)
);

CREATE TABLE IF NOT EXISTS auditoria_plazas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plaza_id INT NOT NULL,
    campo_modificado VARCHAR(50),
    valor_anterior VARCHAR(255),
    valor_nuevo VARCHAR(255),
    fecha DATETIME NOT NULL,
    FOREIGN KEY (plaza_id) REFERENCES plazas(id)
);

CREATE TABLE IF NOT EXISTS historico_precios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    precio_anterior DECIMAL(10,2) NOT NULL,
    precio_nuevo DECIMAL(10,2) NOT NULL,
    fecha_cambio DATETIME NOT NULL,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

CREATE TABLE IF NOT EXISTS historico_disponibilidad (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    disponible_anterior BOOLEAN NOT NULL,
    disponible_nuevo BOOLEAN NOT NULL,
    fecha_cambio DATETIME NOT NULL,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

INSERT INTO usuarios (nombre, password, rol, estado)
VALUES
('Administrador', 'admin123', 'administrador', 'activo'),
('Gerente General', 'gerente123', 'gerente', 'activo'),
('Cliente Ejemplo', 'cliente123', 'usuario', 'activo');

INSERT INTO correos_usuario (id_usuario, email)
VALUES
(1, 'admin@plaza.com'),
(2, 'gerente@plaza.com'),
(3, 'cliente@ejemplo.com');

INSERT INTO telefonos_usuario (id_usuario, telefono)
VALUES
(1, '5551234567'),
(2, '5557654321'),
(3, '5559876543');

INSERT INTO plazas (nombre, direccion, estado)
VALUES
('Plaza Central', 'Av. Principal 123', 'activo'),
('Plaza Norte', 'Calle Secundaria 456', 'activo');

INSERT INTO tipos_comercio (nombre_tipo)
VALUES
('Restaurante'),
('Cafetería'),
('Comida Rápida');

INSERT INTO metodos_pago (nombre_metodo)
VALUES
('Efectivo'),
('Tarjeta de Crédito'),
('Tarjeta de Débito');

INSERT INTO estados_pedido (nombre_estado)
VALUES
('Pendiente'),
('En preparación'),
('Listo para recoger'),
('Completado'),
('Cancelado');

CREATE PROCEDURE sp_login_usuario(IN p_email VARCHAR(100), IN p_password VARCHAR(100))
BEGIN
    SELECT u.* FROM usuarios u JOIN correos_usuario cu ON u.id = cu.id_usuario WHERE cu.email = p_email AND u.password = p_password AND u.estado = 'activo';
END $$

CREATE PROCEDURE sp_registrar_usuario(
    IN p_nombre VARCHAR(100),
    IN p_email VARCHAR(100),
    IN p_password VARCHAR(100)
)
BEGIN
    DECLARE new_user_id INT;
    INSERT INTO usuarios (nombre, password, rol, estado)
    VALUES (p_nombre, p_password, 'usuario', 'activo');
    SET new_user_id = LAST_INSERT_ID();
    INSERT INTO correos_usuario (id_usuario, email)
    VALUES (new_user_id, p_email);
END $$

CREATE PROCEDURE sp_actualizar_usuario(
    IN p_id INT,
    IN p_nombre VARCHAR(100),
    IN p_email VARCHAR(100),
    IN p_telefono VARCHAR(20),
    IN p_estado ENUM('activo', 'inactivo')
)
BEGIN
    UPDATE usuarios
    SET nombre = p_nombre,
        estado = p_estado
    WHERE id = p_id;

    UPDATE correos_usuario
    SET email = p_email
    WHERE id_usuario = p_id;

    UPDATE telefonos_usuario
    SET telefono = p_telefono
    WHERE id_usuario = p_id;
END $$

CREATE PROCEDURE sp_buscar_usuario_por_id(IN p_id INT)
BEGIN
    SELECT u.*, cu.email, tu.telefono
    FROM usuarios u
    LEFT JOIN correos_usuario cu ON u.id = cu.id_usuario
    LEFT JOIN telefonos_usuario tu ON u.id = tu.id_usuario
    WHERE u.id = p_id;
END $$

CREATE PROCEDURE sp_listar_usuarios_por_rol(IN p_rol ENUM('usuario','gerente','administrador'))
BEGIN
    SELECT u.*, cu.email, tu.telefono
    FROM usuarios u
    LEFT JOIN correos_usuario cu ON u.id = cu.id_usuario
    LEFT JOIN telefonos_usuario tu ON u.id = tu.id_usuario
    WHERE u.rol = p_rol;
END $$

CREATE PROCEDURE sp_eliminar_usuario(IN p_id INT)
BEGIN
    UPDATE usuarios SET estado = 'inactivo' WHERE id = p_id;
END $$

CREATE PROCEDURE sp_verificar_email_existente(IN p_email VARCHAR(100))
BEGIN
    SELECT COUNT(*) AS existe FROM correos_usuario WHERE email = p_email;
END $$

CREATE PROCEDURE sp_cambiar_estado_usuario(IN p_id INT, IN p_estado ENUM('activo', 'inactivo'))
BEGIN
    UPDATE usuarios SET estado = p_estado WHERE id = p_id;
END $$

CREATE PROCEDURE sp_listar_locales()
BEGIN
    SELECT l.*, tc.nombre_tipo AS tipo_comercio_nombre, tl.telefono
    FROM locales l
    LEFT JOIN tipos_comercio tc ON l.id_tipo_comercio = tc.id
    LEFT JOIN telefonos_local tl ON l.id = tl.id_local
    ORDER BY l.id;
END $$

CREATE PROCEDURE sp_agregar_local(
    IN p_nombre VARCHAR(100),
    IN p_id_tipo_comercio INT,
    IN p_direccion VARCHAR(200),
    IN p_telefono VARCHAR(20),
    IN p_horario_apertura TIME,
    IN p_horario_cierre TIME,
    IN p_estado ENUM('activo', 'inactivo'),
    IN p_id_plaza INT
)
BEGIN
    DECLARE new_local_id INT;
    INSERT INTO locales(nombre, id_tipo_comercio, direccion,
                        horario_apertura, horario_cierre, estado, id_plaza)
    VALUES (p_nombre, p_id_tipo_comercio, p_direccion,
           p_horario_apertura, p_horario_cierre, p_estado, p_id_plaza);
    SET new_local_id = LAST_INSERT_ID();
    INSERT INTO telefonos_local (id_local, telefono) VALUES (new_local_id, p_telefono);
END $$

CREATE PROCEDURE sp_obtener_locales_por_plaza(IN p_id_plaza INT)
BEGIN
    SELECT l.*, tc.nombre_tipo AS tipo_comercio_nombre, tl.telefono
    FROM locales l
    LEFT JOIN tipos_comercio tc ON l.id_tipo_comercio = tc.id
    LEFT JOIN telefonos_local tl ON l.id = tl.id_local
    WHERE l.id_plaza = p_id_plaza;
END $$

CREATE PROCEDURE sp_obtener_local_por_id(IN p_id INT)
BEGIN
    SELECT l.*, tc.nombre_tipo AS tipo_comercio_nombre, tl.telefono
    FROM locales l
    LEFT JOIN tipos_comercio tc ON l.id_tipo_comercio = tc.id
    LEFT JOIN telefonos_local tl ON l.id = tl.id_local
    WHERE l.id = p_id;
END $$

CREATE PROCEDURE sp_asignar_gerente(IN p_id_local INT, IN p_id_gerente INT)
BEGIN
    UPDATE locales SET gerente_id = p_id_gerente WHERE id = p_id_local;
END $$

CREATE PROCEDURE sp_modificar_local(
    IN p_id INT,
    IN p_nombre VARCHAR(100),
    IN p_id_tipo_comercio INT,
    IN p_direccion VARCHAR(200),
    IN p_telefono VARCHAR(20),
    IN p_horario_apertura TIME,
    IN p_horario_cierre TIME,
    IN p_estado ENUM('activo', 'inactivo'),
    IN p_id_plaza INT
)
BEGIN
    UPDATE locales
    SET nombre = p_nombre,
        id_tipo_comercio = p_id_tipo_comercio,
        direccion = p_direccion,
        horario_apertura = p_horario_apertura,
        horario_cierre = p_horario_cierre,
        estado = p_estado,
        id_plaza = p_id_plaza
    WHERE id = p_id;

    UPDATE telefonos_local
    SET telefono = p_telefono
    WHERE id_local = p_id;
END $$

CREATE PROCEDURE sp_eliminar_local(IN p_id INT)
BEGIN
    UPDATE locales SET estado = 'inactivo' WHERE id = p_id;
END $$

CREATE PROCEDURE sp_obtener_locales_por_estado(IN p_estado ENUM('activo', 'inactivo'))
BEGIN
    SELECT l.*, tc.nombre_tipo AS tipo_comercio_nombre, tl.telefono
    FROM locales l
    LEFT JOIN tipos_comercio tc ON l.id_tipo_comercio = tc.id
    LEFT JOIN telefonos_local tl ON l.id = tl.id_local
    WHERE l.estado = p_estado ORDER BY nombre;
END $$

CREATE PROCEDURE sp_buscar_locales_por_nombre(IN p_nombre VARCHAR(100))
BEGIN
    SELECT l.*, tc.nombre_tipo AS tipo_comercio_nombre, tl.telefono
    FROM locales l
    LEFT JOIN tipos_comercio tc ON l.id_tipo_comercio = tc.id
    LEFT JOIN telefonos_local tl ON l.id = tl.id_local
    WHERE l.nombre LIKE CONCAT('%', p_nombre, '%') ORDER BY nombre;
END $$

CREATE PROCEDURE sp_agregar_plaza(
    IN p_nombre VARCHAR(100),
    IN p_direccion VARCHAR(200),
    IN p_estado ENUM('activo', 'inactivo')
)
BEGIN
    INSERT INTO plazas(nombre, direccion, estado)
    VALUES (p_nombre, p_direccion, p_estado);
END $$

CREATE PROCEDURE sp_obtener_plaza_por_id(IN p_id INT)
BEGIN
    SELECT * FROM plazas WHERE id = p_id;
END $$

CREATE PROCEDURE sp_modificar_plaza(
    IN p_id INT,
    IN p_nombre VARCHAR(100),
    IN p_direccion VARCHAR(200),
    IN p_estado ENUM('activo', 'inactivo')
)
BEGIN
    UPDATE plazas
    SET nombre = p_nombre,
        direccion = p_direccion,
        estado = p_estado
    WHERE id = p_id;
END $$

CREATE PROCEDURE sp_eliminar_plaza(IN p_id INT)
BEGIN
    UPDATE plazas SET estado = 'inactivo' WHERE id = p_id;
END $$

CREATE PROCEDURE sp_listar_productos()
BEGIN
    SELECT * FROM productos ORDER BY id;
END $$

CREATE PROCEDURE sp_modificar_producto(
    IN p_id INT,
    IN p_nombre VARCHAR(100),
    IN p_descripcion TEXT,
    IN p_precio DECIMAL(10,2),
    IN p_id_menu INT,
    IN p_disponible BOOLEAN,
    IN p_categoria VARCHAR(50)
)
BEGIN
    UPDATE productos
    SET nombre = p_nombre,
        descripcion = p_descripcion,
        precio = p_precio,
        id_menu = p_id_menu,
        disponible = p_disponible,
        categoria = p_categoria
    WHERE id = p_id;
END $$

CREATE PROCEDURE sp_obtener_producto_por_id(IN p_id INT)
BEGIN
    SELECT * FROM productos WHERE id = p_id;
END $$

CREATE PROCEDURE sp_agregar_producto(
    IN p_nombre VARCHAR(100),
    IN p_descripcion TEXT,
    IN p_precio DECIMAL(10,2),
    IN p_id_menu INT,
    IN p_disponible BOOLEAN,
    IN p_categoria VARCHAR(50)
)
BEGIN
    INSERT INTO productos(nombre, descripcion, precio, id_menu, disponible, categoria)
    VALUES (p_nombre, p_descripcion, p_precio, p_id_menu, p_disponible, p_categoria);
END $$

CREATE PROCEDURE sp_eliminar_producto(IN p_id INT)
BEGIN
    DELETE FROM productos WHERE id = p_id;
END $$

CREATE PROCEDURE sp_obtener_productos_por_categoria(IN p_categoria VARCHAR(50))
BEGIN
    SELECT * FROM productos WHERE categoria = p_categoria AND disponible = TRUE ORDER BY nombre;
END $$

CREATE PROCEDURE sp_obtener_productos_por_precio(
    IN p_precio_min DECIMAL(10,2),
    IN p_precio_max DECIMAL(10,2)
)
BEGIN
    SELECT * FROM productos
    WHERE precio BETWEEN p_precio_min AND p_precio_max
    AND disponible = TRUE
    ORDER BY precio;
END $$

CREATE PROCEDURE sp_obtener_menus_por_local(IN p_id_local INT)
BEGIN
    SELECT * FROM menus WHERE id_local = p_id_local ORDER BY id;
END $$

CREATE PROCEDURE sp_listar_menus()
BEGIN
    SELECT * FROM menus ORDER BY id;
END $$

CREATE PROCEDURE sp_obtener_menu_por_id(IN p_id INT)
BEGIN
    SELECT * FROM menus WHERE id = p_id;
END $$

CREATE PROCEDURE sp_agregar_menu(
    IN p_id_local INT,
    IN p_nombre_menu VARCHAR(100),
    IN p_descripcion TEXT
)
BEGIN
    INSERT INTO menus (id_local, nombre_menu, descripcion)
    VALUES (p_id_local, p_nombre_menu, p_descripcion);
END $$

CREATE PROCEDURE sp_modificar_menu(
    IN p_id INT,
    IN p_id_local INT,
    IN p_nombre_menu VARCHAR(100),
    IN p_descripcion TEXT
)
BEGIN
    UPDATE menus
    SET id_local = p_id_local,
        nombre_menu = p_nombre_menu,
        descripcion = p_descripcion
    WHERE id = p_id;
END $$

CREATE PROCEDURE sp_eliminar_menu(IN p_id INT)
BEGIN
    DELETE FROM menus WHERE id = p_id;
END $$

CREATE TRIGGER tr_auditoria_usuarios_insert
AFTER INSERT ON usuarios
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_usuarios(usuario_id, accion, detalles_cambio, fecha)
    VALUES (NEW.id, 'INSERT',
            CONCAT('Usuario insertado. ID: ', NEW.id, ', Nombre: ', NEW.nombre, ', Rol: ', NEW.rol),
            NOW());
END $$

CREATE TRIGGER tr_auditoria_usuarios_update
AFTER UPDATE ON usuarios
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_usuarios(usuario_id, accion, detalles_cambio, fecha)
    VALUES (NEW.id, 'UPDATE',
            CONCAT('Usuario actualizado. ID: ', NEW.id, '. Nombre: ', OLD.nombre, ' -> ', NEW.nombre,
                   ', Rol: ', OLD.rol, ' -> ', NEW.rol, ', Estado: ', OLD.estado, ' -> ', NEW.estado),
            NOW());
END $$

CREATE TRIGGER tr_auditoria_usuarios_delete
AFTER DELETE ON usuarios
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_usuarios(usuario_id, accion, detalles_cambio, fecha)
    VALUES (OLD.id, 'DELETE',
            CONCAT('Usuario eliminado. ID: ', OLD.id, ', Nombre: ', OLD.nombre, ', Rol: ', OLD.rol),
            NOW());
END $$

CREATE TRIGGER tr_validar_email_usuario_insert
BEFORE INSERT ON correos_usuario
FOR EACH ROW
BEGIN
    IF NEW.email NOT LIKE '%@%' OR NEW.email NOT LIKE '%@%.%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Email debe contener @ y un dominio válido.';
    END IF;
END $$

CREATE TRIGGER tr_validar_email_usuario_update
BEFORE UPDATE ON correos_usuario
FOR EACH ROW
BEGIN
    IF NEW.email NOT LIKE '%@%' OR NEW.email NOT LIKE '%@%.%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Email debe contener @ y un dominio válido.';
    END IF;
END $$

CREATE TRIGGER tr_local_creado
AFTER INSERT ON locales
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_locales(local_id, accion, detalles, fecha)
    VALUES (NEW.id, 'CREACION',
           CONCAT('Local "', NEW.nombre, '" creado en plaza ', (SELECT nombre FROM plazas WHERE id = NEW.id_plaza)),
           NOW());
END $$

CREATE TRIGGER tr_locales_actualizacion
BEFORE UPDATE ON locales
FOR EACH ROW
BEGIN
    IF NEW.estado = 'inactivo' AND OLD.estado = 'activo' THEN
        INSERT INTO auditoria_locales(local_id, accion, detalles, fecha)
        VALUES (NEW.id, 'DESACTIVACION',
               CONCAT('Local "', NEW.nombre, '" desactivado'),
               NOW());
    END IF;
END $$

CREATE TRIGGER tr_plazas_auditoria
AFTER UPDATE ON plazas
FOR EACH ROW
BEGIN
    IF NEW.nombre != OLD.nombre THEN
        INSERT INTO auditoria_plazas(plaza_id, campo_modificado, valor_anterior, valor_nuevo, fecha)
        VALUES (NEW.id, 'nombre', OLD.nombre, NEW.nombre, NOW());
    END IF;

    IF NEW.direccion != OLD.direccion THEN
        INSERT INTO auditoria_plazas(plaza_id, campo_modificado, valor_anterior, valor_nuevo, fecha)
        VALUES (NEW.id, 'direccion', OLD.direccion, NEW.direccion, NOW());
    END IF;

    IF NEW.estado != OLD.estado THEN
        INSERT INTO auditoria_plazas(plaza_id, campo_modificado, valor_anterior, valor_nuevo, fecha)
        VALUES (NEW.id, 'estado', OLD.estado, NEW.estado, NOW());
    END IF;
END $$

CREATE TRIGGER tr_prevenir_eliminar_plaza
BEFORE DELETE ON plazas
FOR EACH ROW
BEGIN
    DECLARE locales_count INT;
    SELECT COUNT(*) INTO locales_count FROM locales WHERE id_plaza = OLD.id AND estado = 'activo';

    IF locales_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se puede eliminar la plaza porque tiene locales activos asociados';
    END IF;
END $$

CREATE TRIGGER tr_productos_precio
BEFORE UPDATE ON productos
FOR EACH ROW
BEGIN
    IF NEW.precio != OLD.precio THEN
        INSERT INTO historico_precios(producto_id, precio_anterior, precio_nuevo, fecha_cambio)
        VALUES (NEW.id, OLD.precio, NEW.precio, NOW());
    END IF;
END $$

CREATE TRIGGER tr_producto_modificado
BEFORE UPDATE ON productos
FOR EACH ROW
BEGIN
    IF NEW.disponible != OLD.disponible THEN
        INSERT INTO historico_disponibilidad(producto_id, disponible_anterior, disponible_nuevo, fecha_cambio)
        VALUES (NEW.id, OLD.disponible, NEW.disponible, NOW());
    END IF;
END $$

CREATE TRIGGER tr_validar_precio_producto_insert
BEFORE INSERT ON productos
FOR EACH ROW
BEGIN
    IF NEW.precio <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El precio debe ser mayor que cero';
    END IF;
END $$

CREATE TRIGGER tr_validar_precio_producto_update
BEFORE UPDATE ON productos
FOR EACH ROW
BEGIN
    IF NEW.precio <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El precio debe ser mayor que cero';
    END IF;
END $$

CREATE TRIGGER tr_menus_integridad
BEFORE DELETE ON menus
FOR EACH ROW
BEGIN
    DECLARE productos_count INT;
    SELECT COUNT(*) INTO productos_count FROM productos WHERE id_menu = OLD.id;

    IF productos_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se puede eliminar el menú porque tiene productos asociados';
    END IF;
END $$

CREATE TRIGGER tr_auditoria_menus_insert
AFTER INSERT ON menus
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_locales(local_id, accion, detalles, fecha)
    VALUES (NEW.id_local, 'MENU_CREADO',
           CONCAT('Menú "', NEW.nombre_menu, '" creado para el local'),
           NOW());
END $$

CREATE TRIGGER tr_auditoria_menus_update
AFTER UPDATE ON menus
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_locales(local_id, accion, detalles, fecha)
    VALUES (NEW.id_local, 'MENU_MODIFICADO',
           CONCAT('Menú "', OLD.nombre_menu, '" actualizado'),
           NOW());
END $$

CREATE TRIGGER tr_auditoria_menus_delete
AFTER DELETE ON menus
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_locales(local_id, accion, detalles, fecha)
    VALUES (OLD.id_local, 'MENU_ELIMINADO',
           CONCAT('Menú "', OLD.nombre_menu, '" eliminado'),
           NOW());
END $$

CREATE TRIGGER tr_prevenir_eliminar_local_con_menus
BEFORE DELETE ON locales
FOR EACH ROW
BEGIN
    DECLARE menus_count INT;
    SELECT COUNT(*) INTO menus_count FROM menus WHERE id_local = OLD.id;

    IF menus_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se puede eliminar el local porque tiene menús asociados';
    END IF;
END $$

CREATE TRIGGER tr_prevenir_eliminar_usuario_gerente
BEFORE DELETE ON usuarios
FOR EACH ROW
BEGIN
    DECLARE locales_count INT;
    SELECT COUNT(*) INTO locales_count FROM locales WHERE gerente_id = OLD.id AND estado = 'activo';

    IF locales_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se puede eliminar el usuario porque está asignado como gerente de locales activos';
    END IF;
END $$

CREATE USER 'admin_plaza'@'localhost' IDENTIFIED BY 'AdminSecurePass123!';
GRANT ALL PRIVILEGES ON plaza_db.* TO 'admin_plaza'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

CREATE USER 'gerente_plaza'@'localhost' IDENTIFIED BY 'GerenteSecurePass123!';
GRANT SELECT, INSERT, UPDATE ON plaza_db.locales TO 'gerente_plaza'@'localhost';
GRANT SELECT, INSERT, UPDATE ON plaza_db.productos TO 'gerente_plaza'@'localhost';
GRANT SELECT, INSERT, UPDATE ON plaza_db.menus TO 'gerente_plaza'@'localhost';
GRANT SELECT ON plaza_db.pedidos TO 'gerente_plaza'@'localhost';
GRANT SELECT ON plaza_db.detalle_pedidos TO 'gerente_plaza'@'localhost';
GRANT SELECT, INSERT, UPDATE ON plaza_db.telefonos_local TO 'gerente_plaza'@'localhost';
FLUSH PRIVILEGES;

CREATE USER 'cliente_plaza'@'localhost' IDENTIFIED BY 'ClienteSecurePass123!';
GRANT SELECT ON plaza_db.locales TO 'cliente_plaza'@'localhost';
GRANT SELECT ON plaza_db.productos TO 'cliente_plaza'@'localhost';
GRANT SELECT ON plaza_db.menus TO 'cliente_plaza'@'localhost';
GRANT SELECT, INSERT, UPDATE ON plaza_db.pedidos TO 'cliente_plaza'@'localhost';
GRANT SELECT, INSERT, UPDATE ON plaza_db.detalle_pedidos TO 'cliente_plaza'@'localhost';
GRANT SELECT ON plaza_db.estados_pedido TO 'cliente_plaza'@'localhost';
FLUSH PRIVILEGES;