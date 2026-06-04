# MoodTune
Creado por Santiago Devoto, Ramon Otero Monegur, Mia Blaquier, Alfonso Bujan y Wenceslao Grosse Garros. 

# Objetivo y descripción general
MoodTune es un sistema de recomendación musical que registra el estado emocional diario del usuario mediante un cuestionario sencillo y le sugiere una canción acorde. Combina el registro personal de emociones con recomendación automática para brindar una experiencia personalizada y cotidiana.

El sistema trabaja exclusivamente con el estado emocional **autopercibido y reportado** por el usuario. No realiza diagnósticos ni evaluaciones clínicas de ningún tipo.

# Principales funcionalidades
- Registro de perfil con preferencias musicales
- Cuestionario diario de estado de ánimo (respuestas del 1 al 10)
- Clasificación automática en 5 categorías emocionales
- Recomendación de canciones personalizada según categoría y géneros favoritos
- Historial personal con fecha, puntaje y canción recomendada
- Gráficos de evolución emocional a lo largo del tiempo

# Fuente de datos 
La base de canciones se encuentra en un archivo `data_moods.csv` que se encuentra dentro de un proyecto de Github que contiene la clasificacion de diversas canciones mostrando su titulo, artista, album, estado emocional, entre varias otras categorias. 

# Librerias utilizadas
- pandas: Almacenar y leer registros diarios.
- matplotlib: Generar graficos
- datetime: Registrar fecha de cada entrada diaria
- random: Seleccion aleatoria entre canciones del mismo mood
  
# Funciones principales

### `preguntar_preferencias(usuario)`
Muestra los géneros musicales disponibles y le pide al usuario que elija sus favoritos. Valida que haya seleccionado al menos uno (reintenta si no) y guarda las preferencias en `usuarios.csv`. Retorna las preferencias para usarlas en la recomendación.

### `cuestionario_diario()`
Presenta las 4 preguntas de estado de ánimo con respuestas del 1 al 10 (por ejemplo: *¿Cuánta energía tenés hoy?*, *¿Qué tan motivado te sentís?*). Valida que cada respuesta sea un entero en el rango válido y, al terminar, calcula y retorna un **puntaje ponderado** (cada pregunta tiene un peso distinto según su relevancia).

### `clasificar_estado(puntaje)`
Recibe el puntaje ponderado y lo clasifica en una de las 5 categorías emocionales:

| Rango | Categoría |
|---|---|
| 8 – 10 | Energético |
| 6 – 7.9 | Motivado |
| 4 – 5.9 | Calmo |
| 2 – 3.9 | Ansioso |
| 1 – 1.9 | Triste |

### `recomendar_cancion(categoria, preferencias)`
Carga `data_moods.csv` y filtra por la categoría emocional. Si el usuario tiene géneros preferidos, los prioriza cuando hay coincidencias. Selecciona una canción al azar con `random` y retorna nombre, artista y género.

### `guardar_registro(usuario, fecha, puntaje, categoria, cancion)`
Arma una fila con los datos del día y la agrega a `historial.csv` usando `pandas`. Es un flujo completamente lineal.

### `generar_graficos(usuario)`
Lee el historial del usuario. Si no hay registros, avisa y termina. Si hay datos, genera con `matplotlib` tres gráficos:
- Evolución del puntaje emocional por día
- Distribución de categorías emocionales
- Géneros musicales más recomendados

# Resultados y salidas del programa
Al usar el sistema, el usuario obtiene:

- **Recomendación musical**: nombre de la canción, artista y género, seleccionada automáticamente según su estado del día y sus preferencias.
- **Historial**: tabla con fecha, puntaje emocional y canción recomendada de cada día registrado.
- **Gráficos**: tres visualizaciones generadas con `matplotlib` que muestran la evolución emocional a lo largo del tiempo, la distribución de sus estados y sus géneros más escuchados.

# Declaracion de IA
Durante el desarrollo de este proyecto se utilizaron herramientas de inteligencia artificial (como ChatGPT o Claude) como una herramienta de asistencia y no reemplazó el proceso de aprendizaje ni la autoría del trabajo.
