# Analisis INDEC - EPH 2016T2-2025T4

Proyecto para analizar microdatos de la Encuesta Permanente de Hogares (EPH) de INDEC.

## Estructura

```text
data/
  infoCruda/       # descargas originales, no versionadas
  infoProcesada/   # bases unificadas generadas, no versionadas
  infoInflacion/   # datos de inflacion
outputs/
  figures/         # graficos generados
  tables/          # tablas generadas
src/
  download_eph.py
  build_eph_processed.py
notas/
```

## Instalacion

```powershell
python -m pip install -r requirements.txt
```

## Descargar microdatos EPH

Descarga las bases trimestrales en formato txt desde INDEC para el periodo 2016T2-2025T4:

```powershell
python src/download_eph.py
```

Los archivos quedan en:

```text
data/infoCruda/eph/
```

## Construir bases procesadas

Une las bases de individuos y hogares:

```powershell
python src/build_eph_processed.py
```

Las salidas quedan en:

```text
data/infoProcesada/eph/eph_individual_2016T2_2025T4.csv.gz
data/infoProcesada/eph/eph_hogar_2016T2_2025T4.csv.gz
data/infoProcesada/eph/resumen_archivos_eph.csv
```

## Nota sobre datos

Las bases crudas y procesadas no se suben al repositorio porque son archivos pesados y reproducibles desde la fuente oficial. Para trabajar, cada integrante debe ejecutar los scripts anteriores.
