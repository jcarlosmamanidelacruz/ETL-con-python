USE `importaciones_db` ;

-- MARCA
SELECT * FROM MARCA order by 2;

-- MODELO_LANZAMIENTO
SELECT * FROM MODELO_LANZAMIENTO;

-- LINEA
SELECT NombreLinea, COUNT(*)
FROM LINEA 
GROUP BY NombreLinea
HAVING COUNT(*) > 1;

SELECT * FROM LINEA order by 2;
SELECT COUNT(*) FROM LINEA;

-- LINEA_MODELO
SELECT * FROM LINEA_MODELO;

-- LINEA_MODELO
SELECT
	ma.NombreMarca,
    ln.NombreLinea,
    ml.anio,
    lm.IdLinea
	/*
	lm.IdLinea_Modelo,
    lm.IdLinea,
    ln.NombreLinea,
    lm.IdModeloLanzamiento,
    ml.anio,
    ln.IdMarcaFk,
    ma.NombreMarca
    */
FROM LINEA_MODELO lm
	LEFT JOIN LINEA ln on lm.IdLinea = ln.IdLinea
    LEFT JOIN MARCA ma on lm.IdMarca = ma.IdMarca
	LEFT JOIN MODELO_LANZAMIENTO ml on lm.IdModeloLanzamiento = ml.IdModeloLanzamiento
ORDER BY 1,2,3;

-- TIPO_VEHICULO
SELECT * FROM TIPO_VEHICULO;

-- TIPO_IMPORTADOR
SELECT * FROM TIPO_IMPORTADOR;

-- TIPO_COMBUSTIBLE
SELECT * FROM TIPO_COMBUSTIBLE;

-- PAIS_ORIGEN
SELECT * FROM PAIS_ORIGEN;

-- ADUANA_INGRESO
SELECT * FROM ADUANA_INGRESO;

-- PAIS_ADUANA

SELECT * FROM PAIS_ADUANA;

SELECT
	pad.IdPais_IdAduana,
    po.NombrePaisOrigen,
    ai.NombreAduanaIngreso
FROM PAIS_ADUANA pad
	LEFT JOIN PAIS_ORIGEN po on pad.IdPaisOrigen = po.IdPaisOrigen
    LEFT JOIN ADUANA_INGRESO ai on pad.IdAduanaIngreso = ai.IdAduanaIngreso
    LEFT JOIN LINEA_MODELO lm on 
order by 2, 3;

-- IMPORTACION
SELECT
	po.NombrePaisOrigen,
	ai.NombreAduanaIngreso,
    im.FechaImportacion,
    ml.anio,
    ma.NombreMarca,
    ln.NombreLinea,
    tp.NombreTipoVehiculo,
    ti.NombreTipoImportador,
    tc.NombreTipoCombustible,
	im.asientos,
	im.puertas,
	im.tonelaje,
	im.valorCIF,
	im.impuesto
FROM IMPORTACION im
LEFT JOIN PAIS_ADUANA pad ON im.IdPais_IdAduana = pad.IdPais_IdAduana
LEFT JOIN PAIS_ORIGEN po on pad.IdPaisOrigen = po.IdPaisOrigen
LEFT JOIN ADUANA_INGRESO ai on pad.IdAduanaIngreso = ai.IdAduanaIngreso
LEFT JOIN LINEA_MODELO lm on im.IdLinea_Modelo = lm.IdLinea_Modelo
LEFT JOIN MODELO_LANZAMIENTO ml on lm.IdModeloLanzamiento = ml.IdModeloLanzamiento
LEFT JOIN MARCA ma on lm.IdMarca = ma.IdMarca
LEFT JOIN LINEA ln on lm.IdLinea = ln.IdLinea
LEFT JOIN TIPO_VEHICULO tp on im.IdTipoVehiculoFk = tp.IdTipoVehiculo
LEFT JOIN TIPO_IMPORTADOR ti on im.IdTipoImportadorFk = ti.IdTipoImportador
LEFT JOIN TIPO_COMBUSTIBLE tc on im.IdTipoCombustibleFk = tc.IdTipoCombustible;
-- WHERE im.IdImportacion = 1;

SELECT FechaImportacion, count(*)
FROM IMPORTACION
group by FechaImportacion
order by FechaImportacion;


SELECT count(*)
FROM IMPORTACION;
