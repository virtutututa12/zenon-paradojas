"""
===============================================================================
SIMULADOR DE PARADOJAS: Aquiles y la Tortuga (Zenón de Elea) + Límites Laterales
===============================================================================

Proyecto: "Simuladores de Paradojas" — Línea tecnológica de programación (Python)

Este script construye una aplicación web interactiva con Streamlit que contiene
dos visualizaciones:

  1) LA PARADOJA DE ZENÓN (Aquiles y la Tortuga)
     Se muestra cómo una suma infinita de pasos (tiempos e intervalos cada vez
     más pequeños) converge a un valor de tiempo y distancia FINITO, resolviendo
     la paradoja mediante el concepto de serie geométrica convergente.

  2) LÍMITES LATERALES Y RUPTURA DE UNA FUNCIÓN
     Se explora qué ocurre con f(x) cuando x se aproxima a un punto crítico
     x = a por la izquierda (x -> a-) y por la derecha (x -> a+), incluyendo
     discontinuidad de salto, discontinuidad removible (hueco) y asíntota
     vertical (discontinuidad infinita).

-------------------------------------------------------------------------------
REQUISITOS (ejecutar antes de correr la app):

    pip install streamlit numpy plotly sympy pandas

-------------------------------------------------------------------------------
CÓMO EJECUTAR (ver también las instrucciones al final de este archivo y en el
documento de sustentación adjunto):

    streamlit run zenon_paradojas_app.py

-------------------------------------------------------------------------------
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import sympy as sp

# ==============================================================================
# CONFIGURACIÓN GENERAL DE LA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Paradojas de Zenón: Aquiles, la Tortuga y los Límites",
    page_icon="🐢",
    layout="wide",
)

st.title("🐢🏃 Simulador de Paradojas de Zenón de Elea")
st.markdown(
    """
Esta aplicación explora **dos caras del mismo problema matemático**: qué pasa
cuando dividimos algo (tiempo, distancia, una función) en pasos cada vez más
pequeños **sin límite**. Usa las pestañas para navegar entre ambas simulaciones.
"""
)

tab1, tab2 = st.tabs(
    ["🏃 Paradoja de Aquiles y la Tortuga", "📉 Límites Laterales y Ruptura de f(x)"]
)

# ==============================================================================
# =====================  TAB 1: AQUILES Y LA TORTUGA  ========================
# ==============================================================================
with tab1:
    st.header("Paradoja de Aquiles y la Tortuga")
    st.markdown(
        r"""
        Zenón argumentaba que Aquiles (rápido) nunca alcanzaría a la tortuga
        (lenta, con ventaja inicial), porque cada vez que Aquiles llega a donde
        estaba la tortuga, ella ya avanzó un poco más — y esto se repite
        **infinitas veces**. La resolución está en notar que, aunque el número
        de pasos es infinito, la **suma de los tiempos** de esos pasos converge
        a un valor finito (serie geométrica convergente).
        """
    )

    # ---------------------------------------------------------------------
    # Controles interactivos (sliders)
    # ---------------------------------------------------------------------
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        v_aquiles = st.slider("Velocidad de Aquiles (m/s)", 2.0, 20.0, 10.0, 0.5)
    with col_b:
        v_tortuga = st.slider(
            "Velocidad de la tortuga (m/s)", 0.1, v_aquiles - 0.5, 2.0, 0.1
        )
    with col_c:
        ventaja = st.slider("Ventaja inicial de la tortuga (m)", 1.0, 100.0, 10.0, 1.0)

    n_pasos = st.slider(
        "Número de pasos de Zenón a graficar (n)",
        1,
        30,
        12,
        1,
        help="Cada 'paso de Zenón' es: Aquiles llega a donde la tortuga estaba antes.",
    )

    # ---------------------------------------------------------------------
    # Matemática del modelo
    # ---------------------------------------------------------------------
    # Paso 1: Aquiles recorre la distancia de la ventaja inicial d0.
    #   tiempo del paso 1 -> t1 = d0 / v_aquiles
    #   en ese tiempo, la tortuga avanzó -> d1 = v_tortuga * t1
    # Paso 2: Aquiles debe recorrer d1 -> t2 = d1 / v_aquiles = t1 * r,  r = v_tortuga/v_aquiles
    # ... en general, cada paso es el anterior multiplicado por la razón r < 1
    #
    # => Es una serie geométrica de razón r = v_tortuga / v_aquiles < 1
    #    Suma infinita de tiempos = t1 / (1 - r)   (convergente, pues 0 < r < 1)

    r = v_tortuga / v_aquiles
    t1 = ventaja / v_aquiles

    pasos = np.arange(1, n_pasos + 1)
    t_pasos = t1 * r ** (pasos - 1)          # tiempo de cada paso individual
    t_acumulado = np.cumsum(t_pasos)         # suma parcial de tiempos (S_n)

    # Límite exacto (cierre algebraico, sin usar la serie): tiempo y punto de encuentro real
    t_encuentro = ventaja / (v_aquiles - v_tortuga)
    x_encuentro = v_aquiles * t_encuentro

    # Verificación: la suma de la serie infinita coincide con el cierre algebraico
    suma_serie_infinita = t1 / (1 - r)

    st.latex(
        r"""
        t_{\text{encuentro}} \;=\; \sum_{n=1}^{\infty} t_1 \, r^{\,n-1}
        \;=\; \frac{t_1}{1-r}, \qquad r = \frac{v_{\text{tortuga}}}{v_{\text{Aquiles}}} < 1
        """
    )

    m1, m2, m3 = st.columns(3)
    m1.metric("Razón geométrica r", f"{r:.4f}")
    m1.metric("Suma de la serie (tiempo límite)", f"{suma_serie_infinita:.4f} s")
    m2.metric("Tiempo real de encuentro", f"{t_encuentro:.4f} s")
    m3.metric("Posición real de encuentro", f"{x_encuentro:.4f} m")
    st.caption(
        "Nótese que la suma de la serie infinita **coincide exactamente** con el "
        "cálculo directo de encuentro (cinemática clásica): la paradoja desaparece "
        "porque infinitos pasos pueden sumar un tiempo finito."
    )

    # ---------------------------------------------------------------------
    # Gráfica 1: convergencia de la suma parcial S_n hacia el límite
    # ---------------------------------------------------------------------
    fig_conv = go.Figure()
    fig_conv.add_trace(
        go.Scatter(
            x=pasos,
            y=t_acumulado,
            mode="lines+markers",
            name="Suma parcial S_n (tiempo acumulado)",
            marker=dict(size=8, color="crimson"),
            line=dict(width=2, color="crimson"),
        )
    )
    fig_conv.add_hline(
        y=t_encuentro,
        line_dash="dash",
        line_color="black",
        annotation_text=f"Límite finito t = {t_encuentro:.3f} s",
        annotation_position="bottom right",
    )
    fig_conv.update_layout(
        title="Convergencia de la suma de los 'pasos de Zenón' hacia un tiempo finito",
        xaxis_title="Número de paso n",
        yaxis_title="Tiempo acumulado S_n (s)",
        height=420,
    )
    st.plotly_chart(fig_conv, use_container_width=True)

    # ---------------------------------------------------------------------
    # Gráfica 2: posición real de Aquiles y la tortuga en el tiempo
    # ---------------------------------------------------------------------
    t_max_plot = t_encuentro * 1.3
    t_line = np.linspace(0, t_max_plot, 400)
    pos_aquiles = v_aquiles * t_line
    pos_tortuga = ventaja + v_tortuga * t_line

    # Posiciones en cada "paso de Zenón" (para mostrar cómo se acercan al punto límite)
    t_marca = np.concatenate(([0], t_acumulado))
    pos_marca_aquiles = v_aquiles * t_marca

    fig_pos = go.Figure()
    fig_pos.add_trace(
        go.Scatter(x=t_line, y=pos_aquiles, mode="lines", name="Aquiles (posición real)", line=dict(color="royalblue"))
    )
    fig_pos.add_trace(
        go.Scatter(x=t_line, y=pos_tortuga, mode="lines", name="Tortuga (posición real)", line=dict(color="seagreen"))
    )
    fig_pos.add_trace(
        go.Scatter(
            x=t_marca,
            y=pos_marca_aquiles,
            mode="markers",
            name="Pasos de Zenón (n)",
            marker=dict(color="crimson", size=9, symbol="x"),
        )
    )
    fig_pos.add_trace(
        go.Scatter(
            x=[t_encuentro],
            y=[x_encuentro],
            mode="markers",
            name="Punto de encuentro (límite)",
            marker=dict(color="black", size=14, symbol="star"),
        )
    )
    fig_pos.update_layout(
        title="Posición de Aquiles y la tortuga: los pasos de Zenón se acumulan en el punto de encuentro",
        xaxis_title="Tiempo (s)",
        yaxis_title="Posición (m)",
        height=460,
    )
    st.plotly_chart(fig_pos, use_container_width=True)

    with st.expander("📋 Ver tabla numérica de los primeros pasos de Zenón"):
        df_pasos = pd.DataFrame(
            {
                "Paso n": pasos,
                "Tiempo del paso (s)": t_pasos,
                "Tiempo acumulado S_n (s)": t_acumulado,
                "Distancia recorrida por Aquiles en este paso (m)": v_aquiles * t_pasos,
            }
        )
        st.dataframe(df_pasos, use_container_width=True)

# ==============================================================================
# ==================  TAB 2: LÍMITES LATERALES Y RUPTURA  ====================
# ==============================================================================
with tab2:
    st.header("Límites Laterales y Ruptura de una Función")
    st.markdown(
        r"""
        Así como la paradoja de Zenón trata sobre acercarse infinitamente en el
        **tiempo**, el concepto de límite lateral trata sobre acercarse
        infinitamente en el **eje x**. Elige un tipo de discontinuidad y observa
        qué ocurre cuando $x \to a^-$ (por la izquierda) y $x \to a^+$
        (por la derecha).
        """
    )

    tipo = st.selectbox(
        "Tipo de discontinuidad a explorar",
        [
            "Discontinuidad de salto (jump)",
            "Discontinuidad removible (hueco)",
            "Discontinuidad infinita (asíntota vertical)",
        ],
    )

    col1, col2 = st.columns(2)
    with col1:
        a = st.slider("Punto crítico x = a", -5.0, 5.0, 1.0, 0.1)
    with col2:
        epsilon = st.slider(
            "Distancia de aproximación ε (qué tan cerca de 'a' evaluamos)",
            0.5,
            0.001,
            0.2,
            0.001,
            help="Entre más pequeño ε, más cerca estamos de x = a. Muévelo hacia la izquierda para 'acercarte tanto como quieras'.",
        )

    x_sym, a_sym = sp.symbols("x a", real=True)

    # -----------------------------------------------------------------------
    # Definición simbólica (sympy) y numérica de cada función según el caso
    # -----------------------------------------------------------------------
    if tipo == "Discontinuidad de salto (jump)":
        expr_izq = x_sym**2                     # rama para x < a
        expr_der = x_sym**2 + 2                 # rama para x >= a  (salto de tamaño 2)

        def f_numpy(x, a):
            return np.where(x < a, x**2, x**2 + 2)

        f_sym = sp.Piecewise((expr_izq, x_sym < a_sym), (expr_der, True))

    elif tipo == "Discontinuidad removible (hueco)":
        # f(x) = (x^2 - a^2)/(x-a) = x + a  para todo x != a ; en x=a NO está definida
        def f_numpy(x, a):
            with np.errstate(divide="ignore", invalid="ignore"):
                y = (x**2 - a**2) / (x - a)
            return y

        f_sym = (x_sym**2 - a_sym**2) / (x_sym - a_sym)

    else:  # Asíntota vertical
        def f_numpy(x, a):
            with np.errstate(divide="ignore", invalid="ignore"):
                y = 1.0 / (x - a)
            return y

        f_sym = 1 / (x_sym - a_sym)

    # -----------------------------------------------------------------------
    # Cálculo simbólico riguroso de los límites laterales con sympy
    # -----------------------------------------------------------------------
    f_a = f_sym.subs(a_sym, a)
    lim_izq = sp.limit(f_a, x_sym, a, dir="-")
    lim_der = sp.limit(f_a, x_sym, a, dir="+")

    def fmt_limit(v):
        if v in (sp.oo, -sp.oo):
            return f"{v}"
        return f"{float(v):.4f}"

    st.latex(
        rf"\lim_{{x \to a^-}} f(x) = {sp.latex(lim_izq)} \qquad\qquad "
        rf"\lim_{{x \to a^+}} f(x) = {sp.latex(lim_der)}"
    )

    existe = (lim_izq == lim_der) and (lim_izq not in (sp.oo, -sp.oo, sp.zoo))
    if existe:
        st.success(
            f"✅ El límite **existe** en x = a, y vale L = {fmt_limit(lim_izq)}. "
            "Ambos límites laterales coinciden."
        )
    else:
        st.error(
            "❌ El límite **NO existe** en x = a (los límites laterales difieren, "
            "o divergen a infinito). La función es discontinua en ese punto."
        )

    # -----------------------------------------------------------------------
    # Tabla de aproximación punto a punto (izquierda / derecha) con ε decreciente
    # -----------------------------------------------------------------------
    factores = np.array([1, 1 / 2, 1 / 4, 1 / 8, 1 / 16, 1 / 64, 1 / 256])
    eps_vals = epsilon * factores
    x_izq_vals = a - eps_vals
    x_der_vals = a + eps_vals

    df_aprox = pd.DataFrame(
        {
            "ε (distancia a 'a')": eps_vals,
            "x → a⁻  (izquierda)": x_izq_vals,
            "f(x → a⁻)": f_numpy(x_izq_vals, a),
            "x → a⁺  (derecha)": x_der_vals,
            "f(x → a⁺)": f_numpy(x_der_vals, a),
        }
    )
    st.markdown("**Tabla de aproximación:** observa cómo f(x) se estabiliza (o no) mientras ε → 0")
    st.dataframe(df_aprox.style.format(precision=4), use_container_width=True)

    # -----------------------------------------------------------------------
    # Gráfica de la función con los puntos de aproximación
    # -----------------------------------------------------------------------
    x_range = np.linspace(a - 4, a + 4, 1600)
    x_range = x_range[np.abs(x_range - a) > 1e-6]  # evitar división por cero exacta
    y_range = f_numpy(x_range, a)

    fig_lim = go.Figure()

    if tipo == "Discontinuidad infinita (asíntota vertical)":
        # separar ramas para no dibujar una línea vertical falsa a través de la asíntota
        izq_mask = x_range < a
        fig_lim.add_trace(go.Scatter(x=x_range[izq_mask], y=y_range[izq_mask], mode="lines", name="f(x)", line=dict(color="royalblue")))
        fig_lim.add_trace(go.Scatter(x=x_range[~izq_mask], y=y_range[~izq_mask], mode="lines", showlegend=False, line=dict(color="royalblue")))
        fig_lim.update_yaxes(range=[-20, 20])
    elif tipo == "Discontinuidad de salto (jump)":
        izq_mask = x_range < a
        fig_lim.add_trace(go.Scatter(x=x_range[izq_mask], y=y_range[izq_mask], mode="lines", name="f(x), rama x<a", line=dict(color="royalblue")))
        fig_lim.add_trace(go.Scatter(x=x_range[~izq_mask], y=y_range[~izq_mask], mode="lines", name="f(x), rama x≥a", line=dict(color="royalblue")))
    else:
        fig_lim.add_trace(go.Scatter(x=x_range, y=y_range, mode="lines", name="f(x)", line=dict(color="royalblue")))
        # hueco visible en la discontinuidad removible
        fig_lim.add_trace(
            go.Scatter(x=[a], y=[2 * a], mode="markers", name="Punto no definido (hueco)",
                        marker=dict(color="white", size=12, line=dict(color="royalblue", width=2)))
        )

    fig_lim.add_trace(
        go.Scatter(x=x_izq_vals, y=f_numpy(x_izq_vals, a), mode="markers", name="Aproximación x→a⁻",
                    marker=dict(color="seagreen", size=9, symbol="triangle-right"))
    )
    fig_lim.add_trace(
        go.Scatter(x=x_der_vals, y=f_numpy(x_der_vals, a), mode="markers", name="Aproximación x→a⁺",
                    marker=dict(color="orange", size=9, symbol="triangle-left"))
    )
    fig_lim.add_vline(x=a, line_dash="dash", line_color="black", annotation_text="x = a")
    fig_lim.update_layout(
        title=f"{tipo}: aproximación lateral a x = a",
        xaxis_title="x",
        yaxis_title="f(x)",
        height=500,
    )
    st.plotly_chart(fig_lim, use_container_width=True)

    st.info(
        "💡 Mueve el slider de **ε** hacia la izquierda (valores más pequeños) para "
        "ver cómo los puntos verdes (izquierda) y naranjas (derecha) se acercan cada "
        "vez más a x = a, y observa en la tabla si f(x) se estabiliza en un mismo "
        "valor L o no."
    )

# ==============================================================================
# NOTAS FINALES EN LA PROPIA APP
# ==============================================================================
st.divider()
st.caption(
    "Proyecto 'Simuladores de Paradojas' — Paradoja de Zenón (Aquiles y la Tortuga) "
    "y Límites Laterales. Construido con Streamlit, NumPy, Plotly y SymPy."
)
