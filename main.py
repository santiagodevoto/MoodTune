import os
import pandas as pd
from datetime import datetime

from clase import registrar_usuario, cargar_usuario
from cuestionario import cuestionario_diario
from clasificacion import clasificar_estado
from recomendacion import recomendar_cancion, generos_disponibles
from graficos import generar_graficos


def preguntar_preferencias(usuario):
    """
    Muestra los géneros disponibles y pide al usuario que elija sus favoritos.
    Valida que se elija al menos uno y guarda las preferencias en el perfil.

    Args:
        usuario (UsuarioMoodTune): El usuario cuyas preferencias se van a fijar.

    Returns:
        list[str]: Lista de géneros seleccionados por el usuario.
    """
    print("\nEstos son los géneros disponibles:")
    for i in range(len(generos_disponibles)):
        print(str(i + 1) + ". " + generos_disponibles[i])

    preferencias = []

    while len(preferencias) == 0:
        entrada = input("\nIngresá los números de tus géneros favoritos separados por coma (ejemplo: 1,3,5): ")
        partes = entrada.split(",")

        preferencias = []
        hay_error = False

        for parte in partes:
            parte = parte.strip()

            if parte.isdigit():
                indice = int(parte) - 1

                if indice >= 0 and indice < len(generos_disponibles):
                    preferencias.append(generos_disponibles[indice])
                else:
                    print("El número " + parte + " no corresponde a ningún género. Intentá de nuevo.")
                    hay_error = True
                    break
            else:
                print("'" + parte + "' no es un número válido. Intentá de nuevo.")
                hay_error = True
                break

        if hay_error:
            preferencias = []

    print("Géneros guardados: " + ", ".join(preferencias))

    usuario.generos_preferidos = preferencias
    usuario.guardar_perfil("usuarios.csv")

    return preferencias


def guardar_registro(usuario, puntaje, categoria, cancion):
    """
    Guarda el registro del día en historial.csv y en el historial del usuario.

    Si el archivo no existe lo crea con encabezados.
    Si ya existe, agrega la nueva fila al final.

    Args:
        usuario   (UsuarioMoodTune): Usuario activo.
        puntaje   (float): Puntaje ponderado del día.
        categoria (str): Categoría emocional del día.
        cancion   (dict): Diccionario con claves 'nombre', 'artista', 'genero'.
    """
    fecha = datetime.now().strftime("%Y-%m-%d")

    nueva_fila = {
        "fecha": fecha,
        "puntaje": puntaje,
        "categoria": categoria,
        "cancion": cancion["nombre"],
        "artista": cancion["artista"],
        "genero": cancion["genero"]
    }

    df_nueva = pd.DataFrame([nueva_fila])

    if os.path.exists("historial.csv"):
        df_nueva.to_csv("historial.csv", mode="a", header=False, index=False)
    else:
        df_nueva.to_csv("historial.csv", mode="a", header=True, index=False)

    usuario.agregar_registro(puntaje, categoria, cancion["nombre"])

    print("Registro del " + fecha + " guardado correctamente.")


def main():
    print("Bienvenido a MoodTune!")

    if os.path.exists("usuarios.csv"):
        usuario = cargar_usuario("usuarios.csv")
    else:
        usuario = registrar_usuario()

    if len(usuario.generos_preferidos) == 0 or usuario.generos_preferidos == [""]:
        print("\nTodavía no tenés géneros favoritos configurados.")
        preguntar_preferencias(usuario)

    opcion = ""

    while opcion != "3":
        print("\n" + "-" * 40)
        print("Hola, " + usuario.nombre + "!")
        print("1. Registrar ánimo del día")
        print("2. Ver gráficos de evolución")
        print("3. Salir")
        print("-" * 40)

        opcion = input("Elegí una opción (1-3): ")

        if opcion == "1":
            print("\n-- Cuestionario diario --")
            puntaje = cuestionario_diario()
            categoria = clasificar_estado(puntaje)

            print("\nPuntaje del día: " + str(round(puntaje, 1)) + " → " + categoria)

            cancion = recomendar_cancion(categoria, usuario.generos_preferidos, "data_moods.csv")

            if cancion != None:
                print("\nCanción recomendada:")
                print("  " + cancion["nombre"] + " — " + cancion["artista"])
                print("  Género: " + cancion["genero"])
                guardar_registro(usuario, puntaje, categoria, cancion)
            else:
                print("No se encontró ninguna canción. Revisá data_moods.csv.")

        elif opcion == "2":
            generar_graficos(usuario, "historial.csv")

        elif opcion == "3":
            print("\n¡Hasta pronto, " + usuario.nombre + "!")

        else:
            print("Opción inválida. Ingresá 1, 2 o 3.")


main()
