# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 13:36:44 2026

@author: mom
"""

from datetime import datetime
import pandas as pd

class UsuarioMoodTune:
    """
   Representa al único usuario del sistema MoodTune.

    Centraliza los datos del perfil y el historial de registros diarios.
    Se instancia una sola vez al registrarse (registrar_usuario) y, en las
    sesiones siguientes, se reconstruye desde usuarios.csv (cargar_usuario).

    Attributes:
        nombre (str): Nombre del usuario.
        generos_preferidos (list[str]): Géneros preferidos, ej. ["pop", "rock"].
        fecha_registro (datetime): Momento en que se creó el objeto.
        historial (list[dict]): Registros diarios; cada dict tiene las claves
            'fecha', 'puntaje', 'categoria' y 'cancion'.
    """

    def __init__(self, nombre, generos_preferidos):
        """
        Inicializa el perfil del usuario con un historial vacío.

        Fija fecha_registro con la fecha y hora actuales e inicializa
        historial como lista vacía.

        Args:
            nombre (str): Nombre del usuario.
            generos_preferidos (list[str]): Lista de géneros preferidos.
        """
        self.nombre = nombre
        self.generos_preferidos = generos_preferidos   # lista, ej: ["pop", "rock"]
        self.fecha_registro = datetime.now()
        self.historial = []   # lista de dicts: {fecha, puntaje, categoria, cancion}

    def guardar_perfil(self, ruta="usuarios.csv"):
       """
        Guarda el perfil del usuario en un archivo CSV.

        Escribe nombre, géneros preferidos (unidos por comas) y fecha de
        registro en una única fila. Como MoodTune maneja un solo usuario,
        el archivo se sobrescribe por completo en cada llamada. Imprime una
        confirmación por consola.

        Args:
            ruta (str): Ruta del archivo de salida. Por defecto "usuarios.csv".

        Returns:
            None
        """
       datos = {
            "nombre": [self.nombre],
            "generos_preferidos": [",".join(self.generos_preferidos)],
            "fecha_registro": [self.fecha_registro]
        }
       pd.DataFrame(datos).to_csv(ruta, index=False)
       print(f"Perfil de {self.nombre} guardado correctamente.")

    def agregar_registro(self, puntaje, categoria, cancion):
        """
        Agrega el registro del día al historial en memoria del usuario.

        Construye una entrada con la fecha actual (formato YYYY-MM-DD) y los
        datos recibidos, y la añade a self.historial. No persiste en disco.

        Args:
            puntaje (float): Puntaje emocional del día (escala 1 a 10).
            categoria (str): Categoría emocional asignada (p. ej. "Calmo").
            cancion (str): Canción recomendada para ese día.

        Returns:
            None
        """
        entrada = {
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "puntaje": puntaje,
            "categoria": categoria,
            "cancion": cancion
        }
        self.historial.append(entrada)


def registrar_usuario():
    """
   Crea el perfil del usuario la primera vez que usa el sistema.

   Solicita por consola el nombre y los géneros preferidos, construye un
   objeto UsuarioMoodTune y guarda el perfil en usuarios.csv. Está pensada
   para ejecutarse una sola vez (cuando todavía no existe el archivo de perfil).

   Returns:
       UsuarioMoodTune: El usuario recién creado, con historial vacío.
   """
    print("¡Bienvenido a MoodTune! Vamos a crear tu perfil.")
    nombre = input("¿Cuál es tu nombre? ").strip()
    generos = input("¿Qué géneros musicales preferís? (separados por coma): ").strip()
    generos_lista = [g.strip() for g in generos.split(",")]

    usuario = UsuarioMoodTune(nombre, generos_lista)
    usuario.guardar_perfil()
    return usuario


def cargar_usuario(ruta="usuarios.csv"):
   """
    Reconstruye el perfil del usuario desde usuarios.csv.

    Lee la primera (y única) fila del archivo y crea un UsuarioMoodTune con
    el nombre y los géneros preferidos guardados. Se usa en todas las
    sesiones posteriores a la primera. Imprime un saludo de bienvenida.

    Nota: solo se restauran nombre y géneros. fecha_registro se reinicia al
    momento actual e historial arranca vacío, ya que el CSV de perfil no
    almacena esos datos.

    Args:
        ruta (str): Ruta del archivo de perfil. Por defecto "usuarios.csv".

    Returns:
        UsuarioMoodTune: El usuario cargado.

    Raises:
        FileNotFoundError: Si no existe el archivo en la ruta indicada.
    """
   df = pd.read_csv(ruta)
   fila = df.iloc[0]
   usuario = UsuarioMoodTune(
        nombre=fila["nombre"],
        generos_preferidos=fila["generos_preferidos"].split(",")
    )
   print(f"Bienvenido de vuelta, {usuario.nombre}.")
   return usuario

import os

if os.path.exists("usuarios.csv"):
    usuario = cargar_usuario()       # sesiones 2, 3, 4...
else:
    usuario = registrar_usuario()    # solo la primera vez
