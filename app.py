import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# ----------------------------
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
st.subheader("Análisis interactivo - Tienda de barrio")
st.write("Antes de ver el gráfico, participa 👇")

producto_usuario = st.selectbox(
    "¿Qué producto crees que la gente dejaría de comprar más fácil si sube el precio?",
    df["Producto"]
)
if st.button("Ver resultado"):
    valor = df[df["Producto"] == producto_usuario]["Elasticidad"].values[0]
    if valor > 1:
        st.success(f"{producto_usuario} es ELÁSTICO 📉 (la gente sí reduce su consumo)")
    else:
        st.info(f"{producto_usuario} es INELÁSTICO 📊 (la gente lo sigue comprando)")

st.subheader("📈 Gráfico tipo semáforo")
fig, ax = plt.subplots()
ax.bar(df["Producto"], df["Elasticidad"], color=df["Color"])
ax.axhline(y=1, linestyle='--')
ax.set_ylabel("Elasticidad")
ax.set_xlabel("Productos")
ax.set_title("Elasticidad Precio de la Demanda")
plt.xticks(rotation=45)
st.pyplot(fig)

st.markdown("""
### 🧠 ¿Cómo interpretar?
- 🟢 Verde: Productos INELÁSTICOS → Se siguen comprando (arroz, leche, huevos)
- 🔴 Rojo: Productos ELÁSTICOS → Se dejan de comprar más fácil (café, aceite, pan)

👉 Línea punteada = punto clave (elasticidad = 1)
""")

st.subheader("📌 Conclusión")
st.write("""
En barrios como El Perdomo, la mayoría de productos básicos son inelásticos,
porque las personas los necesitan en su día a día. Sin embargo, algunos productos
como el café o las galletas sí cambian más su demanda cuando sube el precio.
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
        cant = st.number_input(label, min_value=0, max_value=10, value=0,
                               key=f"{prefix}_{p['nombre']}")
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
# SECCIÓN 1 JUGADOR
# ============================================================
st.divider()
st.title("🛒 Haz tu mercado inteligente")
st.markdown("Participa en el juego y aprende sobre elasticidad, bienes sustitutos, presupuesto, oferta y demanda.")

st.header("Paso 1: Elige tu personaje")
personaje = st.selectbox("Selecciona tu personaje:", list(personajes.keys()))
info = personajes[personaje]
st.write(f"**{personaje}** {info['emoji']}: {info['descripcion']}")
st.write(f"Edad: {info['edad']} | {info['condiciones']}")
st.write(f"Presupuesto: **${info['presupuesto']:,}**")

col_p2, col_p3 = st.columns(2, gap="large")

with col_p2:
    st.header("🛒 Paso 2: Precios normales")
    cantidades_ind1 = inputs_productos(productos, prefix="ind1")
    total_ind1, sel_ind1 = calcular_total(cantidades_ind1, productos, usar_precio_nuevo=False)
    st.progress(min(total_ind1 / info['presupuesto'], 1.0),
                text=f"Usado: ${total_ind1:,} de ${info['presupuesto']:,}")
    if st.button("✅ Finalizar (precios normales)", key="btn_ind1"):
        if total_ind1 > info['presupuesto']:
            st.error(f"¡Te pasaste! ${total_ind1:,} > ${info['presupuesto']:,}")
        elif total_ind1 == 0:
            st.warning("No seleccionaste nada.")
        else:
            st.success(f"Compra realizada: ${total_ind1:,}")
            for item in sel_ind1:
                st.write(f"- {item['producto']} x{item['cantidad']} = ${item['total']:,}")

with col_p3:
    st.header("📈 Paso 3: ¡Precios subieron!")
    cantidades_ind2 = inputs_productos(productos, prefix="ind2", usar_precio_nuevo=True)
    total_ind2, sel_ind2 = calcular_total(cantidades_ind2, productos, usar_precio_nuevo=True)
    st.progress(min(total_ind2 / info['presupuesto'], 1.0),
                text=f"Usado: ${total_ind2:,} de ${info['presupuesto']:,}")
    if st.button("✅ Finalizar (precios nuevos)", key="btn_ind2"):
        if total_ind2 > info['presupuesto']:
            st.error(f"¡Te pasaste! ${total_ind2:,} > ${info['presupuesto']:,}")
        elif total_ind2 == 0:
            st.warning("No seleccionaste nada.")
        else:
            st.success(f"Compra realizada: ${total_ind2:,}")
            for item in sel_ind2:
                st.write(f"- {item['producto']} x{item['cantidad']} = ${item['total']:,}")
            st.info("¿Qué dejaste de comprar? ¿Qué mantuviste? ¿Por qué?")

st.header("Paso 4: Producción y decisiones empresariales 🏭")
st.write("Imagina que eres Don Carlos, dueño del supermercado. ¿Qué harías si suben tus costos?")
decision = st.selectbox("¿Qué decisión tomarías?", [
    "Subir precios",
    "Comprar menos mercancía",
    "Contratar menos empleados",
    "Buscar proveedores más baratos"
])
st.write(f"Elegiste: **{decision}**")
st.markdown("""
**Conceptos:** Elasticidad e inelasticidad · Bienes sustitutos · Presupuesto · Estratos · Producción · Costos · Oferta y demanda

🎁 El que haga el mercado más inteligente gana un dulce 🍬
""")


# ============================================================
# SECCIÓN 2 JUGADORES SIMULTÁNEOS
# ============================================================
st.divider()
st.title("🛒 Mercado inteligente — 2 Jugadores simultáneos")
st.markdown("**José** y **Laura** juegan al mismo tiempo. Cada columna es un jugador.")

# ---- PASO 2: precios normales ----
st.header("Paso 2: Precios normales 🛒")
col_jose1, col_laura1 = st.columns(2, gap="large")

with col_jose1:
    st.subheader("👴 José")
    st.caption(f"Presupuesto: ${personajes['José']['presupuesto']:,} | {personajes['José']['condiciones']}")
    st.caption(personajes['José']['descripcion'])
    st.markdown("---")
    cant_jose1 = inputs_productos(productos, prefix="jose1")
    total_jose1, sel_jose1 = calcular_total(cant_jose1, productos)
    st.progress(min(total_jose1 / personajes['José']['presupuesto'], 1.0),
                text=f"Usado: ${total_jose1:,} / ${personajes['José']['presupuesto']:,}")
    if st.button("✅ José finaliza (precios normales)", key="btn_jose1"):
        if total_jose1 > personajes['José']['presupuesto']:
            st.error(f"¡José, te pasaste! ${total_jose1:,}")
        elif total_jose1 == 0:
            st.warning("José no seleccionó nada.")
        else:
            st.success(f"¡José listo! Total: ${total_jose1:,}")
            for item in sel_jose1:
                st.write(f"- {item['producto']} x{item['cantidad']} = ${item['total']:,}")

with col_laura1:
    st.subheader("👩 Laura")
    st.caption(f"Presupuesto: ${personajes['Laura']['presupuesto']:,} | {personajes['Laura']['condiciones']}")
    st.caption(personajes['Laura']['descripcion'])
    st.markdown("---")
    cant_laura1 = inputs_productos(productos, prefix="laura1")
    total_laura1, sel_laura1 = calcular_total(cant_laura1, productos)
    st.progress(min(total_laura1 / personajes['Laura']['presupuesto'], 1.0),
                text=f"Usado: ${total_laura1:,} / ${personajes['Laura']['presupuesto']:,}")
    if st.button("✅ Laura finaliza (precios normales)", key="btn_laura1"):
        if total_laura1 > personajes['Laura']['presupuesto']:
            st.error(f"¡Laura, te pasaste! ${total_laura1:,}")
        elif total_laura1 == 0:
            st.warning("Laura no seleccionó nada.")
        else:
            st.success(f"¡Laura lista! Total: ${total_laura1:,}")
            for item in sel_laura1:
                st.write(f"- {item['producto']} x{item['cantidad']} = ${item['total']:,}")

# ---- PASO 3: precios nuevos ----
st.divider()
st.header("Paso 3: ¡Subida de precios! 📈")
col_jose2, col_laura2 = st.columns(2, gap="large")

with col_jose2:
    st.subheader("👴 José — precios nuevos")
    st.caption(f"Presupuesto: ${personajes['José']['presupuesto']:,}")
    st.markdown("---")
    cant_jose2 = inputs_productos(productos, prefix="jose2", usar_precio_nuevo=True)
    total_jose2, sel_jose2 = calcular_total(cant_jose2, productos, usar_precio_nuevo=True)
    st.progress(min(total_jose2 / personajes['José']['presupuesto'], 1.0),
                text=f"Usado: ${total_jose2:,} / ${personajes['José']['presupuesto']:,}")
    if st.button("✅ José finaliza (precios nuevos)", key="btn_jose2"):
        if total_jose2 > personajes['José']['presupuesto']:
            st.error(f"¡José, te pasaste! ${total_jose2:,}")
        elif total_jose2 == 0:
            st.warning("José no seleccionó nada.")
        else:
            st.success(f"¡José listo! Total: ${total_jose2:,}")
            for item in sel_jose2:
                st.write(f"- {item['producto']} x{item['cantidad']} = ${item['total']:,}")
            st.info("¿Dejó de comprar medicina? (bien inelástico)")

with col_laura2:
    st.subheader("👩 Laura — precios nuevos")
    st.caption(f"Presupuesto: ${personajes['Laura']['presupuesto']:,}")
    st.markdown("---")
    cant_laura2 = inputs_productos(productos, prefix="laura2", usar_precio_nuevo=True)
    total_laura2, sel_laura2 = calcular_total(cant_laura2, productos, usar_precio_nuevo=True)
    st.progress(min(total_laura2 / personajes['Laura']['presupuesto'], 1.0),
                text=f"Usado: ${total_laura2:,} / ${personajes['Laura']['presupuesto']:,}")
    if st.button("✅ Laura finaliza (precios nuevos)", key="btn_laura2"):
        if total_laura2 > personajes['Laura']['presupuesto']:
            st.error(f"¡Laura, te pasaste! ${total_laura2:,}")
        elif total_laura2 == 0:
            st.warning("Laura no seleccionó nada.")
        else:
            st.success(f"¡Laura lista! Total: ${total_laura2:,}")
            for item in sel_laura2:
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
