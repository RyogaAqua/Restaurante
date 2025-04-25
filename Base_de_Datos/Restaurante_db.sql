-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Puntos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Puntos` (
  `PuntosTotal` INT NOT NULL,
  `Redimidos` INT NULL,
  `Ofertas` INT NULL,
  `PuntosGastados` INT NULL,
  PRIMARY KEY (`PuntosTotal`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Address`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Address` (
  `Address` VARCHAR(45) NOT NULL,
  `Zip_code` VARCHAR(45) NULL,
  `State` VARCHAR(45) NULL,
  `Country` VARCHAR(45) NULL,
  `City` VARCHAR(45) NULL,
  PRIMARY KEY (`Address`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Usuarios` (
  `Id_Usuario` INT NOT NULL,
  `Nombre_Usuario` VARCHAR(45) NOT NULL,
  `Apellido_Usuario` VARCHAR(45) NOT NULL,
  `Email` VARCHAR(45) NOT NULL,
  `Telefono` VARCHAR(45) NULL,
  `Hash_Contrasena_Usuario` VARCHAR(45) NULL,
  `Fecha_Ingresada` VARCHAR(45) NULL,
  `MetodoDePago` VARCHAR(45) NOT NULL,
  `Puntos` INT NOT NULL,
  `Address` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Id_Usuario`, `Puntos`, `Address`),
  UNIQUE INDEX `Email_UNIQUE` (`Email` ASC) VISIBLE,
  UNIQUE INDEX `Telefono_UNIQUE` (`Telefono` ASC) VISIBLE,
  UNIQUE INDEX `Hash_Contrasena_Usuario_UNIQUE` (`Hash_Contrasena_Usuario` ASC) VISIBLE,
  INDEX `fk_Usuarios_Puntos1_idx` (`Puntos` ASC) VISIBLE,
  INDEX `fk_Usuarios_Address1_idx` (`Address` ASC) VISIBLE,
  CONSTRAINT `fk_Usuarios_Puntos1`
    FOREIGN KEY (`Puntos`)
    REFERENCES `mydb`.`Puntos` (`PuntosTotal`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Usuarios_Address1`
    FOREIGN KEY (`Address`)
    REFERENCES `mydb`.`Address` (`Address`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Restaurante`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Restaurante` (
  `Id_Restaurante` INT NOT NULL,
  `Restaurante_Address` VARCHAR(45) NULL,
  `Nombre` VARCHAR(45) NULL,
  PRIMARY KEY (`Id_Restaurante`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Menu_Objetos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Menu_Objetos` (
  `Objetos` INT NOT NULL,
  `Nombre_Objeto` VARCHAR(45) NOT NULL,
  `Precio` INT NULL,
  `Categoria` VARCHAR(45) NOT NULL,
  `Calorias` INT NULL,
  `Restaurante` INT NOT NULL,
  PRIMARY KEY (`Objetos`, `Restaurante`),
  INDEX `fk_Menu_Objetos_Restaurante1_idx` (`Restaurante` ASC) VISIBLE,
  CONSTRAINT `fk_Menu_Objetos_Restaurante1`
    FOREIGN KEY (`Restaurante`)
    REFERENCES `mydb`.`Restaurante` (`Id_Restaurante`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Orden`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Orden` (
  `Id_Transaccion` INT NOT NULL,
  `Puntos_Total` INT NULL,
  `Precio_Total` INT NULL,
  `Id_Usuario` INT NOT NULL,
  `Puntos` INT NOT NULL,
  `Address` VARCHAR(45) NOT NULL,
  `Objetos` INT NOT NULL,
  PRIMARY KEY (`Id_Transaccion`, `Id_Usuario`, `Puntos`, `Address`, `Objetos`),
  INDEX `fk_Orden_Usuarios1_idx` (`Id_Usuario` ASC, `Puntos` ASC, `Address` ASC) VISIBLE,
  INDEX `fk_Orden_Menu_Objetos1_idx` (`Objetos` ASC) VISIBLE,
  CONSTRAINT `fk_Orden_Usuarios1`
    FOREIGN KEY (`Id_Usuario` , `Puntos` , `Address`)
    REFERENCES `mydb`.`Usuarios` (`Id_Usuario` , `Puntos` , `Address`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Orden_Menu_Objetos1`
    FOREIGN KEY (`Objetos`)
    REFERENCES `mydb`.`Menu_Objetos` (`Objetos`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
