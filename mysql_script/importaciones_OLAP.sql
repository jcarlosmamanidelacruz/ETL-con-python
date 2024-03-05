CREATE DATABASE IF NOT EXISTS `importaciones_olap`;

DROP SCHEMA IF EXISTS `importaciones_olap`;

CREATE SCHEMA IF NOT EXISTS `importaciones_olap` DEFAULT CHARACTER SET utf8;

USE `importaciones_olap` ;

-- -----------------------------------------------------
-- Table `importaciones_olap`.`DIM_PAISORIGEN`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `importaciones_olap`.`DIM_PAISORIGEN` (
  `IdPaisOrigen` INT NOT NULL,
  `NombrePaisOrigen` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`IdPaisOrigen`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `importaciones_olap`.`DIM_ADUANAINGRESO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `importaciones_olap`.`DIM_ADUANAINGRESO` (
  `IdAduanaIngreso` INT NOT NULL,
  `NombreAduanaIngreso` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`IdAduanaIngreso`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `importaciones_olap`.`DIM_PAISADUANA`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `importaciones_olap`.`DIM_PAISADUANA` (
  `IdPais_IdAduana` INT NOT NULL,
  `IdPaisOrigen` INT NOT NULL,
  `IdAduanaIngreso` INT NOT NULL,
  PRIMARY KEY (`IdPais_IdAduana`),
  INDEX `fk_DIM_PAISADUANA_DIM_PAISORIGEN_idx` (`IdPaisOrigen` ASC) VISIBLE,
  INDEX `fk_DIM_PAISADUANA_DIM_ADUANAINGRESO1_idx` (`IdAduanaIngreso` ASC) VISIBLE,
  CONSTRAINT `fk_DIM_PAISADUANA_DIM_PAISORIGEN`
    FOREIGN KEY (`IdPaisOrigen`)
    REFERENCES `importaciones_olap`.`DIM_PAISORIGEN` (`IdPaisOrigen`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_DIM_PAISADUANA_DIM_ADUANAINGRESO1`
    FOREIGN KEY (`IdAduanaIngreso`)
    REFERENCES `importaciones_olap`.`DIM_ADUANAINGRESO` (`IdAduanaIngreso`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `importaciones_olap`.`DIM_FECHA`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `importaciones_olap`.`DIM_FECHA` (
  `IdFecha` INT NOT NULL,
  `FechaImportacion` DATE NOT NULL,
  `Anio` SMALLINT NULL,
  `Mes` SMALLINT NULL,
  `Mes_nombre` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`IdFecha`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `importaciones_olap`.`FAC_IMPORTACION`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `importaciones_olap`.`FAC_IMPORTACION` (
  `IdPais_IdAduana` INT NOT NULL,
  `IdFecha` INT NOT NULL,
  `ValorCIF` DOUBLE NOT NULL,
  `Impuesto` DOUBLE NOT NULL,
  INDEX `fk_FAC_IMPORTACION_DIM_PAISADUANA1_idx` (`IdPais_IdAduana` ASC) VISIBLE,
  INDEX `fk_FAC_IMPORTACION_DIM_FECHA1_idx` (`IdFecha` ASC) VISIBLE,
  CONSTRAINT `fk_FAC_IMPORTACION_DIM_PAISADUANA1`
    FOREIGN KEY (`IdPais_IdAduana`)
    REFERENCES `importaciones_olap`.`DIM_PAISADUANA` (`IdPais_IdAduana`)
    
    
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_FAC_IMPORTACION_DIM_FECHA1`
    FOREIGN KEY (`IdFecha`)
    REFERENCES `importaciones_olap`.`DIM_FECHA` (`IdFecha`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
