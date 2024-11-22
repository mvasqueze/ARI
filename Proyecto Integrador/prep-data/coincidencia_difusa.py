from rapidfuzz import fuzz

def comparar_frases(frase1, frase2, umbral):
    """
    Compara dos frases y determina si su coincidencia es igual o superior al umbral.
    
    Parámetros:
    - frase1 (str): Primera frase a comparar.
    - frase2 (str): Segunda frase a comparar.
    - umbral (int): Puntaje mínimo para considerar una coincidencia (0-100).
    
    Retorna:
    - bool: True si la coincidencia es mayor o igual al umbral, False en caso contrario.
    """
    if not frase1 or not frase2:
        return False  # Si alguna frase está vacía, no hay coincidencia.
    
    puntaje = fuzz.ratio(frase1, frase2)
    return puntaje >= umbral

'''# Ejemplo de uso
frase1 = "El poblao"
frase2 = "El Poblado"

resultado = comparar_frases(frase1, frase2)
print(f"Las frases son similares: {resultado}")'''
