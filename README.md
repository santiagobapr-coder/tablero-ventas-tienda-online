# Tablero de ventas para tienda online

Tablero que responde las preguntas que un dueño de tienda online se hace cada semana:
**¿cuánto vendí?, ¿cómo voy contra el año pasado?, ¿qué canal funciona?, ¿qué productos se están
cayendo?, ¿cuántos clientes vuelven?**

## Qué incluye

| Archivo | Qué hace |
| --- | --- |
| `generate_data.py` | Genera `ventas.csv` con datos inventados (2025–oct 2026, 20 productos, 4 canales) |
| `dashboard.py` | Calcula indicadores y crea `tablero.html`, un archivo autónomo que abre en cualquier navegador |
| `dashboard_kit.py` | Funciones de diseño del tablero (tarjetas, gráficos, tablas) |
| `powerbi/medidas_dax.md` | Pasos y medidas DAX para reproducirlo en Power BI |

## Indicadores y análisis

- Ingresos, pedidos, ticket promedio y clientes activos, comparados contra el mismo periodo del año anterior.
- Ingresos mensuales 2026 contra 2025.
- Top 10 de productos y participación por canal.
- Pedidos de clientes nuevos y recurrentes por mes.
- **Alertas de productos que pierden tracción:** ventas de los últimos 3 meses contra los 3 anteriores.

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
python generate_data.py
python dashboard.py
# abre tablero.html en el navegador
```

## Con tus propios datos

Reemplaza `ventas.csv` por un archivo con estas columnas: `order_id, fecha, cliente_id, producto_id,
producto, categoria, canal, cantidad, precio_unitario, descuento` y vuelve a correr `dashboard.py`.

## Tecnologías

Python, pandas, matplotlib, HTML/CSS. Guía complementaria en Power BI (DAX).

> Todos los datos son inventados y generados con una semilla fija para poder reproducir los resultados.


## Qué busca (el problema)

Un dueño de tienda online ve ventas en Excel y no sabe qué canal rinde, qué producto cae ni si los clientes vuelven.

## Cómo se cumple

Consolida las ventas en un tablero con KPIs frente al mismo periodo del año anterior, canales, clientes nuevos vs recurrentes y alerta de productos que pierden tracción.

## Cómo ofrecerlo como servicio

- **Qué entrego:** Tablero a la medida + montaje en Power BI (medidas DAX incluidas) y actualización mensual.
- **A quién:** Tiendas en Shopify/WooCommerce/Instagram con ventas en Excel o CSV.
- **Precio de referencia (ajustar):** Montaje inicial: 400.000–1.200.000 COP según fuentes de datos. Mantenimiento mensual opcional: 150.000–400.000 COP.
- **Frase para empezar:** «Te muestro en un tablero qué canal y qué productos te dejan plata, con tus propias ventas. Te enseño una demo con datos de ejemplo.»
- **Flujo:** 1) reunión corta y datos del cliente → 2) prototipo con sus datos → 3) ajustes → 4) entrega y capacitación.

> Datos del repositorio inventados; ejecutar los scripts para reproducir el tablero.
