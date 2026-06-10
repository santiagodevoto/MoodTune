import pandas as pd
import matplotlib.pyplot as plt
import os


def generar_graficos(usuario, ruta_historial="historial.csv"):
    """
    Genera tres gráficos con matplotlib a partir del historial del usuario.

    Lee historial.csv y, si hay registros, produce:
      1. Evolución del puntaje emocional por día (gráfico de línea).
      2. Distribución de categorías emocionales (gráfico de torta).
      3. Géneros musicales más recomendados (gráfico de barras).

    Si el archivo no existe o está vacío, avisa por consola y termina
    sin generar ningún gráfico.

    Args:
        usuario (UsuarioMoodTune): El usuario activo. Se usa su nombre
                                   en el título de los gráficos.
        ruta_historial (str): Ruta al CSV de historial.
                              Por defecto "historial.csv".

    Returns:
        None
    """

    if not os.path.exists(ruta_historial):
        print("Aún no tenés registros guardados.")
        print("Completá al menos un día antes de ver los gráficos.")
        return

    df = pd.read_csv(ruta_historial)

    if df.empty:
        print("El historial está vacío.")
        print("Completá al menos un día antes de ver los gráficos.")
        return

    plt.figure()
    plt.plot(df["fecha"], df["puntaje"], marker="o")
    plt.title(f"Evolución del ánimo de {usuario.nombre}")
    plt.xlabel("Fecha")
    plt.ylabel("Puntaje (1-10)")
    plt.xticks(rotation=45)

    conteo_categorias = df["categoria"].value_counts()

    plt.figure()
    plt.pie(conteo_categorias.values, labels=conteo_categorias.index, autopct="%1.0f%%")
    plt.title(f"Categorías emocionales de {usuario.nombre}")

    conteo_generos = df["genero"].value_counts()

    plt.figure()
    plt.bar(conteo_generos.index, conteo_generos.values)
    plt.title(f"Géneros más recomendados a {usuario.nombre}")
    plt.xlabel("Género")
    plt.ylabel("Cantidad de veces")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

