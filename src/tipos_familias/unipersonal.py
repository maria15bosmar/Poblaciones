""" Unidad unipersonal. """

import numpy as np
from tipos_familias.tipo_familia import Tipo_familia
from entidades.persona import Persona

class Unipersonal(Tipo_familia):
    def __init__(self, poblacion, num_ciudadanos, n_pers, subtipos) -> None:
        super().__init__(poblacion, num_ciudadanos, n_pers, subtipos)

    def check_posible(self):
        if self.num_ciudadanos[0] + self.num_ciudadanos[1] > 0:
            return 0
        return -1

    def generar_personas(self):
        # Listas de probabilidad para numpy.
        PORC_EDAD = self.INPUTS_FAMILIADOR["familiador"]["1"]["edad"]
        PORC_GENERO = self.INPUTS_FAMILIADOR["familiador"]["1"]["genero"]
        RANGOS_EDAD = self.INPUTS_FAMILIADOR["familiador"]["rangos_edad"]
        # Seleccionamos edad y género.
        edad = np.random.choice(len(PORC_EDAD), p=PORC_EDAD)
        genre_prob = PORC_GENERO[edad]
        # Para el rango de edad de jóvenes de menos de 24 años hay que comprobar que queden jóvenes.
        if edad == 0:
            h, m = self.quasiadultos(1)
            # Si no quedan jóvenes, se pasa a adultos.
            if h == 0 and m == 0:
                edad = 1
                genero = np.random.choice(2, p = [1-genre_prob, genre_prob])
                if self.num_ciudadanos[0] < 1:
                    genero = 1
                elif self.num_ciudadanos[1] < 1:
                    genero = 0
            # Si no quedan jóvenes de algún género se fija al que haya.
            elif h <= 0:
                genero = 1
            elif m <= 0:
                genero = 0
            else:
                genero = np.random.choice(2, p=[1-genre_prob, genre_prob])
        # Para adultos de más de 24 años.
        else:
            genero = np.random.choice(2, p=[1-genre_prob, genre_prob])
            if self.num_ciudadanos[0] < 1:
                genero = 1
            elif self.num_ciudadanos[1] < 1:
                genero = 0
        # Obtener la edad y agregar la persona.
        unipersonal = self.elegir_personas(RANGOS_EDAD[edad], RANGOS_EDAD[edad+1]-1, genero)
        self.personas.append(Persona(unipersonal, genero))
        return self.personas
