# Sustentación matemática — Paradoja de Zenón y Límites Laterales

## 0. Resumen del proyecto

La aplicación `zenon_paradojas_app.py` (Streamlit) contiene dos simulaciones:

1. **Aquiles y la Tortuga**, mostrando que una suma infinita de intervalos de
   tiempo cada vez más pequeños **converge** a un valor finito.
2. **Límites laterales**, mostrando qué pasa con una función f(x) cuando x se
   aproxima a un punto crítico *a* por la izquierda y por la derecha.

Ambos fenómenos son, matemáticamente, la misma idea: **acercarse "tanto como
se quiera" a un valor mediante infinitos pasos no implica que el proceso sea
infinito en extensión — puede converger a un límite finito.**

---

## 1. Resolución matemática de la paradoja de Aquiles y la tortuga

### 1.1 Planteamiento de Zenón

Aquiles corre a velocidad `v_A` y la tortuga a velocidad `v_T`, con `v_A > v_T`.
La tortuga parte con una ventaja `d0`. Zenón divide la persecución en pasos:

- Paso 1: Aquiles recorre la distancia `d0` que lo separaba de la tortuga. Tarda
  `t1 = d0 / v_A`. En ese tiempo la tortuga avanzó `d1 = v_T · t1`.
- Paso 2: Aquiles debe recorrer ahora `d1`. Tarda `t2 = d1 / v_A`. La tortuga
  avanza `d2 = v_T · t2`.
- Y así sucesivamente, **infinitas veces**.

Zenón concluye — erróneamente — que como el número de pasos es infinito,
Aquiles "nunca" alcanza a la tortuga.

### 1.2 Los pasos forman una serie geométrica

Cada paso es una fracción constante del anterior:

```
t_(n+1) / t_n = v_T / v_A = r,   con   0 < r < 1
```

Por lo tanto, los tiempos de los pasos son:

```
t_n = t1 · r^(n-1)
```

y el "tiempo total" que propone Zenón es la **serie geométrica**:

```
T = Σ_{n=1}^{∞} t1 · r^(n-1)
```

### 1.3 Convergencia de la serie

Como `0 < r < 1`, esta serie geométrica **converge** (criterio de la serie
geométrica: converge si y solo si `|r| < 1`), y su suma tiene una fórmula
cerrada:

```
T = t1 · Σ_{n=0}^{∞} r^n = t1 / (1 - r)
```

Esto es un número **finito**, aunque la suma tenga infinitos términos. Es
exactamente el mismo tipo de resultado que el caso particular famoso:

```
Σ_{n=1}^{∞} 1/2^n = 1
```

(aquí `r = 1/2`, `t1 = 1/2`, y la suma da 1 — finito).

### 1.4 Verificación con cinemática clásica

Si resolvemos el problema de encuentro de forma directa (sin pasos de Zenón),
igualando posiciones `x_A(t) = v_A t` y `x_T(t) = d0 + v_T t`:

```
v_A t = d0 + v_T t   =>   t_encuentro = d0 / (v_A - v_T)
```

Puede demostrarse algebraicamente que:

```
t1 / (1 - r) = [d0 / v_A] / [1 - v_T/v_A] = d0 / (v_A - v_T) = t_encuentro
```

Es decir, **la suma de la serie infinita de Zenón coincide exactamente con el
tiempo real de encuentro**. La paradoja no revela una contradicción física:
revela que nuestra intuición sobre "infinitos pasos = tiempo infinito" es
incorrecta. Infinitos pasos pueden ocurrir dentro de un intervalo de tiempo
finito, siempre que sus duraciones decrezcan lo suficientemente rápido (razón
geométrica `r < 1`).

### 1.5 Relación con el concepto de límite

Formalmente, el "tiempo total" es el **límite de las sumas parciales**:

```
T = lim_{n→∞} S_n,     S_n = Σ_{k=1}^{n} t_k
```

En la aplicación, la gráfica de "convergencia" muestra justamente la sucesión
`S_n` acercándose asintóticamente a la recta horizontal `T = t_encuentro`,
sin necesidad de que `n` llegue a ser realmente infinito para que la
diferencia `|T - S_n|` sea tan pequeña como se quiera.

---

## 2. Límites laterales y ruptura de una función

### 2.1 Definición de límite lateral

- **Límite por la izquierda:** `lim_{x→a⁻} f(x) = L₁` significa que f(x) se
  acerca a `L₁` tanto como se quiera, cuando x se aproxima a `a` tomando
  valores **menores** que `a` (por la izquierda en la recta numérica).
- **Límite por la derecha:** `lim_{x→a⁺} f(x) = L₂` significa lo mismo, pero
  con valores de x **mayores** que `a`.

Formalmente (definición ε-δ), `lim_{x→a⁻} f(x) = L₁` si para todo `ε > 0`
existe `δ > 0` tal que si `a - δ < x < a`, entonces `|f(x) - L₁| < ε`. La
definición para el límite derecho es análoga, con `a < x < a + δ`.

### 2.2 Condición de existencia del límite bilateral

```
lim_{x→a} f(x) existe   <=>   lim_{x→a⁻} f(x) = lim_{x→a⁺} f(x) = L
```

Si ambos límites laterales existen y son iguales, el límite general existe y
vale `L`. Si son distintos (o alguno no existe / diverge a infinito), el
**límite general no existe**.

### 2.3 Los tres casos simulados en la aplicación

| Caso | Definición de f(x) | Límite izq. | Límite der. | ¿Existe el límite? | ¿Continua en a? |
|---|---|---|---|---|---|
| **Salto (jump)** | `x²` si `x<a`; `x²+2` si `x≥a` | `a²` | `a²+2` | No (difieren) | No |
| **Removible (hueco)** | `(x²-a²)/(x-a) = x+a`, indefinida en `x=a` | `2a` | `2a` | Sí (`L=2a`) | No (f(a) no está definida) |
| **Infinita (asíntota)** | `1/(x-a)` | `-∞` | `+∞` | No (diverge) | No |

**Interpretación de cada caso:**

- **Discontinuidad de salto:** los dos límites laterales existen como números
  finitos, pero son **diferentes**. La gráfica "salta" de un valor a otro en
  `x=a`. Es el análogo, en el eje x, de una suma que no converge a un único
  valor: aquí el "acercamiento" desde dos direcciones produce dos resultados
  distintos.
- **Discontinuidad removible:** los dos límites laterales **coinciden**
  (`L = 2a`), por lo que el límite bilateral sí existe — pero la función no
  está definida en `x = a` (división por cero en la expresión original antes
  de simplificar). Se dice "removible" porque bastaría **redefinir** `f(a) = 2a`
  para que la función fuera continua ahí.
- **Discontinuidad infinita (asíntota vertical):** al acercarnos por la
  izquierda, `f(x) → -∞`; por la derecha, `f(x) → +∞` (o viceversa, según el
  signo). Ninguno de los dos límites laterales es un número finito, así que
  el límite ni siquiera se puede comparar — la función se "rompe" de forma
  más drástica, alejándose sin cota en vez de saltar a otro valor finito.

### 2.4 Conexión con la paradoja de Zenón

En la paradoja de Zenón, nos preguntamos qué pasa cuando el **número de
pasos** tiende a infinito (`n → ∞`) y encontramos que la suma parcial `S_n`
**sí** converge a un límite finito `T`, porque los tiempos decrecen
geométricamente.

En los límites laterales, nos preguntamos qué pasa cuando la **variable x**
se acerca a un punto `a`. A veces (caso removible) el proceso de acercamiento
sí converge a un valor único, y a veces (salto, asíntota) no converge o
converge a valores distintos según la dirección.

En ambos casos, el concepto clave es el mismo: **evaluar el comportamiento de
una cantidad cuando otra cantidad se acerca "tanto como se quiera" a un valor
—ya sea el número de pasos tendiendo a infinito, o la variable x tendiendo a
un punto—**, y preguntarnos si ese proceso de acercamiento converge a un
único valor finito o no.

---

## 3. Instrucciones de ejecución y despliegue

### Opción A — Google Colab (rápido, sin necesidad de cuenta externa)

Streamlit no se ejecuta de forma nativa como un notebook de Colab (necesita un
servidor), así que la manera más simple y confiable de usarlo en Colab es con
un túnel local. Pasos:

1. Sube `zenon_paradojas_app.py` y `requirements.txt` a tu entorno de Colab
   (panel de archivos, ícono de carpeta a la izquierda → subir).
2. En una celda de código, instala las dependencias y `localtunnel`:

   ```python
   !pip install -q streamlit numpy pandas plotly sympy
   !npm install -g localtunnel -q
   ```

3. En otra celda, lanza la app en segundo plano y crea el túnel público:

   ```python
   import subprocess, time
   subprocess.Popen(["streamlit", "run", "zenon_paradojas_app.py",
                      "--server.port", "8501", "--server.headless", "true"])
   time.sleep(5)
   !npx localtunnel --port 8501
   ```

4. La celda imprimirá una URL pública (algo como `https://xxxx.loca.lt`).
   Ábrela en el navegador; te pedirá una contraseña ("Tunnel Password") que
   es la IP pública que aparece justo arriba del enlace en la salida de la
   celda (o puedes obtenerla con `!curl https://loca.lt/mytunnelpassword`).

### Opción B — Streamlit Community Cloud (recomendado para el enlace final del proyecto)

Esta opción genera un **enlace permanente** ideal para la fase de exposición.

1. Crea un repositorio en GitHub (puede ser público) y sube estos tres
   archivos:
   - `zenon_paradojas_app.py`
   - `requirements.txt`
   - (opcional) `sustentacion_paradoja_zenon.md`
2. Entra a **share.streamlit.io** (Streamlit Community Cloud) e inicia sesión
   con tu cuenta de GitHub.
3. Haz clic en **"New app"**, selecciona el repositorio, la rama (`main`) y
   como archivo principal indica `zenon_paradojas_app.py`.
4. Haz clic en **"Deploy"**. Streamlit Cloud instalará automáticamente lo
   indicado en `requirements.txt` y en 1–2 minutos generará un enlace público
   permanente tipo `https://tu-usuario-zenon-paradojas.streamlit.app`.
5. Comparte ese enlace: se puede abrir desde cualquier navegador, sin
   necesidad de instalar nada.

### Opción C — Ejecución local (para pruebas mientras desarrollas)

```bash
pip install -r requirements.txt
streamlit run zenon_paradojas_app.py
```

Esto abre automáticamente `http://localhost:8501` en tu navegador.

---

## 4. Cómo usar la app durante la exposición

1. **Pestaña "Aquiles y la Tortuga":** mueve las velocidades y la ventaja
   inicial, y observa cómo cambian el tiempo/posición de encuentro; sube el
   número de pasos `n` y muestra cómo los "X" rojos (pasos de Zenón) se
   acumulan sobre el punto de encuentro (estrella negra) sin nunca
   sobrepasarlo — visualizando la convergencia de la serie.
2. **Pestaña "Límites laterales":** cambia el tipo de discontinuidad y reduce
   el slider de ε hacia la izquierda; muestra en la tabla cómo `f(x → a⁻)` y
   `f(x → a⁺)` se estabilizan (o no) en un mismo valor, conectando esto con
   la definición formal ε-δ y con la condición de existencia del límite
   bilateral.
