import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# DATOS GRÁFICO
# ----------------------------
data = {
    "Producto": ["Arroz","Leche","Huevos","Aceite","Pan","Azúcar","Fríjoles","Jabón","Café","Galletas"],
    "Elasticidad": [0.32, 0.22, 0.19, 1.52, 1.51, 0.64, 1.57, 0.13, 1.17, 1.44]
}
df = pd.DataFrame(data)

def color_semáforo(v):
    return "red" if v > 1 else ("orange" if v > 0.8 else "green")

df["Color"] = df["Elasticidad"].apply(color_semáforo)


# ----------------------------
# SECCIÓN GRÁFICO
# ----------------------------
st.title("📊 Elasticidad Precio de la Demanda")

# =============================
# GRÁFICO DE BARRAS AGRUPADAS POR LOCALIDAD
# =============================
st.subheader("📊 Elasticidad por producto y localidad")
productos = ["Arroz", "Leche", "Huevos", "Aceite", "Pan", "Azúcar", "Fríjoles", "Jabón", "Café", "Galletas"]
kennedy = [0.36, 0.34, 0.24, 5.44, 1.65, 0.63, 4.22, 0.26, 4.08, 0.85]
suba = [0.27, 0.17, 0.34, 0.75, 0.64, 0.66, 0.68, 0.11, 1.01, 1.15]
ciudad_bolivar = [0.32, 0.22, 0.19, 1.52, 1.51, 0.64, 1.57, 0.13, 1.17, 1.44]

import numpy as np
bar_width = 0.22
index = np.arange(len(productos))

fig, ax = plt.subplots(figsize=(12, 6))
bars1 = ax.bar(index - bar_width, kennedy, bar_width, label='Kennedy', color='#1f77b4')
bars2 = ax.bar(index, suba, bar_width, label='Suba', color='#ff7f0e')
bars3 = ax.bar(index + bar_width, ciudad_bolivar, bar_width, label='Ciudad Bolívar', color='#2ca02c')

# Línea horizontal en y=1
ax.axhline(y=1, color='gray', linestyle='--', linewidth=1)
ax.text(len(productos)-0.5, 1.03, 'Elástico (>1)', color='gray', fontsize=10, va='bottom', ha='right')
ax.text(len(productos)-0.5, 0.97, 'Inelástico (<1)', color='gray', fontsize=10, va='top', ha='right')

ax.set_xlabel('Productos', fontsize=12)
ax.set_ylabel('Elasticidad (valor absoluto)', fontsize=12)
ax.set_title('Elasticidad precio de la demanda por producto y localidad', fontsize=14, fontweight='bold')
ax.set_xticks(index)
ax.set_xticklabels(productos, rotation=30, ha='right', fontsize=11)
ax.legend(title='Localidad', fontsize=11, title_fontsize=12)
ax.set_ylim(0, max(max(kennedy), max(suba), max(ciudad_bolivar)) + 1)
ax.grid(axis='y', linestyle=':', alpha=0.5)
fig.tight_layout()
st.pyplot(fig)


st.markdown("""
### 🧠 ¿Cómo interpretar?
- Si la barra está por debajo de la línea punteada (elasticidad < 1), la demanda es inelástica: el consumo cambia poco aunque suba el precio.
- Si la barra está por encima de la línea (elasticidad > 1), la demanda es elástica: el consumo baja mucho si sube el precio.
- Puedes comparar cómo reacciona cada producto en las tres localidades.

👉 Línea punteada = frontera entre inelástico y elástico (elasticidad = 1)
""")


st.subheader("📌 Conclusión")
st.write("""
La gráfica muestra que la reacción al precio cambia según la localidad: en Suba la demanda es mayormente inelástica (consumo estable), en Ciudad Bolívar es más elástica (alta sensibilidad al precio) y en Kennedy es mixta. Esto indica que no se pueden aplicar las mismas estrategias de precios en todas las zonas.
""")

# ----------------------------
# DATOS MERCADO
# ----------------------------
productos = [
    {"nombre": "Arroz",      "precio": 5000,  "precio_nuevo": 7000},
    {"nombre": "Leche",      "precio": 4000,  "precio_nuevo": 6000},
    {"nombre": "Huevos",     "precio": 8000,  "precio_nuevo": 8000},
    {"nombre": "Medicina",   "precio": 15000, "precio_nuevo": 18000},
    {"nombre": "Transporte", "precio": 10000, "precio_nuevo": 10000},
    {"nombre": "Netflix",    "precio": 20000, "precio_nuevo": 30000},
    {"nombre": "Perfume",    "precio": 35000, "precio_nuevo": 50000},
    {"nombre": "Gaseosa",    "precio": 6000,  "precio_nuevo": 6000},
    {"nombre": "Pan",        "precio": 3000,  "precio_nuevo": 3000},
    {"nombre": "Pollo",      "precio": 18000, "precio_nuevo": 18000},
]

personajes = {
    "José": {
        "edad": 60,
        "condiciones": "Tiene diabetes, vive con su esposa",
        "presupuesto": 50000,
        "descripcion": "Debe priorizar medicamentos y alimentos básicos. Demanda inelástica.",
        "emoji": "👴"
    },
    "Laura": {
        "edad": 24,
        "condiciones": "Vive sola, trabaja y estudia",
        "presupuesto": 80000,
        "descripcion": "Puede comprar bienes más elásticos.",
        "emoji": "👩"
    }
}

# ----------------------------
# HELPERS sin columnas anidadas
# ----------------------------
def inputs_productos(productos_lista, prefix, usar_precio_nuevo=False):
    cantidades = {}
    for p in productos_lista:
        precio = p["precio_nuevo"] if usar_precio_nuevo else p["precio"]
        sufijo = " ⬆️" if usar_precio_nuevo and p["precio_nuevo"] > p["precio"] else ""
        label = f"{p['nombre']} — ${precio:,}{sufijo}"
        cant = st.number_input(label, min_value=0, max_value=10, value=0, key=f"{prefix}_{p['nombre']}")
        cantidades[p['nombre']] = cant
    return cantidades
def calcular_total(cantidades, productos_lista, usar_precio_nuevo=False):
    total = 0
    seleccion = []
    for p in productos_lista:
        cant = cantidades.get(p['nombre'], 0)
        precio = p["precio_nuevo"] if usar_precio_nuevo else p["precio"]
        if cant > 0:
            total += cant * precio
            seleccion.append({"producto": p["nombre"], "cantidad": cant, "total": cant * precio})
    return total, seleccion






# ============================================================
# JUEGO: 2 JUGADORES SIMULTÁNEOS
# ============================================================
st.divider()
st.title("🛒 Juego: 2 Jugadores simultáneos")
st.markdown("**José** y **Laura** juegan al mismo tiempo. Cada columna es un jugador.")

col_jose, col_laura = st.columns(2, gap="large")

with col_jose:
    st.subheader("👴 José")
    st.caption(f"Presupuesto: ${personajes['José']['presupuesto']:,} | {personajes['José']['condiciones']}")
    st.caption(personajes['José']['descripcion'])
    st.markdown("---")
    cant_jose_normal = inputs_productos(productos, prefix="jose_normal")
    total_jose_normal, sel_jose_normal = calcular_total(cant_jose_normal, productos)
    st.progress(min(total_jose_normal / personajes['José']['presupuesto'], 1.0),
                text=f"Usado: ${total_jose_normal:,} / ${personajes['José']['presupuesto']:,}")
    if st.button("✅ José finaliza (precios normales)", key="btn_jose_normal"):
        if total_jose_normal > personajes['José']['presupuesto']:
            st.error(f"¡José, te pasaste! ${total_jose_normal:,}")
        elif total_jose_normal == 0:
            st.warning("José no seleccionó nada.")
        else:
            st.success(f"¡José listo! Total: ${total_jose_normal:,}")
            for item in sel_jose_normal:
                st.write(f"- {item['producto']} x{item['cantidad']} = ${item['total']:,}")

    st.markdown("**Ahora con precios nuevos:**")
    cant_jose_nuevo = inputs_productos(productos, prefix="jose_nuevo", usar_precio_nuevo=True)
    total_jose_nuevo, sel_jose_nuevo = calcular_total(cant_jose_nuevo, productos, usar_precio_nuevo=True)
    st.progress(min(total_jose_nuevo / personajes['José']['presupuesto'], 1.0),
                text=f"Usado: ${total_jose_nuevo:,} / ${personajes['José']['presupuesto']:,}")
    if st.button("✅ José finaliza (precios nuevos)", key="btn_jose_nuevo"):
        if total_jose_nuevo > personajes['José']['presupuesto']:
            st.error(f"¡José, te pasaste! ${total_jose_nuevo:,}")
        elif total_jose_nuevo == 0:
            st.warning("José no seleccionó nada.")
        else:
            st.success(f"¡José listo! Total: ${total_jose_nuevo:,}")
            for item in sel_jose_nuevo:
                st.write(f"- {item['producto']} x{item['cantidad']} = ${item['total']:,}")
            st.info("¿Dejó de comprar medicina? (bien inelástico)")

with col_laura:
    st.subheader("👩 Laura")
    st.caption(f"Presupuesto: ${personajes['Laura']['presupuesto']:,} | {personajes['Laura']['condiciones']}")
    st.caption(personajes['Laura']['descripcion'])
    st.markdown("---")
    cant_laura_normal = inputs_productos(productos, prefix="laura_normal")
    total_laura_normal, sel_laura_normal = calcular_total(cant_laura_normal, productos)
    st.progress(min(total_laura_normal / personajes['Laura']['presupuesto'], 1.0),
                text=f"Usado: ${total_laura_normal:,} / ${personajes['Laura']['presupuesto']:,}")
    if st.button("✅ Laura finaliza (precios normales)", key="btn_laura_normal"):
        if total_laura_normal > personajes['Laura']['presupuesto']:
            st.error(f"¡Laura, te pasaste! ${total_laura_normal:,}")
        elif total_laura_normal == 0:
            st.warning("Laura no seleccionó nada.")
        else:
            st.success(f"¡Laura lista! Total: ${total_laura_normal:,}")
            for item in sel_laura_normal:
                st.write(f"- {item['producto']} x{item['cantidad']} = ${item['total']:,}")

    st.markdown("**Ahora con precios nuevos:**")
    cant_laura_nuevo = inputs_productos(productos, prefix="laura_nuevo", usar_precio_nuevo=True)
    total_laura_nuevo, sel_laura_nuevo = calcular_total(cant_laura_nuevo, productos, usar_precio_nuevo=True)
    st.progress(min(total_laura_nuevo / personajes['Laura']['presupuesto'], 1.0),
                text=f"Usado: ${total_laura_nuevo:,} / ${personajes['Laura']['presupuesto']:,}")
    if st.button("✅ Laura finaliza (precios nuevos)", key="btn_laura_nuevo"):
        if total_laura_nuevo > personajes['Laura']['presupuesto']:
            st.error(f"¡Laura, te pasaste! ${total_laura_nuevo:,}")
        elif total_laura_nuevo == 0:
            st.warning("Laura no seleccionó nada.")
        else:
            st.success(f"¡Laura lista! Total: ${total_laura_nuevo:,}")
            for item in sel_laura_nuevo:
                st.write(f"- {item['producto']} x{item['cantidad']} = ${item['total']:,}")
            st.info("¿Dejó de pagar Netflix? (bien elástico)")

st.divider()
st.markdown("""
**Preguntas para reflexionar:**
- ¿Quién tomó mejores decisiones económicas?
- ¿Quién dejó de comprar más productos tras la subida de precios?
- ¿Qué productos son inelásticos para cada uno?
- ¿Qué productos sustituyeron?
""")
