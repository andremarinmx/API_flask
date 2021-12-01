CREATE DATABASE API_Cursos;
USE API_Cursos;
CREATE TABLE materias(
    codigo VARCHAR(6) NOT NULL PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL, 
    creditos INT
);
INSERT INTO materias(codigo, nombre, creditos) 
VALUES(
    "6", "Integradora", 8
)