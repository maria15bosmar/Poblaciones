""" Función main. Contiene las funciones pertenecientes al familiador. """

import json, copy
import numpy as np
from utils import *
from planeador import planear
# Tipos de familias.
from tipos_familias.abuelo_nieto import Abuelo_nieto
from tipos_familias.hermanos import Hermanos
from tipos_familias.monopar import Monopar
from tipos_familias.pareja import Pareja
from tipos_familias.unipersonal import Unipersonal
from entidades.persona import Persona

lista_familias = []

tipos_familias = {
    "unipersonal" : Unipersonal,
    "monopar_m" : Monopar,
    "monopar_f" : Monopar,
    "pareja" : Pareja,
    "hermanos" : Hermanos,
    "abuelo_nieto" : Abuelo_nieto
}

with open(PATH_JSON_FAMILIADOR) as f:
    INPUTS_FAMILIADOR = json.load(f)

def familiador():
    """ Crea una familia sintérica con los datos de los censos. """
    global poblacion, num_ciudadanos, lista_familias, casas
    datos = INPUTS_FAMILIADOR["familiador"]["numero_personas"]
    n_pers = np.random.choice(range(1, 8), p=datos)
    if n_pers > len(INPUTS_FAMILIADOR["familiador"]["familias"]):
        return
    familias = INPUTS_FAMILIADOR["familiador"]["familias"][n_pers - 1]
    datos = INPUTS_FAMILIADOR["familiador"][str(n_pers)]
    subtipos = []
    while isinstance(familias, list):
        datos = datos["subtipo"]
        seleccion = np.random.choice(len(datos["probabilidad"]), p=datos["probabilidad"])
        subtipos.append(seleccion)
        familias = familias[seleccion]
    if familias == "nada":
        return
    if familias == "monopar_m":
        generador = tipos_familias[familias](poblacion, num_ciudadanos, n_pers, subtipos, 0)
    elif familias == "monopar_f":
        generador = tipos_familias[familias](poblacion, num_ciudadanos, n_pers, subtipos, 1)
    else:
        generador = tipos_familias[familias](poblacion, num_ciudadanos, n_pers, subtipos)
    if generador.check_posible() != 0:
        return
    nueva_fam = generador.generar_familia(casas)
    if nueva_fam is None:
        return
    lista_familias.append(nueva_fam)
    
if __name__ == "__main__":
    ### POR CADA DISTRITO.:
    num_distritos = INPUT_DATA["num_distritos"]
    for distrito in range(num_distritos):
        Persona.n_pers_distrito = 0
        ## DATOS DE LA POBLACIÓN.
        num_ciudadanos = []
        censo = leer_censo(distrito + 1)
        # Num_ciudadanos es una lista de cuatro números:
        # - cantidad de hombres adultos.
        # - cantidad de mujeres adultas.
        # - cantidad de hombres menos de 24 años.
        # - cantidad de mujeres menos de 24 años.
        for value in censo[2:]:
            num_ciudadanos.append(value)
        # Población es una matriz de 2x96 con una lista de cantidad de hombres
        # por edad y otra de cantidad de mujeres por edad.
        poblacion = np.array([censo[0], censo[1]])
        # Casas es una lista que contiene tres listas de coordenadas:
        # - casas grandes.
        # - casas medianas.
        # - casas pequeñas.
        casas = leer_catastro(distrito + 1)
        casascopia = copy.deepcopy(casas)

        print("DISTRITO", distrito)
        ## CREACIÓN DE FAMILIAS.
        # El bucle continúa hasta que no queden adultos.
        while num_ciudadanos[0] + num_ciudadanos[1] > 0 and Persona.n_pers_distrito < MAX_AGENTES//num_distritos:
            # En caso de quedarse sin casas, se restaura la lista de casas partiendo de una copia.
            if len(casas[0]) == 0 and len(casas[1]) == 0 and len(casas[2]) == 0:
                casas = copy.deepcopy(casascopia)
            # Se crea una nueva familia.
            familiador()
            print(num_ciudadanos[0], num_ciudadanos[1], len(lista_familias))

    ### PLANES.
    # Una vez se obtienen las familias, se les asocia una serie de planes.
    planear(lista_familias)
