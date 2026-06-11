# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 13:36:44 2026

@author: mom
"""

from datetime import datetime
import pandas as pd
import os

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
        self.generos_preferidos = generos_preferidos   
        self.fecha_registro = datetime.now()
        self.historial = []  

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

    Returns:
        UsuarioMoodTune: Usuario recién creado, con historial vacío.
    """
    print("¡Bienvenido a MoodTune! Vamos a crear tu perfil.")
    nombre = input("¿Cuál es tu nombre? ").strip()

    usuario = UsuarioMoodTune(nombre, [])
    usuario.guardar_perfil()
    return usuario


def cargar_usuario(ruta="usuarios.csv"):
   """
    Reconstruye el perfil del usuario desde usuarios.csv.

    Returns:
        UsuarioMoodTune: El usuario cargado.
    """
    df = pd.read_csv(ruta)
    fila = df.iloc[0]
    generos_raw = fila["generos_preferidos"]

    # Manejar el caso en que el campo esté vacío
    if pd.isna(generos_raw) or str(generos_raw).strip() == "":
        generos = []
    else:
        generos = [g.strip() for g in str(generos_raw).split(",") if g.strip()]

    usuario = UsuarioMoodTune(
        nombre=fila["nombre"],
        generos_preferidos=generos
    )
    print(f"Bienvenido de vuelta, {usuario.nombre}.")
    return usuario
