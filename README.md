# elasticidad-streamlit
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.title('Streamlit funciona!')



# ----------------------------
# DATOS
# ----------------------------
data = {
    "Producto": [
        "Arroz", "Leche", "Huevos", "Aceite", "Pan",
        "Azúcar", "Fríjoles", "Jabón", "Café", "Galletas"
    ],
    "Elasticidad": [
        0.32, 0.22, 0.19, 1.52, 1.51,
        0.64, 1.57, 0.13, 1.17, 1.44
    ]
}

df = pd.DataFrame(data)

# ----------------------------
# COLORES TIPO SEMÁFORO
# ----------------------------
def color_semáforo(valor):
    if valor > 1:
        return "red"
    elif valor > 0.8:
        return "orange"
    else:
        return "green"

df["Color"] = df["Elasticidad"].apply(color_semáforo)

# ----------------------------
# INTERFAZ
# ----------------------------
st.title("📊 Elasticidad Precio de la Demanda")
st.subheader("Análisis interactivo - Tienda de barrio")

st.write("Antes de ver el gráfico, participa 👇")

# Interacción con compañeros
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

# ----------------------------
# GRÁFICO
# ----------------------------
st.subheader("📈 Gráfico tipo semáforo")

fig, ax = plt.subplots()

ax.bar(df["Producto"], df["Elasticidad"], color=df["Color"])

# Línea clave en elasticidad = 1
ax.axhline(y=1, linestyle='--')

ax.set_ylabel("Elasticidad")
ax.set_xlabel("Productos")
ax.set_title("Elasticidad Precio de la Demanda")

plt.xticks(rotation=45)

st.pyplot(fig)

# ----------------------------
# EXPLICACIÓN
# ----------------------------
st.markdown("""
### 🧠 ¿Cómo interpretar?

- 🟢 Verde: Productos INELÁSTICOS → Se siguen comprando (arroz, leche, huevos)
- 🔴 Rojo: Productos ELÁSTICOS → Se dejan de comprar más fácil (café, aceite, pan)

👉 Línea punteada = punto clave (elasticidad = 1)
""")

# ----------------------------
# CONCLUSIÓN
# ----------------------------
st.subheader("📌 Conclusión")
st.write("""
En barrios como El Perdomo, la mayoría de productos básicos son inelásticos,
porque las personas los necesitan en su día a día. Sin embargo, algunos productos
como el café o las galletas sí cambian más su demanda cuando sube el precio.
""")
