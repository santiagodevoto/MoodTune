def clasificar_estado(puntaje):
    """
    Clasifica el estado de ánimo del usuario según su puntaje emocional.

    Toma el puntaje ponderado del cuestionario diario y lo ubica en una de
    las cuatro categorías de la base de canciones, comparándolo en cascada
    contra los rangos definidos. Devuelve la primera categoría cuyo límite
    inferior cumple el puntaje. Las categorías coinciden con los valores de
    la columna 'mood' de data_moods.csv, para poder filtrar canciones luego.

    Rangos:
        Energético : 8 a 10
        Feliz     : 6 a 7.9
        Calmo      : 4 a 5.9
        Triste       : menor a 4 (1 a 3.9)

    Args:
        puntaje (float): Puntaje emocional del día, en la escala de 1 a 10.

    Returns:
        str: Categoría emocional correspondiente. Uno de:
             "Energético", "Feliz", "Calmo" o "Triste".
    """
    if puntaje >= 8:
        categoria = "Energético"
    elif puntaje >= 6:
        categoria = "Feliz"
    elif puntaje >= 4:
        categoria = "Calmo"
    else:
        categoria = "Triste"

    return categoria
