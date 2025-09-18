# Análisis de diabetes.csv

Ruta del CSV: `/Users/emiliano/proyecto/datos/TC1002S-Dataset/diabetes.csv`

- Filas: 768
- Columnas: 9

## Variables y tipos

- **Pregnancies**: int64

- **Glucose**: int64

- **BloodPressure**: int64

- **SkinThickness**: int64

- **Insulin**: int64

- **BMI**: float64

- **DiabetesPedigreeFunction**: float64

- **Age**: int64

- **Outcome**: int64


## Valores faltantes por columna

- Pregnancies: 0

- Glucose: 0

- BloodPressure: 0

- SkinThickness: 0

- Insulin: 0

- BMI: 0

- DiabetesPedigreeFunction: 0

- Age: 0

- Outcome: 0


## Rango (mín–máx) de variables numéricas

| Variable | Mín | Máx |
|---|---:|---:|

| Pregnancies | 0.000 | 17.000 |

| Glucose | 0.000 | 199.000 |

| BloodPressure | 0.000 | 122.000 |

| SkinThickness | 0.000 | 99.000 |

| Insulin | 0.000 | 846.000 |

| BMI | 0.000 | 67.100 |

| DiabetesPedigreeFunction | 0.078 | 2.420 |

| Age | 21.000 | 81.000 |

| Outcome | 0.000 | 1.000 |


## Estadísticos descriptivos (media, mediana, desviación estándar)

| Variable | Media | Mediana | Desv.Std |
|---|---:|---:|---:|

| Pregnancies | 3.845 | 3.000 | 3.370 |

| Glucose | 120.895 | 117.000 | 31.973 |

| BloodPressure | 69.105 | 72.000 | 19.356 |

| SkinThickness | 20.536 | 23.000 | 15.952 |

| Insulin | 79.799 | 30.500 | 115.244 |

| BMI | 31.993 | 32.000 | 7.884 |

| DiabetesPedigreeFunction | 0.472 | 0.372 | 0.331 |

| Age | 33.241 | 29.000 | 11.760 |

| Outcome | 0.349 | 0.000 | 0.477 |


## Asimetría y posibles valores atípicos (regla IQR)

| Variable | Skew | Posibles atípicos |
|---|---:|---:|

| Pregnancies | 0.902 | 4 |

| Glucose | 0.174 | 5 |

| BloodPressure | -1.844 | 45 |

| SkinThickness | 0.109 | 1 |

| Insulin | 2.272 | 34 |

| BMI | -0.429 | 19 |

| DiabetesPedigreeFunction | 1.920 | 29 |

| Age | 1.130 | 9 |

| Outcome | 0.635 | 0 |


## Correlación con Outcome (opcional)

|                          |      corr |
|:-------------------------|----------:|
| Glucose                  | 0.466581  |
| BMI                      | 0.292695  |
| Age                      | 0.238356  |
| Pregnancies              | 0.221898  |
| DiabetesPedigreeFunction | 0.173844  |
| Insulin                  | 0.130548  |
| SkinThickness            | 0.0747522 |
| BloodPressure            | 0.0650684 |


## Conclusiones

- Media, mediana y desviación estándar permiten ver tendencia central y dispersión por variable.
- Si la **media > mediana** suele haber **asimetría positiva** (cola a la derecha); si **media < mediana**, asimetría negativa.
- Variables con **desviación estándar alta** muestran mayor variabilidad y posibles valores extremos.
- El conteo de **posibles atípicos (IQR)** sugiere columnas a depurar o revisar por errores de captura.


Variables con mayor dispersión (top 3 por desviación estándar):

- Insulin: 115.244

- Glucose: 31.973

- BloodPressure: 19.356


Variables con mayor asimetría (top 3 por |skew|):

- Insulin: 2.272

- DiabetesPedigreeFunction: 1.920

- BloodPressure: 1.844
