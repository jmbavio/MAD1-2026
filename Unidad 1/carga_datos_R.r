# Cargar librerías
library(tidyverse)
library(lubridate)
library(caret)
library(naniar)
library(httr)
library(jsonlite)

# Fijar semilla
set.seed(42)

cat("Librerías cargadas correctamente\n")
# Crear dataset
n <- 200

empleados <- tibble(
  id = 1:n,
  nombre = paste('Empleado_', 1:n),
  edad = sample(22:64, n, replace = TRUE),
  departamento = sample(c('IT', 'Ventas', 'RRHH', 'Finanzas', 'Marketing'), 
                       n, replace = TRUE),
  salario = sample(30000:119999, n, replace = TRUE),
  fecha_ingreso = seq(as.Date('2015-01-01'), by = '7 days', length.out = n),
  educacion = sample(c('secundaria', 'universitaria', 'posgrado'), 
                    n, replace = TRUE, prob = c(0.2, 0.6, 0.2))
)

# Introducir problemas de calidad

# 1. Valores faltantes
na_indices_edad <- sample(1:nrow(empleados), 15)
na_indices_salario <- sample(1:nrow(empleados), 10)
empleados$edad[na_indices_edad] <- NA
empleados$salario[na_indices_salario] <- NA

# 2. Duplicados
empleados <- bind_rows(empleados, empleados[c(5, 10, 15), ])

# 3. Inconsistencias en texto
empleados$departamento[20:25] <- tolower(empleados$departamento[20:25])
empleados$departamento[30:32] <- '  IT  '  # Con espacios

# 4. Valores fuera de rango
empleados$edad[40] <- -5
empleados$edad[41] <- 150
empleados$salario[50] <- -10000

cat("Dataset creado:", nrow(empleados), "filas,", ncol(empleados), "columnas\n")