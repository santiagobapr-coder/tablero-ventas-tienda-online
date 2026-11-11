# Guía para reproducir el tablero en Power BI

Esta carpeta no incluye un archivo `.pbix`: el tablero de este proyecto se genera con Python
(`dashboard.py`). Si el cliente prefiere Power BI, estos son los pasos y las medidas DAX
equivalentes sobre el mismo archivo `ventas.csv`.

## 1. Carga y limpieza (Power Query)

1. Obtener datos → Texto/CSV → `ventas.csv`.
2. Tipos: `fecha` como Fecha, `cantidad`, `precio_unitario` y `descuento` como número.
3. Columna personalizada `ingreso = [cantidad] * [precio_unitario] * (1 - [descuento])`.

## 2. Tabla de calendario

```dax
Calendario =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2025, 1, 1 ), DATE ( 2026, 12, 31 ) ),
    "Año", YEAR ( [Date] ),
    "MesNum", MONTH ( [Date] ),
    "Mes", FORMAT ( [Date], "mmm" )
)
```

Relación: `Calendario[Date]` → `ventas[fecha]` (uno a muchos). Marcar como tabla de fechas.

## 3. Medidas

```dax
Ingresos = SUM ( ventas[ingreso] )

Pedidos = DISTINCTCOUNT ( ventas[order_id] )

Ticket promedio = DIVIDE ( [Ingresos], [Pedidos] )

Ingresos año anterior =
CALCULATE ( [Ingresos], SAMEPERIODLASTYEAR ( Calendario[Date] ) )

Variación anual % =
DIVIDE ( [Ingresos] - [Ingresos año anterior], [Ingresos año anterior] )

Clientes activos = DISTINCTCOUNT ( ventas[cliente_id] )

Primera compra =
CALCULATE ( MIN ( ventas[fecha] ), ALLEXCEPT ( ventas, ventas[cliente_id] ) )

Pedidos clientes nuevos =
CALCULATE (
    [Pedidos],
    FILTER ( ventas, EOMONTH ( ventas[fecha], 0 ) = EOMONTH ( [Primera compra], 0 ) )
)

Pedidos recurrentes = [Pedidos] - [Pedidos clientes nuevos]
```

## 4. Páginas sugeridas

- **Resumen:** tarjetas (Ingresos, Pedidos, Ticket promedio, Clientes activos), línea de ingresos por mes con año anterior, segmentadores de año y canal.
- **Productos:** barras de los 10 productos con más ingresos y matriz producto × mes.
- **Canales y clientes:** barras por canal y columnas apiladas de pedidos nuevos y recurrentes.

## 5. Validación

Compara `Ingresos` total en Power BI con el total que muestra `tablero.html`. Deben coincidir.
