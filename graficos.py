import pandas as pd
import matplotlib.pyplot as plt
import os
 
 
def generar_graficos(usuario, ruta_historial="historial.csv"):
    """
    Genera tres gráficos con matplotlib a partir del historial del usuario.
 
    1. Evolución del puntaje emocional por día (línea).
    2. Distribución de categorías emocionales (torta).
    3. Géneros musicales más recomendados (barras).
 
    Args:
        usuario        (UsuarioMoodTune): Usuario activo (se usa su nombre).
        ruta_historial (str):             Ruta al CSV de historial.
    """
    if not os.path.exists(ruta_historial):
        print("  Aún no tenés registros guardados.")
        print("  Completá al menos un día antes de ver los gráficos.")
        return
 
    df = pd.read_csv(ruta_historial)
 
    if df.empty:
        print("  El historial está vacío.")
        print("  Completá al menos un día antes de ver los gráficos.")
        return
 
    # Gráfico 1: evolución del puntaje
    plt.figure()
    plt.plot(df["fecha"], df["puntaje"], marker="o", color="#5b8dee")
    plt.title(f"Evolución del ánimo de {usuario.nombre}")
    plt.xlabel("Fecha")
    plt.ylabel("Puntaje (1-10)")
    plt.xticks(rotation=45)
    plt.tight_layout()
 
    # Gráfico 2: distribución de categorías
    conteo_categorias = df["categoria"].value_counts()
    plt.figure()
    plt.pie(conteo_categorias.values,
            labels=conteo_categorias.index,
            autopct="%1.0f%%")
    plt.title(f"Categorías emocionales de {usuario.nombre}")
    plt.tight_layout()
 
    # Gráfico 3: géneros más recomendados
    conteo_generos = df["genero"].value_counts()
    plt.figure()
    plt.bar(conteo_generos.index, conteo_generos.values, color="#f4845f")
    plt.title(f"Géneros más recomendados a {usuario.nombre}")
    plt.xlabel("Género")
    plt.ylabel("Cantidad de veces")
    plt.xticks(rotation=45)
    plt.tight_layout()
 
    plt.show()

