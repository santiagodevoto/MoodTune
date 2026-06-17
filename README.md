# MoodTune
Creado por Santiago Devoto, Ramon Otero Monegur, Mia Blaquier, Alfonso Bujan y Wenceslao Grosse Garros. 

## Objetivo y descripción general
MoodTune es un sistema de recomendación musical que registra el estado emocional diario del usuario mediante un cuestionario sencillo y le sugiere una canción acorde. Combina el registro personal de emociones con recomendación automática para brindar una experiencia personalizada y cotidiana.

El sistema trabaja exclusivamente con el estado emocional **autopercibido y reportado** por el usuario. No realiza diagnósticos ni evaluaciones clínicas de ningún tipo.

## Principales funcionalidades
- Registro de perfil con preferencias musicales
- Cuestionario diario de estado de ánimo (respuestas del 1 al 10)
- Clasificación automática en 4 categorías emocionales
- Recomendación de canciones personalizada según categoría y géneros favoritos
- Historial personal con fecha, puntaje y canción recomendada
- Gráficos de evolución emocional a lo largo del tiempo

## Estructura del proyecto
El programa está dividido en módulos, cada uno con una responsabilidad puntual:

- **`main.py`**: punto de entrada del programa. Muestra el menú principal, pide las preferencias musicales la primera vez y coordina las llamadas al resto de los módulos.
- **`clase.py`**: define la clase `UsuarioMoodTune` y las funciones `registrar_usuario()` y `cargar_usuario()`, que crean y reconstruyen el perfil del usuario a partir de `usuarios.csv`.
- **`cuestionario.py`**: contiene `cuestionario_diario()`, que hace las 4 preguntas del día y calcula el puntaje ponderado.
- **`clasificacion.py`**: contiene `clasificar_estado(puntaje)`, que traduce ese puntaje en una categoría emocional.
- **`recomendacion.py`**: contiene `recomendar_cancion()` y la lista `generos_disponibles`, usadas para filtrar y elegir una canción de `data_moods.csv` según la categoría y los géneros preferidos.
- **`graficos.py`**: contiene `generar_graficos()`, que dibuja los tres gráficos a partir de `historial.csv`.

## Fuente de datos 
La base de canciones se encuentra en un archivo `data_moods.csv` que se encuentra dentro de un proyecto de Github que contiene la clasificacion de diversas canciones mostrando su titulo, artista, album, estado emocional, entre varias otras categorias. 

## Librerias utilizadas
- pandas: Almacenar y leer registros diarios.
- matplotlib: Generar graficos
- datetime: Registrar fecha de cada entrada diaria
- random: Seleccion aleatoria entre canciones del mismo mood
- os: Verificar si ya existen `usuarios.csv` o `historial.csv` antes de leerlos o crearlos
  
  
## Funciones principales

### `registrar_usuario()` y `cargar_usuario(ruta="usuarios.csv")`
Manejan el ciclo de vida del perfil. `registrar_usuario()` se ejecuta la primera vez que se usa el sistema: pide el nombre, crea un objeto `UsuarioMoodTune` con historial vacío y lo guarda en `usuarios.csv`. En las sesiones siguientes, `cargar_usuario()` reconstruye ese mismo perfil leyendo el CSV.

### `preguntar_preferencias(usuario)`
Muestra los géneros musicales disponibles y le pide al usuario que elija sus favoritos. Valida que haya seleccionado al menos uno (reintenta si no) y guarda las preferencias en `usuarios.csv` a través de `usuario.guardar_perfil()`. Retorna las preferencias para usarlas en la recomendación.

### `cuestionario_diario()`
Presenta 4 preguntas sobre el bienestar del día (estado de ánimo, motivación, descanso y productividad) con respuestas del 1 al 10. Valida que cada respuesta sea un entero en el rango válido y, al terminar, calcula y retorna un **puntaje ponderado** (cada pregunta tiene un peso distinto según su relevancia).

### `clasificar_estado(puntaje)`
Recibe el puntaje ponderado y lo clasifica en una de las 4 categorías emocionales:

| Rango | Categoría |
|---|---|
| 8 – 10 | Energético |
| 6 – 7.9 | Feliz |
| 4 – 5.9 | Calmo |
| 1 – 3.9 | Triste |

### `recomendar_cancion(categoria, preferencias, ruta="data_moods.csv")`
Carga `data_moods.csv` y filtra por la categoría emocional. Si el usuario tiene géneros preferidos, los prioriza cuando hay coincidencias; si no, usa todas las canciones de esa categoría. Selecciona una canción al azar con `random` y retorna nombre, artista y género.

### `guardar_registro(usuario, puntaje, categoria, cancion)`
Arma una fila con la fecha del día (generada internamente con `datetime`), el puntaje, la categoría y los datos de la canción, y la agrega a `historial.csv` usando `pandas`. También actualiza el historial en memoria del usuario.

### `generar_graficos(usuario, ruta_historial="historial.csv")`
Lee el historial del usuario. Si no hay registros, avisa y termina. Si hay datos, genera con `matplotlib` tres gráficos:
- Evolución del puntaje emocional por día
- Distribución de categorías emocionales
- Géneros musicales más recomendados

## Resultados y salidas del programa
Al usar el sistema, el usuario obtiene:

- **Recomendación musical**: nombre de la canción, artista y género, seleccionada automáticamente según su estado del día y sus preferencias.
- **Historial**: tabla con fecha, puntaje emocional y canción recomendada de cada día registrado.
- **Gráficos**: tres visualizaciones generadas con `matplotlib` que muestran la evolución emocional a lo largo del tiempo, la distribución de sus estados y sus géneros más escuchados.

## Declaracion de IA
Durante el desarrollo de este proyecto se utilizaron herramientas de inteligencia artificial (como ChatGPT o Claude) como una herramienta de asistencia y no reemplazó el proceso de aprendizaje ni la autoría del trabajo.

Principalmente, nos apoyamos en Claude para realizar los diagramas de flujo. Luego de una revision grupal, reenviavamos el diagrama a una nueva comversacion con la IA para que basandose unicamente en ese diagrama proceda a codear. Los codigos fueron siempre revisados dado que sin instrucciones claras, Claude introducia conceptos o formas de codear que no nos eran familiares. Por eso, varias veces le pedimos que simplifique basandose unicamente en lo visto durante la cursada. De esta manera, pudimos ir comprendiendo las lineas del codigo y aprendiendo cosas nuevas. 

El trabajo mas arduo que le solicitamos fue el desarrollo del codigo principal. Le enviamos todos lo codigos y diagramas, solicitandole que detecte errores, verifique los codigos sigan un mismo hilo conductor y que tambien se tome su tiempo. El prompt que utilizamos para el desarrollo fue el siguiente: "Hola claude te voy a subir todos los archivos del programa que estoy creando y necesito que revises que todo funcione de manera coherente, bien y todo funcione en conjunto. En base a todo el programa crea el main (te adjunte el diagrama de flujo del main)."


