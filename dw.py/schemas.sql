ORACLE_USER="C##diego_cordova"
ORACLE_DSN="10.50.1.0/xe"
ORACLE_PASSWORD="Inacap#2025"

CREATE TABLE MASCOTAS (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(64),
    edad Number(2),
    especie VARCHAR(32)
);

CREATE TABLE PERROS (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(64),
    edad Number(2),
    especie VARCHAR(32),
    vacunas_aplicada VARCHAR(100)
);

CREATE TABLE GATOS (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(64),
    edad Number(2),
    especie VARCHAR(32),
    fecha_esterilizacion VARCHAR(100)
);

CREATE TABLE AVES (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(64),
    edad Number(2),
    especie VARCHAR(32),
    control_vuelo VARCHAR(100),
    tipo_jaula VARCHAR(100)
);
