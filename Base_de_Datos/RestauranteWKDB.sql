-- Script para crear la base de datos completa

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS mydb;
USE mydb;

-- Tabla: address
CREATE TABLE IF NOT EXISTS address (
    Id_Address INT AUTO_INCREMENT PRIMARY KEY,
    Address VARCHAR(255) NOT NULL,
    Zip_Code VARCHAR(20),
    State VARCHAR(100),
    Country VARCHAR(100),
    City VARCHAR(100)
);

-- Tabla: usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    Id_Usuario INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_Usuario VARCHAR(45) NOT NULL,
    Apellido_Usuario VARCHAR(45) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Telefono VARCHAR(25) UNIQUE,
    Hash_Contrasena_Usuario VARCHAR(255),
    Fecha_Ingresada DATETIME,
    MetodoDePago VARCHAR(45),
    Id_Address INT,
    FOREIGN KEY (Id_Address) REFERENCES address(Id_Address)
);

-- Tabla: alembic_version
CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(32) NOT NULL PRIMARY KEY
);

-- Tabla: menu_objetos
CREATE TABLE IF NOT EXISTS menu_objetos (
    Id_Objeto INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_Objeto VARCHAR(100) NOT NULL UNIQUE,
    Precio FLOAT,
    Categoria VARCHAR(45) NOT NULL,
    Calorias INT,
    Imagen_URL VARCHAR(255)
);

-- Tabla: puntos_balance
CREATE TABLE IF NOT EXISTS puntos_balance (
    Id_Usuario INT NOT NULL PRIMARY KEY,
    Puntos_Total INT NOT NULL,
    Redimidos_Total INT NOT NULL,
    Actualizado_En TIMESTAMP NOT NULL,
    FOREIGN KEY (Id_Usuario) REFERENCES usuarios(Id_Usuario)
);

-- Tabla: cart (opcional para carrito de compras)
CREATE TABLE IF NOT EXISTS cart (
    Id_Cart INT AUTO_INCREMENT PRIMARY KEY,
    Id_Usuario INT NOT NULL,
    Id_Objeto INT NOT NULL,
    Cantidad INT NOT NULL DEFAULT 1,
    Agregado_En TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Id_Usuario) REFERENCES usuarios(Id_Usuario),
    FOREIGN KEY (Id_Objeto) REFERENCES menu_objetos(Id_Objeto)
);

-- Insertar datos iniciales en menu_objetos
INSERT INTO menu_objetos (Nombre_Objeto, Precio, Categoria, Calorias, Imagen_URL) VALUES
('Big Burger', 12.99, 'burgers', 800, '/static/image/big_burger.jpg'),
('Chicken Wing', 8.99, 'chicken', 600, '/static/image/chicken_wing.jpg'),
('Lemonade', 3.99, 'drinks', 150, '/static/image/lemonade.jpg'),
('Nuggets', 6.99, 'chicken', 400, '/static/image/nuggets.png'),
('Small Burger', 9.99, 'burgers', 500, '/static/image/small_burger.png'),
('Soda Drink', 2.99, 'drinks', 200, '/static/image/soda_drink.jpg'),
('Sundae', 4.99, 'desserts', 300, '/static/image/sundae.jpg');

