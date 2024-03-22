# Funciones extra de la aplicación users.
import random
import string

def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """Esta funcion genera un codigo de 6 letras mayuscuals o numeros de forma aleatoria"""
    return ''.join(random.choice(chars) for _ in range(size))