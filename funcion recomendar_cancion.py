# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 15:14:19 2026

@author: mom
"""

import pandas as pd
import random

categoria_a_mood = {
    "Energético": "Energetic",
    "Feliz":      "Happy",
    "Calmo":      "Calm",
    "Triste":     "Sad"
}

generos_disponibles = ["Pop", "Rock", "Hip-Hop", "Indie", "R&B",
                       "Electronic", "Latin", "Jazz", "Classical"]


def recomendar_cancion(categoria, preferencias, ruta="data_moods.csv"):
    """
    Recomienda una canción según la categoría emocional del día y los
    géneros preferidos del usuario.

    Carga data_moods.csv y filtra las canciones cuyo campo 'mood' coincida
    con la categoría recibida (mapeada del español al inglés del CSV).
    Si el usuario tiene géneros preferidos y alguno aparece en el subconjunto
    filtrado, se prioriza ese subconjunto; si no hay coincidencias de género,
    se usa la totalidad de canciones de esa categoría. Finalmente elige una
    canción al azar con random y retorna sus datos principales.

    Columnas usadas de data_moods.csv:
        - 'mood'   : Energetic | Happy | Calm | Sad
        - 'genre'  : Pop | Rock | Hip-Hop | Indie | R&B |
                     Electronic | Latin | Jazz | Classical
        - 'name'   : Título de la canción.
        - 'artist' : Nombre del artista.

    Args:
        categoria (str): Categoría emocional del día, una de:
                         "Energético", "Feliz", "Calmo" o "Triste".
        preferencias (list[str]): Géneros preferidos del usuario,
                                  por ejemplo ["Pop", "Rock"].
                                  Puede ser lista vacía.
        ruta (str): Ruta al archivo data_moods.csv.
                    Por defecto "data_moods.csv".

    Returns:
        dict: Diccionario con las claves:
              - "nombre"  (str): Título de la canción.
              - "artista" (str): Nombre del artista.
              - "genero"  (str): Género musical de la canción.
        None: Si no hay canciones disponibles para la categoría dada,
              imprime un aviso y retorna None.

    Raises:
        FileNotFoundError: Si no se encuentra el archivo en la ruta indicada.
        KeyError: Si la categoría recibida no está en CATEGORIA_A_MOOD.
    """

    df = pd.read_csv(ruta)

    mood_csv = categoria_a_mood[categoria]
    canciones_categoria = df[df["mood"] == mood_csv]

    if canciones_categoria.empty:
        print(f"No se encontraron canciones para la categoría '{categoria}'.")
        return None

    if preferencias:
        preferencias_norm = [g.strip().title() for g in preferencias]

        canciones_preferidas = canciones_categoria[
            canciones_categoria["genre"].isin(preferencias_norm)
        ]

        if not canciones_preferidas.empty:
            pool = canciones_preferidas
        else:
            pool = canciones_categoria

    else:
        pool = canciones_categoria

    cancion_elegida = pool.sample(n=1).iloc[0]

    resultado = {
        "nombre":  cancion_elegida["name"],
        "artista": cancion_elegida["artist"],
        "genero":  cancion_elegida["genre"]
    }

    return resultado

if __name__ == "__main__":

    casos_prueba = [
        ("Energético", ["Rock", "Pop"]),
        ("Feliz",      ["Jazz"]),
        ("Calmo",      ["Indie", "Classical"]),
        ("Triste",     []),              
        ("Feliz",      ["Kpop"]),       
    ]

    for categoria, prefs in casos_prueba:
        print(f"\nCategoría: {categoria} | Preferencias: {prefs}")
        cancion = recomendar_cancion(
            categoria,
            prefs,
            ruta="Data_Moods__csv_-_data_moods_csv.csv"   
        )
        if cancion:
            print(f"  🎵 {cancion['nombre']} — {cancion['artista']} ({cancion['genero']})")