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

## Recorrido del código en orden de ejecución
3.1 Arranque del programa
main()
Archivo: main.py
Es el punto de entrada: la única línea que se ejecuta al correr el programa es la llamada main() al final del archivo. Orquesta todo el resto del sistema.
Cómo funciona:
Imprime el saludo de bienvenida.
Revisa con os.path.exists("usuarios.csv") si ya existe un perfil guardado: si existe, llama a cargar_usuario(); si no, llama a registrar_usuario().
Si el usuario todavía no tiene géneros preferidos configurados, llama a preguntar_preferencias().
Entra en un bucle while que muestra el menú de 4 opciones hasta que el usuario elige "4. Salir".
Retorna: nada (None). Es la función orquestadora; no devuelve datos, solo controla el flujo del programa.

3.2 Gestión del perfil del usuario
Archivo: clase.py
class UsuarioMoodTune
Representa al único usuario del sistema. Guarda en memoria cuatro datos: nombre, generos_preferidos (lista), fecha_registro y historial (lista de registros diarios, distinta del CSV).
registrar_usuario()
Se ejecuta solo la primera vez que se usa el programa, cuando usuarios.csv todavía no existe.
Cómo funciona:
Pide el nombre por consola con input().
Crea un objeto UsuarioMoodTune con ese nombre y una lista de géneros vacía.
Llama a guardar_perfil() para persistirlo en usuarios.csv.
Retorna: el objeto UsuarioMoodTune recién creado.
cargar_usuario(ruta="usuarios.csv")
Se ejecuta en todas las sesiones siguientes a la primera, cuando ya existe un perfil guardado.
Cómo funciona:
Lee usuarios.csv con pandas y toma la primera (y única) fila.
Revisa si el campo de géneros está vacío o es NaN. Si lo está, arma una lista vacía; si no, separa el texto por comas y limpia espacios.
Reconstruye el objeto UsuarioMoodTune con esos datos.
Retorna: el objeto UsuarioMoodTune reconstruido desde el CSV.
guardar_perfil(self, ruta="usuarios.csv")  — método de la clase
Persiste el perfil actual en disco. Se llama tanto desde registrar_usuario() como desde preguntar_preferencias() cada vez que cambian los géneros.
Cómo funciona: arma un diccionario con nombre, géneros (unidos por comas) y fecha de registro, y lo escribe con to_csv(), sobrescribiendo el archivo completo (porque el sistema maneja un solo usuario).
Retorna: nada (None). Imprime una confirmación por consola.
agregar_registro(self, puntaje, categoria, cancion)  — método de la clase
Guarda el registro del día en memoria, dentro del objeto usuario. No escribe en disco: eso lo hace guardar_registro() en main.py, que es una función distinta con un nombre parecido.
Cómo funciona: arma un diccionario con la fecha actual y los datos recibidos, y lo agrega a self.historial con .append().
Retorna: nada (None).

3.3 Configuración de preferencias musicales
Archivo: main.py
preguntar_preferencias(usuario)
Se llama una sola vez, justo después de crear o cargar al usuario, solo si todavía no tiene géneros configurados.
Cómo funciona:
Muestra la lista numerada de generos_disponibles (importada de recomendacion.py).
Pide al usuario que ingrese los números de sus géneros favoritos separados por coma.
Valida cada número (que sea un dígito y esté dentro del rango disponible). Si algo falla, avisa el error y vuelve a pedir todo de nuevo, en un bucle hasta que la entrada sea completamente válida.
Guarda la lista de géneros en usuario.generos_preferidos y llama a usuario.guardar_perfil() para persistirla.
Retorna: list[str] con los géneros elegidos.
3.4 El menú principal y sus 4 opciones
A partir de acá el programa entra en un bucle que se repite hasta que el usuario elige "4. Salir". Cada opción dispara una secuencia distinta de funciones.

Opción 1 — Registrar ánimo del día
Es la secuencia más larga: encadena 4 funciones de 4 archivos distintos.
cuestionario_diario()
Archivo: cuestionario.py
Cómo funciona:
Define 4 preguntas (ánimo, motivación, descanso, productividad) y sus pesos (0.4, 0.3, 0.2, 0.1).
Para cada pregunta, pide una respuesta entre 1 y 10. Si el usuario ingresa algo no numérico o fuera de rango, imprime un error y vuelve a pedir esa misma pregunta (no se propaga ninguna excepción hacia afuera).
Una vez que tiene las 4 respuestas válidas, calcula el puntaje ponderado: suma de respuesta[i] por peso[i].
Retorna: float — el puntaje final del día, entre 1.0 y 10.0.
clasificar_estado(puntaje)
Archivo: clasificacion.py
Cómo funciona: compara el puntaje en cascada contra 3 umbrales (8, 6 y 4) con if/elif/else, y asigna la primera categoría que cumple.
| Rango | Categoría |
|---|---|
| 8 – 10 | Energético |
| 6 – 7.9 | Feliz |
| 4 – 5.9 | Calmo |
| 1 – 3.9 | Triste |
Retorna: str — una de las 4 categorías.
recomendar_cancion(categoria, preferencias, ruta="data_moods.csv")
Archivo: recomendacion.py
Cómo funciona:
Lee data_moods.csv con pandas.
Traduce la categoría al inglés con el diccionario categoria_a_mood (el CSV usa "Energetic", "Happy", "Calm", "Sad") y filtra las canciones de ese mood.
Si no hay ninguna canción para esa categoría, avisa por consola y corta ahí.
Si el usuario tiene géneros preferidos, intenta filtrar además por esos géneros. Si hay coincidencias usa ese subconjunto más chico; si no hay ninguna coincidencia, usa todas las canciones de la categoría.
Elige una canción al azar del subconjunto final con pandas.DataFrame.sample().
Retorna: dict con claves "nombre", "artista" y "genero" si encontró una canción, o None si no había ninguna canción para esa categoría.
guardar_registro(usuario, puntaje, categoria, cancion)
Archivo: main.py
Solo se ejecuta si recomendar_cancion() no devolvió None.
Cómo funciona:
Genera la fecha actual con datetime.now().
Arma una fila con fecha, puntaje, categoría y los datos de la canción.
Si historial.csv no existe, lo crea con encabezados; si ya existe, agrega la fila al final sin repetir encabezados.
Llama a usuario.agregar_registro() para que el registro quede también en memoria, en el objeto usuario.
Retorna: nada (None). Imprime una confirmación por consola.

Opción 2 — Ver gráficos de evolución
generar_graficos(usuario, ruta_historial="historial.csv")
Archivo: graficos.py
Cómo funciona:
Si historial.csv no existe, avisa y corta ahí.
Si existe pero está vacío, avisa y corta ahí también.
Si hay datos, genera tres gráficos con matplotlib: una línea con la evolución del puntaje por fecha, una torta con la distribución de categorías emocionales, y barras con la cantidad de veces que se recomendó cada género.
Muestra los tres con plt.show().
Retorna: nada (None).

Opción 3 — Revisar historial
ver_historial(usuario, ruta_historial="historial.csv")
Archivo: main.py
Cómo funciona:
Si historial.csv no existe, avisa y corta ahí.
Si existe pero está vacío, avisa y corta ahí también.
Si hay datos, imprime la tabla completa por consola con df.to_string(index=False).
Retorna: nada (None). Es la versión "texto plano" de los gráficos: sirve para consultar rápido los registros sin abrir una ventana de matplotlib.

Opción 4 — Salir
No llama a ninguna función adicional. Solo imprime un mensaje de despedida y, como opcion pasa a valer "4", la condición del while se vuelve falsa y el bucle (y el programa) terminan.

## Resultados y salidas del programa
Al usar el sistema, el usuario obtiene:

- **Recomendación musical**: nombre de la canción, artista y género, seleccionada automáticamente según su estado del día y sus preferencias.
- **Historial**: tabla con fecha, puntaje emocional y canción recomendada de cada día registrado.
- **Gráficos**: tres visualizaciones generadas con `matplotlib` que muestran la evolución emocional a lo largo del tiempo, la distribución de sus estados y sus géneros más escuchados.

## Declaracion de IA
Durante el desarrollo de este proyecto se utilizaron herramientas de inteligencia artificial (como ChatGPT o Claude) como una herramienta de asistencia y no reemplazó el proceso de aprendizaje ni la autoría del trabajo.

Principalmente, nos apoyamos en Claude para realizar los diagramas de flujo. Luego de una revision grupal, reenviavamos el diagrama a una nueva comversacion con la IA para que basandose unicamente en ese diagrama proceda a codear. Los codigos fueron siempre revisados dado que sin instrucciones claras, Claude introducia conceptos o formas de codear que no nos eran familiares. Por eso, varias veces le pedimos que simplifique basandose unicamente en lo visto durante la cursada. De esta manera, pudimos ir comprendiendo las lineas del codigo y aprendiendo cosas nuevas. 

El trabajo mas arduo que le solicitamos fue el desarrollo del codigo principal. Le enviamos todos lo codigos y diagramas, solicitandole que detecte errores, verifique los codigos sigan un mismo hilo conductor y que tambien se tome su tiempo. El prompt que utilizamos para el desarrollo fue el siguiente: "Hola claude te voy a subir todos los archivos del programa que estoy creando y necesito que revises que todo funcione de manera coherente, bien y todo funcione en conjunto. En base a todo el programa crea el main (te adjunte el diagrama de flujo del main)."


