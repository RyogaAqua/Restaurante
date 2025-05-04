-- MySQL Script-

-- -----------------------------------------------------
-- Set Session Variables
-- -----------------------------------------------------
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Address`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Address` (
  `Id_Address` INT NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for the address',
  `Address` VARCHAR(255) NOT NULL COMMENT 'Street address line(s)',
  `Zip_Code` VARCHAR(20) NULL COMMENT 'Postal or Zip code',
  `State` VARCHAR(100) NULL COMMENT 'State, Province, or Region',
  `Country` VARCHAR(100) NULL COMMENT 'Country',
  `City` VARCHAR(100) NULL COMMENT 'City or Town',
  PRIMARY KEY (`Id_Address`),
  UNIQUE INDEX `idx_unique_address` (`Address` ASC, `City` ASC, `State` ASC, `Zip_Code` ASC, `Country` ASC) VISIBLE)
ENGINE = InnoDB
COMMENT = 'Stores reusable address information, referenced by Users and Orders.';


-- -----------------------------------------------------
-- Table `mydb`.`Usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Usuarios` (
  `Id_Usuario` INT NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for the user',
  `Nombre_Usuario` VARCHAR(45) NOT NULL COMMENT 'User''s first name',
  `Apellido_Usuario` VARCHAR(45) NOT NULL COMMENT 'User''s last name',
  `Email` VARCHAR(100) NOT NULL COMMENT 'User''s email address (must be unique)',
  `Telefono` VARCHAR(25) NULL COMMENT 'User''s phone number (must be unique if provided)',
  `Hash_Contrasena_Usuario` VARCHAR(255) NULL COMMENT 'Hashed user password',
  `Fecha_Ingresada` DATETIME NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Date and time when the user account was created',
  `MetodoDePago` VARCHAR(45) NULL COMMENT 'Preferred payment method information',
  `Id_Address` INT NULL COMMENT 'Foreign key to the user''s default address in the Address table',
  PRIMARY KEY (`Id_Usuario`),
  UNIQUE INDEX `Email_UNIQUE` (`Email` ASC) VISIBLE,
  UNIQUE INDEX `Telefono_UNIQUE` (`Telefono` ASC) VISIBLE,
  INDEX `fk_Usuarios_Address_idx` (`Id_Address` ASC) VISIBLE,
  CONSTRAINT `fk_Usuarios_Address`
    FOREIGN KEY (`Id_Address`)
    REFERENCES `mydb`.`Address` (`Id_Address`)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB
COMMENT = 'Stores user account details and links to their default address.';


-- -----------------------------------------------------
-- Table `mydb`.`Puntos_Balance`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Puntos_Balance` (
  `Id_Usuario` INT NOT NULL COMMENT 'Foreign key linking to the user; also Primary Key',
  `Puntos_Total` INT NOT NULL DEFAULT 0 COMMENT 'Current available points balance',
  `Redimidos_Total` INT NOT NULL DEFAULT 0 COMMENT 'Lifetime total points redeemed by the user',
  `Actualizado_En` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp of the last balance update',
  PRIMARY KEY (`Id_Usuario`),
  CONSTRAINT `fk_Puntos_Balance_Usuarios`
    FOREIGN KEY (`Id_Usuario`)
    REFERENCES `mydb`.`Usuarios` (`Id_Usuario`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
COMMENT = 'Tracks the current points balance and lifetime redeemed points for each user.';


-- -----------------------------------------------------
-- Table `mydb`.`Menu_Objetos`
-- Description: Stores details about menu items (including image URL).
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Menu_Objetos` (
  `Id_Objeto` INT NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for the menu item',
  `Nombre_Objeto` VARCHAR(100) NOT NULL COMMENT 'Name of the menu item (must be unique globally)',
  `Precio` DECIMAL(10, 2) NULL COMMENT 'Price of the menu item',
  `Categoria` VARCHAR(45) NOT NULL COMMENT 'Category of the item (e.g., Appetizer, Main, Drink)',
  `Calorias` INT NULL COMMENT 'Calorie count for the item',
  `Imagen_URL` VARCHAR(255) NULL COMMENT 'URL or path to the menu item image', -- <-- ADDED LINE
  PRIMARY KEY (`Id_Objeto`),
  UNIQUE INDEX `idx_unique_item_name` (`Nombre_Objeto` ASC) VISIBLE
  )
ENGINE = InnoDB
COMMENT = 'Stores individual menu items available, including a reference to an image.'; -- Updated comment


-- -----------------------------------------------------
-- Table `mydb`.`Orden`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Orden` (
  `Id_Orden` INT NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for the order transaction',
  `Id_Usuario` INT NOT NULL COMMENT 'Foreign key linking to the user who placed the order',
  `Id_Delivery_Address` INT NOT NULL COMMENT 'Foreign key linking to the address for this specific order delivery',
  `Precio_Total` DECIMAL(10, 2) NULL COMMENT 'Calculated total price for the order',
  `Puntos_Gastados` INT NULL DEFAULT 0 COMMENT 'Points redeemed by the user for this order',
  `Puntos_Ganados` INT NULL DEFAULT 0 COMMENT 'Points earned by the user from this order',
  `Fecha_Orden` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Date and time when the order was placed',
  PRIMARY KEY (`Id_Orden`),
  INDEX `fk_Orden_Usuarios_idx` (`Id_Usuario` ASC) VISIBLE,
  INDEX `fk_Orden_Address_idx` (`Id_Delivery_Address` ASC) VISIBLE,
  CONSTRAINT `fk_Orden_Usuarios`
    FOREIGN KEY (`Id_Usuario`)
    REFERENCES `mydb`.`Usuarios` (`Id_Usuario`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Orden_Address`
    FOREIGN KEY (`Id_Delivery_Address`)
    REFERENCES `mydb`.`Address` (`Id_Address`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
COMMENT = 'Stores header information for customer orders, linking user and delivery address.';


-- -----------------------------------------------------
-- Table `mydb`.`Orden_Items`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Orden_Items` (
  `Id_Orden_Item` INT NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for this specific line item in an order',
  `Id_Orden` INT NOT NULL COMMENT 'Foreign key linking to the order header',
  `Id_Objeto` INT NOT NULL COMMENT 'Foreign key linking to the menu item ordered',
  `Quantity` INT NOT NULL DEFAULT 1 COMMENT 'Number of this specific item ordered',
  `Precio_Unitario_Congelado` DECIMAL(10, 2) NOT NULL COMMENT 'Price of the item unit at the time the order was placed',
  PRIMARY KEY (`Id_Orden_Item`),
  INDEX `fk_Orden_Items_Orden_idx` (`Id_Orden` ASC) VISIBLE,
  INDEX `fk_Orden_Items_Menu_Objetos_idx` (`Id_Objeto` ASC) VISIBLE,
  UNIQUE INDEX `idx_unique_item_per_order` (`Id_Orden` ASC, `Id_Objeto` ASC) VISIBLE,
  CONSTRAINT `fk_Orden_Items_Orden`
    FOREIGN KEY (`Id_Orden`)
    REFERENCES `mydb`.`Orden` (`Id_Orden`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Orden_Items_Menu_Objetos`
    FOREIGN KEY (`Id_Objeto`)
    REFERENCES `mydb`.`Menu_Objetos` (`Id_Objeto`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
COMMENT = 'Stores the individual line items for each order, linking orders and menu items.';

-- -----------------------------------------------------
-- Restore Original Settings
-- -----------------------------------------------------
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;