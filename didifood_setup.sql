-- ================================================================
--  DidiFood — Script PostgreSQL v3
--  Total registros: 12001
--  TODOS los IDs son explícitos → sin huecos ni errores de FK
-- ================================================================
--  USO:
--    psql -U postgres -f didifood_setup.sql
--    (o desde psql:  \i ruta/didifood_setup.sql )
-- ================================================================

DROP DATABASE IF EXISTS didifood;
CREATE DATABASE didifood ENCODING 'UTF8' TEMPLATE template0;
\connect didifood

-- ================================================================
--  DDL — Tablas
-- ================================================================

CREATE TABLE usuarios (
    id_usuario            INT          PRIMARY KEY,
    nombre                VARCHAR(60)  NOT NULL,
    apellido_paterno      VARCHAR(60)  NOT NULL,
    apellido_materno      VARCHAR(60),
    telefono              VARCHAR(20),
    email                 VARCHAR(120) UNIQUE NOT NULL,
    direccion             TEXT,
    fecha_registro        TIMESTAMP,
    calificacion_promedio NUMERIC(3,1) DEFAULT 0.0
);

CREATE TABLE conductores (
    id_conductor          INT          PRIMARY KEY,
    nombre                VARCHAR(60)  NOT NULL,
    apellido_paterno      VARCHAR(60)  NOT NULL,
    apellido_materno      VARCHAR(60),
    telefono              VARCHAR(20),
    email                 VARCHAR(120) UNIQUE NOT NULL,
    tipo_vehiculo         VARCHAR(30),
    placa                 VARCHAR(15)  UNIQUE NOT NULL,
    calificacion_promedio NUMERIC(3,1) DEFAULT 0.0,
    estatus               VARCHAR(20)  DEFAULT 'Activo',
    fecha_ingreso         TIMESTAMP
);

CREATE TABLE restaurantes (
    id_restaurante        INT          PRIMARY KEY,
    nombre                VARCHAR(100) NOT NULL,
    categoria             VARCHAR(50),
    direccion             TEXT,
    ciudad                VARCHAR(60),
    estado                VARCHAR(60),
    telefono              VARCHAR(20),
    email                 VARCHAR(120),
    calificacion_promedio NUMERIC(3,1) DEFAULT 0.0,
    estatus               VARCHAR(20)  DEFAULT 'Activo'
);

CREATE TABLE productos (
    id_producto           INT          PRIMARY KEY,
    id_restaurante        INT          NOT NULL REFERENCES restaurantes(id_restaurante),
    nombre_producto       VARCHAR(100) NOT NULL,
    categoria_producto    VARCHAR(50),
    precio                NUMERIC(10,2) NOT NULL,
    disponibilidad        VARCHAR(20)  DEFAULT 'Disponible'
);

CREATE TABLE estatus_pedido (
    id_estatus            INT          PRIMARY KEY,
    estatus               VARCHAR(50)  NOT NULL,
    descripcion           TEXT
);
CREATE TABLE metodos_pago (
    id_metodo             INT          PRIMARY KEY,
    metodo                VARCHAR(50)  NOT NULL,
    descripcion           TEXT
);

CREATE TABLE pedidos (
    id_pedido             INT          PRIMARY KEY,
    id_usuario            INT          NOT NULL REFERENCES usuarios(id_usuario),
    id_restaurante        INT          NOT NULL REFERENCES restaurantes(id_restaurante),
    id_conductor          INT          REFERENCES conductores(id_conductor),
    id_estatus            INT          NOT NULL REFERENCES estatus_pedido(id_estatus),
    metodo_pago           INT          REFERENCES metodos_pago(id_metodo),
    fecha_pedido          TIMESTAMP    NOT NULL,
    hora_recogida         TIMESTAMP,
    hora_entrega          TIMESTAMP,
    subtotal              NUMERIC(10,2) NOT NULL DEFAULT 0,
    costo_envio           NUMERIC(10,2) NOT NULL DEFAULT 0,
    total                 NUMERIC(10,2) NOT NULL DEFAULT 0,
    tiempo_entrega_min    INT
);

CREATE TABLE detalle_pedido (
    id_detalle            INT          PRIMARY KEY,
    id_pedido             INT          NOT NULL REFERENCES pedidos(id_pedido),
    id_producto           INT          NOT NULL REFERENCES productos(id_producto),
    cantidad              INT          NOT NULL DEFAULT 1,
    precio_unitario       NUMERIC(10,2) NOT NULL,
    subtotal_linea        NUMERIC(10,2) NOT NULL
);

CREATE TABLE resenias_restaurante (
    id_resenia            INT          PRIMARY KEY,
    id_usuario            INT          NOT NULL REFERENCES usuarios(id_usuario),
    id_restaurante        INT          NOT NULL REFERENCES restaurantes(id_restaurante),
    calificacion          SMALLINT     CHECK (calificacion BETWEEN 1 AND 5),
    comentario            TEXT,
    fecha                 TIMESTAMP
);

CREATE TABLE resenias_conductor (
    id_resenia            INT          PRIMARY KEY,
    id_usuario            INT          NOT NULL REFERENCES usuarios(id_usuario),
    id_conductor          INT          NOT NULL REFERENCES conductores(id_conductor),
    calificacion          SMALLINT     CHECK (calificacion BETWEEN 1 AND 5),
    comentario            TEXT,
    fecha                 TIMESTAMP
);

CREATE TABLE estados_conductor (
    id_log                INT          PRIMARY KEY,
    id_conductor          INT          NOT NULL REFERENCES conductores(id_conductor),
    estado                VARCHAR(50)  NOT NULL,
    timestamp_registro    TIMESTAMP    NOT NULL
);

-- Índices
CREATE INDEX idx_ped_usr  ON pedidos(id_usuario);
CREATE INDEX idx_ped_rest ON pedidos(id_restaurante);
CREATE INDEX idx_ped_cond ON pedidos(id_conductor);
CREATE INDEX idx_ped_est  ON pedidos(id_estatus);
CREATE INDEX idx_ped_met  ON pedidos(metodo_pago);
CREATE INDEX idx_det_ped  ON detalle_pedido(id_pedido);
CREATE INDEX idx_rr_rest  ON resenias_restaurante(id_restaurante);
CREATE INDEX idx_rc_cond  ON resenias_conductor(id_conductor);
CREATE INDEX idx_ec_cond  ON estados_conductor(id_conductor);
CREATE INDEX idx_ec_estado ON estados_conductor(estado);

-- Fin del script — 12001 registros totales