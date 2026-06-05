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
    Se crea una sola vez al registrarse; luego se carga desde usuarios.csv.
    """

    def __init__(self, nombre, generos_preferidos):
        self.nombre = nombre
        self.generos_preferidos = generos_preferidos   # lista, ej: ["pop", "rock"]
        self.fecha_registro = datetime.now()
        self.historial = []   # lista de dicts: {fecha, puntaje, categoria, cancion}

    def guardar_perfil(self, ruta="usuarios.csv"):
        """Guarda el perfil por primera vez en usuarios.csv"""
        datos = {
            "nombre": [self.nombre],
            "generos_preferidos": [",".join(self.generos_preferidos)],
            "fecha_registro": [self.fecha_registro]
        }
        pd.DataFrame(datos).to_csv(ruta, index=False)
        print(f"Perfil de {self.nombre} guardado correctamente.")

    def agregar_registro(self, puntaje, categoria, cancion):
        """Agrega la entrada del día al historial del usuario."""
        entrada = {
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "puntaje": puntaje,
            "categoria": categoria,
            "cancion": cancion
        }
        self.historial.append(entrada)


def registrar_usuario():
    """
    Se ejecuta UNA SOLA VEZ: cuando el usuario usa el sistema por primera vez.
    Crea y devuelve un objeto UsuarioMoodTune.
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
    Carga el perfil ya existente desde usuarios.csv.
    Se usa en todas las sesiones posteriores a la primera.
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
