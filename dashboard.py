"""Tablero de ventas para tienda online -> tablero.html (autónomo)."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from dashboard_kit import PALETTE, SERIES, money, render_dashboard, table_html, tag

df = pd.read_csv("ventas.csv", parse_dates=["fecha"])
df["ingreso"] = df["cantidad"] * df["precio_unitario"] * (1 - df["descuento"])
df["mes"] = df["fecha"].dt.to_period("M")
df["anio"] = df["fecha"].dt.year

# --- Periodos comparables: ene-oct 2026 vs ene-oct 2025
cur = df[(df.anio == 2026)]
prev = df[(df.anio == 2025) & (df.fecha.dt.month <= 10)]


def kpis(d):
    ped = d.order_id.nunique()
    ing = d.ingreso.sum()
    return ing, ped, ing / ped, d.cliente_id.nunique()


c_ing, c_ped, c_tm, c_cli = kpis(cur)
p_ing, p_ped, p_tm, p_cli = kpis(prev)


def delta(a, b):
    v = (a / b - 1) * 100
    return f"{v:+.1f}% vs ene-oct 2025", "up" if v >= 0 else "down"


# --- Clientes nuevos vs recurrentes por mes
primera = df.groupby("cliente_id")["fecha"].min().dt.to_period("M")
ped = df.drop_duplicates("order_id")[["order_id", "cliente_id", "mes"]].copy()
ped["tipo"] = np.where(ped["mes"] == ped["cliente_id"].map(primera), "Nuevos", "Recurrentes")
nr = ped.groupby(["mes", "tipo"]).size().unstack(fill_value=0)
nr = nr.iloc[3:]  # se omiten los primeros 3 meses del historial (todos aparecerían como nuevos)
pct_rec = nr["Recurrentes"].iloc[-10:].sum() / nr.iloc[-10:].sum().sum() * 100

# --- Gráfico 1: ingresos mensuales 2025 vs 2026
mens = df.groupby(["anio", df.fecha.dt.month])["ingreso"].sum().unstack(0) / 1e6
fig1, ax = plt.subplots(figsize=(7.2, 3.8))
meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
ax.plot(mens.index, mens[2025], color=PALETTE["muted"], lw=2.2, marker="o", ms=4, label="2025")
ax.plot(mens.index[:10], mens[2026].dropna(), color=PALETTE["primary"], lw=2.6, marker="o", ms=5, label="2026")
ax.set_xticks(range(1, 13), meses)
ax.set_ylabel("Millones COP")
ax.set_title("Ingresos mensuales: 2026 vs 2025")
ax.legend(frameon=False)

# --- Gráfico 2: top 10 productos
top = df.groupby("producto")["ingreso"].sum().sort_values().tail(10) / 1e6
fig2, ax = plt.subplots(figsize=(7.2, 3.8))
ax.barh(top.index, top.values, color=PALETTE["primary"])
ax.set_xlabel("Millones COP (acumulado)")
ax.set_title("Top 10 productos por ingresos")
ax.grid(axis="y", visible=False)

# --- Gráfico 3: canales
can = df.groupby("canal")["ingreso"].sum().sort_values(ascending=False) / 1e6
fig3, ax = plt.subplots(figsize=(7.2, 3.4))
bars = ax.bar(can.index, can.values, color=SERIES[: len(can)])
for b, v in zip(bars, can.values):
    ax.text(b.get_x() + b.get_width() / 2, v, f"{v / can.sum() * 100:.0f}%", ha="center", va="bottom", fontsize=10, color=PALETTE["ink"])
ax.set_ylabel("Millones COP")
ax.set_ylim(0, can.max() * 1.15)
ax.set_title("Ingresos por canal (participación)")
ax.grid(axis="x", visible=False)

# --- Gráfico 4: nuevos vs recurrentes
fig4, ax = plt.subplots(figsize=(7.2, 3.4))
x = np.arange(len(nr))
ax.bar(x, nr["Nuevos"], color=PALETTE["accent"], label="Nuevos")
ax.bar(x, nr["Recurrentes"], bottom=nr["Nuevos"], color=PALETTE["primary"], label="Recurrentes")
ax.set_xticks(x[::2], [str(m) for m in nr.index[::2]], rotation=45, ha="right")
ax.set_ylabel("Pedidos")
ax.set_title("Pedidos de clientes nuevos y recurrentes")
ax.legend(frameon=False, ncol=2)
ax.grid(axis="x", visible=False)

# --- Alertas: productos que caen vs. los 3 meses previos
ult = df[df.fecha >= "2026-08-01"].groupby("producto")["ingreso"].sum()
ant = df[(df.fecha >= "2026-05-01") & (df.fecha < "2026-08-01")].groupby("producto")["ingreso"].sum()
var = ((ult / ant - 1) * 100).dropna().sort_values()
rows = []
for prod, v in var.head(5).items():
    kind = "bad" if v < -30 else "warn" if v < -10 else "good"
    rows.append([prod, money(ult[prod]), money(ant[prod]), tag(f"{v:+.0f}%", kind)])
alertas = table_html(["Producto", "Ago-Oct 2026", "May-Jul 2026", "Variación"], rows)

render_dashboard(
    "tablero.html",
    "Tablero de ventas · Tienda online",
    "Ene 2025 – oct 2026 · Precios en COP · Datos de ejemplo",
    kpis=[
        ("Ingresos 2026 (ene-oct)", money(c_ing), *delta(c_ing, p_ing)),
        ("Pedidos", f"{c_ped:,}", *delta(c_ped, p_ped)),
        ("Ticket promedio", money(c_tm), *delta(c_tm, p_tm)),
        ("Clientes activos", f"{c_cli:,}", *delta(c_cli, p_cli)),
        ("Pedidos de recurrentes", f"{pct_rec:.0f}%", "últimos 10 meses", ""),
    ],
    sections=[
        {"title": "Evolución y comparación anual", "note": "Cada mes de 2026 contra el mismo mes de 2025.", "figs": [fig1, fig2]},
        {"title": "Canales y clientes", "note": "Qué canal vende más y cuánto aportan los clientes que ya compraron antes.", "figs": [fig3, fig4]},
        {"title": "Productos que pierden tracción", "note": "Ventas de los últimos 3 meses contra los 3 anteriores. Rojo: caída de más de 30%.", "html": alertas},
    ],
)
print("tablero.html listo")
print(var.head(5).round(1))
