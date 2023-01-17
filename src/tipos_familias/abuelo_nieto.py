""" Familia formada por un abuelo y un nieto. """

import numpy as np
from tipos_familias.tipo_familia import Tipo_familia
from persona import Persona

class Abuelo_nieto(Tipo_familia):
    def __init__(self, poblacion, num_ciudadanos, n_pers, subtipos) -> None:
        super().__init__(poblacion, num_ciudadanos, n_pers, subtipos)

    def check_posible(self):
        if self.num_ciudadanos[0] + self.num_ciudadanos[1] > 1 and self.num_ciudadanos[2] + self.num_ciudadanos[3] > 0:
            return 0
        return -1

    def generar_personas(self):
        self.ninyos, self.monopar = 1, 1
        DATOS_TIPO = self.INPUTS_FAMILIADOR["familiador"][str(self.n_pers)]
        PORC_GENERO = DATOS_TIPO["abuelo_nieto"]["genero"]
        generos = []
        for i in range(2):
            generos.append(np.random.choice(2, p=[1 - PORC_GENERO[i], PORC_GENERO[i]]))
        # Si no quedan ciudadanos adultos de algún tipo, se usa el otro género.
        if self.num_ciudadanos[0] < 1:
            generos[1] = 1
        elif self.num_ciudadanos[1] < 1:
            generos[1] = 0
        edades = np.random.choice(range(34, 86, 10), p=DATOS_TIPO["abuelo_nieto"]["edad_abuelo"])
        abuelo = self.elegir_personas(edades, edades + 9, generos[1])
        self.personas.append(Persona(Tipo_familia.id_pers, abuelo, generos[1]))
        Tipo_familia.id_pers += 1
        # Nieto.
        PORC_EDAD_NIETO = DATOS_TIPO["abuelo_nieto"]["edad_nieto"]
        # Si no quedan adultos, se escoge un niño y viceversa.
        seleccion = np.random.choice(7, p=PORC_EDAD_NIETO)
        rangos = ((0, 9), (10, 19), (20, 24), (25, 29), (30, 34), (35, 39),
            (40, 50))
        if seleccion < 3 and self.num_ciudadanos[generos[0] + 2] < 1:
            if self.num_ciudadanos[generos[0]] < 1:
                generos[0] = int(not generos[0])
            else:
                seleccion = 3
        elif seleccion >= 3 and self.num_ciudadanos[generos[0]] < 1:
            if self.num_ciudadanos[generos[0] + 2] < 1:
                generos[0] = int(not generos[0])
            else:
                seleccion = 0
        nieto = self.elegir_personas(rangos[seleccion][0], rangos[seleccion][1], generos[0])
        self.personas.append(Persona(Tipo_familia.id_pers, nieto, generos[0]))
        Tipo_familia.id_pers += 1
