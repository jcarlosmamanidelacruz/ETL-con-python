DROP SCHEMA IF EXISTS `importaciones_db`;

CREATE SCHEMA IF NOT EXISTS `importaciones_db` DEFAULT CHARACTER SET utf8;
USE `importaciones_db` ;

-- -----------------------------------------------------
-- Table `importaciones_db`.`MARCA`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `importaciones_db`.`MARCA` (
  `IdMarca` INT NOT NULL AUTO_INCREMENT,
  `NombreMarca` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`IdMarca`),
  UNIQUE (`NombreMarca`)
  )
  
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `importaciones_db`.`TIPO_COMBUSTIBLE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `importaciones_db`.`TIPO_COMBUSTIBLE` (
  `IdTipoCombustible` INT NOT NULL AUTO_INCREMENT,
  `NombreTipoCombustible` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`IdTipoCombustible`),
  UNIQUE (`NombreTipoCombustible`)
  )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `importaciones_db`.`TIPO_VEHICULO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `importaciones_db`.`TIPO_VEHICULO` (
  `IdTipoVehiculo` INT NOT NULL AUTO_INCREMENT,
  `NombreTipoVehiculo` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`IdTipoVehiculo`),
  UNIQUE (`NombreTipoVehiculo`)
  )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `importaciones_db`.`TIPO_IMPORTADOR`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `importaciones_db`.`TIPO_IMPORTADOR` (
  `IdTipoImportador` INT NOT NULL AUTO_INCREMENT,
  `NombreTipoImportador` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`IdTipoImportador`),
  UNIQUE (`NombreTipoImportador`)
  )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `importaciones_db`.`MODELO_LANZAMIENTO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `importaciones_db`.`MODELO_LANZAMIENTO` (
  `IdModeloLanzamiento` INT NOT NULL AUTO_INCREMENT,
  `anio` smallint NOT NULL,
  PRIMARY KEY (`IdModeloLanzamiento`),
  UNIQUE (`anio`)
  )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `importaciones_db`.`LINEA`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `importaciones_db`.`LINEA` (
  `IdLinea` INT NOT NULL AUTO_INCREMENT,
  `NombreLinea` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`IdLinea`),
  UNIQUE INDEX  (`NombreLinea`)
  )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `importaciones_db`.`PAIS_ORIGEN`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `importaciones_db`.`PAIS_ORIGEN` (
  `IdPaisOrigen` INT NOT NULL AUTO_INCREMENT,
  `NombrePaisOrigen` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`IdPaisOrigen`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `importaciones_db`.`ADUANA_INGRESO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `importaciones_db`.`ADUANA_INGRESO` (
  `IdAduanaIngreso` INT NOT NULL AUTO_INCREMENT,
  `NombreAduanaIngreso` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`IdAduanaIngreso`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `importaciones_db`.`PAIS_ADUANA`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `importaciones_db`.`PAIS_ADUANA` (
  `IdPais_IdAduana` INT NOT NULL AUTO_INCREMENT,
  `IdPaisOrigen` INT NOT NULL,
  `IdAduanaIngreso` INT NOT NULL,
  PRIMARY KEY (`IdPais_IdAduana`),
  UNIQUE INDEX `IdPais_IdAduana_UNIQUE` (`IdPaisOrigen` ASC, `IdAduanaIngreso` ASC) VISIBLE,
  CONSTRAINT `fk_PAIS_ADUANA_PAIS_ORIGEN1`
    FOREIGN KEY (`IdPaisOrigen`)
    REFERENCES `importaciones_db`.`PAIS_ORIGEN` (`IdPaisOrigen`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PAIS_ADUANA_ADUANA_INGRESO1`
    FOREIGN KEY (`IdAduanaIngreso`)
    REFERENCES `importaciones_db`.`ADUANA_INGRESO` (`IdAduanaIngreso`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `importaciones_db`.`LINEA_MODELO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `importaciones_db`.`LINEA_MODELO` (
  `IdLinea_Modelo` INT NOT NULL AUTO_INCREMENT,
  `IdLinea` INT NOT NULL,
  `IdModeloLanzamiento` INT NOT NULL,
  `IdMarca` INT NOT NULL,
  PRIMARY KEY (`IdLinea_Modelo`),
  UNIQUE INDEX `IdLinea_IdModeloLanzamiento_UNIQUE` (`IdModeloLanzamiento` ASC, `IdLinea` ASC, `IdMarca` ASC) VISIBLE,
  CONSTRAINT `fk_LINEA_MODELO_LINEA1`
    FOREIGN KEY (`IdLinea`)
    REFERENCES `importaciones_db`.`LINEA` (`IdLinea`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_LINEA_MODELO_MODELO_LANZAMIENTO1`
    FOREIGN KEY (`IdModeloLanzamiento`)
    REFERENCES `importaciones_db`.`MODELO_LANZAMIENTO` (`IdModeloLanzamiento`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_IdMarca_MARCA`
    FOREIGN KEY (`IdMarca`)
    REFERENCES `importaciones_db`.`MARCA` (`IdMarca`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `importaciones_db`.`IMPORTACION`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `importaciones_db`.`IMPORTACION` (
  `IdImportacion` INT NOT NULL AUTO_INCREMENT,
  `IdPais_IdAduana` INT NOT NULL,
  `IdLinea_Modelo` INT NOT NULL,
  `IdTipoVehiculoFk` INT NOT NULL,
  `IdTipoCombustibleFk` INT NOT NULL,
  `IdTipoImportadorFk` INT NOT NULL,
  `FechaImportacion` VARCHAR(45) NOT NULL,
  `ValorCIF` DOUBLE NOT NULL,
  `Impuesto` DOUBLE NOT NULL,
  `Puertas` INT NOT NULL,
  `Tonelaje` DOUBLE NOT NULL,
  `Asientos` INT NOT NULL,
  PRIMARY KEY (`IdImportacion`),
  INDEX `fk_VEHICULO_TIPO_VEHICULO1_idx` (`IdTipoVehiculoFk` ASC) VISIBLE,
  INDEX `fk_VEHICULO_TIPO_COMBUSTIBLE1_idx` (`IdTipoCombustibleFk` ASC) VISIBLE,
  INDEX `fk_VEHICULO_TIPO_IMPORTADOR1_idx` (`IdTipoImportadorFk` ASC) VISIBLE,
  INDEX `fk_VEHICULO_LINEA_MODELO1_idx` (`IdLinea_Modelo` ASC) VISIBLE,
  INDEX `fk_VEHICULO_PAIS_ADUANA1_idx` (`IdPais_IdAduana` ASC) VISIBLE,
  CONSTRAINT `fk_VEHICULO_TIPO_VEHICULO1`
    FOREIGN KEY (`IdTipoVehiculoFk`)
    REFERENCES `importaciones_db`.`TIPO_VEHICULO` (`IdTipoVehiculo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_VEHICULO_TIPO_COMBUSTIBLE1`
    FOREIGN KEY (`IdTipoCombustibleFk`)
    REFERENCES `importaciones_db`.`TIPO_COMBUSTIBLE` (`IdTipoCombustible`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_VEHICULO_TIPO_IMPORTADOR1`
    FOREIGN KEY (`IdTipoImportadorFk`)
    REFERENCES `importaciones_db`.`TIPO_IMPORTADOR` (`IdTipoImportador`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_VEHICULO_LINEA_MODELO1`
    FOREIGN KEY (`IdLinea_Modelo`)
    REFERENCES `importaciones_db`.`LINEA_MODELO` (`IdLinea_Modelo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_VEHICULO_PAIS_ADUANA1`
    FOREIGN KEY (`IdPais_IdAduana`)
    REFERENCES `importaciones_db`.`PAIS_ADUANA` (`IdPais_IdAduana`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
