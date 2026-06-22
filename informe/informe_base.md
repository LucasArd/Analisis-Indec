# Evolución del mercado laboral e ingresos: Neuquén-Plottier vs Mar del Plata

## 1. Introducción

Este informe analiza la evolución de la tasa de actividad, la tasa de empleo, la tasa de desocupación y los ingresos de la población en dos aglomerados urbanos relevados por la EPH: Neuquén-Plottier y Mar del Plata. El período cubierto por las bases descargadas es 2016T2-2025T4. La comparación combina una lectura temporal de los indicadores laborales con un análisis de ingresos reales, variables sociodemográficas y un modelo inicial de imputación de ingresos.

## 2. Datos y metodología

La fuente principal son los microdatos de la Encuesta Permanente de Hogares (EPH) publicados por INDEC. Se utilizan las bases de personas para el período 2016T2-2025T4. Los códigos de aglomerado empleados son 17 para Neuquén-Plottier y 34 para Mar del Plata. Las tasas laborales se calculan con el ponderador `PONDERA`. Para los ingresos de ocupados se usa `P21`, ponderado con `PONDIIO` cuando está disponible.

La tasa de actividad se calcula como PEA sobre población total ponderada; la tasa de empleo como ocupados sobre población total ponderada; y la tasa de desocupación como desocupados sobre PEA. Para ingresos reales se usa el IPC Nivel General Nacional, base diciembre 2016, publicado por INDEC/datos.gob.ar. Como la serie nacional mensual comienza en diciembre de 2016, el análisis de ingresos reales comienza efectivamente en 2016T4. Los valores se expresan a precios de 2025T4.

## 3. Evolución de los indicadores laborales

![Tasa de actividad](../outputs/figures/tasa_actividad.png)

![Tasa de empleo](../outputs/figures/tasa_empleo.png)

![Tasa de desocupación](../outputs/figures/tasa_desocupación.png)

La comparación muestra trayectorias laborales con oscilaciones importantes entre 2016 y 2025. El período 2020 se destaca por el impacto de la pandemia, visible en la caída de observaciones y en movimientos fuertes de actividad y empleo. La lectura comparativa debe hacerse mirando tanto niveles como cambios: Mar del Plata suele mostrar una estructura laboral sensible a estacionalidad y servicios, mientras que Neuquén-Plottier está atravesado por el peso de actividades energéticas y dinámicas regionales patagónicas.

## 4. Ingresos reales

![Ingreso mediano real](../outputs/figures/ingreso_mediano_real.png)

![Distribución de ingresos](../outputs/figures/boxplot_ingresos_reales_2025.png)

El ingreso mediano real permite observar la capacidad de compra de los ocupados una vez descontada la inflación. Se prioriza la mediana por sobre la media porque los ingresos presentan alta asimetría y valores extremos. El boxplot de 2025 muestra que la dispersión de ingresos es considerable en ambos aglomerados, por lo que la comparación no debe limitarse al promedio.

## 5. Análisis por subgrupos

![Desocupación por sexo](../outputs/figures/desocupación_por_sexo.png)

![Empleo por nivel educativo](../outputs/figures/empleo_por_nivel_educativo_2025.png)

El análisis por sexo y nivel educativo permite ver heterogeneidades que quedan ocultas en las tasas agregadas. En general, la insercion laboral tiende a mejorar con el nivel educativo, mientras que la desocupación por sexo puede mostrar brechas persistentes. Estas diferencias son relevantes para interpretar si la evolución agregada se explica por mejoras generalizadas o por cambios concentrados en ciertos grupos.

## 6. Exploracion univariada y no respuesta

La tabla `outputs/tables/resumen_univariado.csv` resume faltantes, percentiles y posibles valores atípicos para variables clave. En ingresos, la no respuesta requiere tratamiento especifico. En este primer corte se considera no respuesta operativa de ingresos en ocupados cuando `P21` es faltante o negativo. Los ingresos iguales a cero no se imputan automáticamente, ya que pueden corresponder a ocupados sin ingreso laboral monetario declarado en el período.

## 7. Modelo de imputación de ingresos

Antes del modelo de imputación se estimaron dos modelos de regresión lineal vistos en clase. El primero es una regresión lineal simple, donde el logaritmo del ingreso real se explica únicamente por la edad. El segundo es una regresión lineal múltiple, donde se incorporan edad, sexo, nivel educativo, aglomerado, año, trimestre, rama de actividad (`PP04B_COD`) y ocupación (`PP04D_COD`). Estos modelos permiten mostrar como mejora la capacidad explicativa cuando se pasa de una relación bivariada a una especificación multivariada.

| Modelo | n train | n test | MAE | RMSE | R2 log |
|---|---:|---:|---:|---:|---:|
| Regresión lineal simple: log(P21 real) ~ edad | 18395 | 6132 | 615552 | 1003449 | 0.001 |
| Regresión lineal múltiple: log(P21 real) ~ edad + sexo + educación + aglomerado + período + rama + ocupación | 18395 | 6132 | 443112 | 773494 | 0.454 |

Para la imputación de no respuesta se ajusto además un modelo Ridge sobre el logaritmo del ingreso real de la ocupación principal (`log(P21_REAL)`). Ridge mantiene una estructura lineal, pero agrega regularización para reducir la inestabilidad de coeficientes cuando hay muchas categorías de rama y ocupación. El modelo se entrenó con ocupados con ingreso positivo y se evaluó con una partición train/test. Luego se aplico a los ocupados con `P21` faltante o negativo para generar ingresos imputados.

Metricas principales:

| Modelo | n train | n test | MAE | RMSE | R2 log |
|---|---:|---:|---:|---:|---:|
| Ridge sobre log(P21 real) | 18395 | 6132 | 438927 | 765421 | 0.460 |

La interpretacion de coeficientes debe hacerse en términos aproximados de cambios porcentuales sobre el ingreso real. La tabla `outputs/tables/modelo_imputación_coeficientes_top.csv` lista los efectos de mayor magnitud. La tabla `outputs/tables/ingresos_reales_imputados_trimestrales.csv` compara la mediana de ingresos original con la mediana luego de imputar no respuesta. Al tratarse de un modelo lineal regularizado, su principal ventaja es la interpretabilidad; su limite es que puede no capturar no linealidades complejas del mercado laboral.

## 8. Síntesis comparativa

La tabla `outputs/tables/resumen_inicial_final.csv` resume el primer y ultimo período observado para tasas laborales e ingresos reales. Como primer resultado, el trabajo muestra que ambos aglomerados atravesaron cambios laborales relevantes en el período, con una ruptura visible durante 2020 y una recomposición posterior. La comparación de ingresos reales muestra una evolución condicionada por la alta inflación del período, por lo que el ajuste por IPC es imprescindible para evitar conclusiones nominales engañosas.

## 9. Limitaciones y próximos ajustes

Esta version es una base de trabajo. Quedan tres puntos para revisar con cuidado: confirmar con el diseno de registro la codificacion exacta de no respuesta de ingresos; decidir si se usa IPC nacional o algun IPC regional/provincial para sensibilidad; y selecciónar los gráficos finales para que el informe quede entre 6 y 10 paginas.
