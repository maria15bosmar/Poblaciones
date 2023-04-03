""" Familia de hermanos. """

import numpy as np
from tipos_familias.tipo_familia import Tipo_familia
from entidades.persona import Persona

class Hermanos(Tipo_familia):
    def __init__(self, poblacion, num_ciudadanos, n_pers, subtipos) -> None:
        super().__init__(poblacion, num_ciudadanos, n_pers, subtipos)

    def check_posible(self):
        if self.num_ciudadanos[0] + self.num_ciudadanos[1] > 1:
            return 0
        return -1

    def generar_personas(self):
        # Edad del primero.
        DATOS_TIPO = self.INPUTS_FAMILIADOR["familiador"][str(self.n_pers)]
        RANGOS_EDAD = self.INPUTS_FAMILIADOR["familiador"]["rangos_edad"]
        PORC_EDAD = DATOS_TIPO["hermanos"]["edad"]
        edad = np.random.choice(len(PORC_EDAD), p = PORC_EDAD)
        # Géneros de ambos hermanos.
        PORC_GENERO = DATOS_TIPO["hermanos"]["generos"]
        elecciones = [[0, 0], [1, 1], [0, 1]]
        # Si no queda algún género se fijan.
        if self.num_ciudadanos[0] < 2:
            generos = [1, 1]
        elif self.num_ciudadanos[1] < 2:
            generos = [0, 0]
        elif self.num_ciudadanos[0] == 1 and self.num_ciudadanos[1] == 1:
            generos = [0, 1]
        else:
            generos = elecciones[np.random.choice(3, p=PORC_GENERO)]
        # Para los jóvenes de menos de 24 años hay que comprobar que queden.
        if edad == 0:
            if self.num_ciudadanos[0] > 1 and self.num_ciudadanos[1] > 1:
                h, m = self.quasiadultos(2)
                # Si no quedan personas de un determinado género, se fija al que haya o se cambia la edad.
                if h == 0 and m == 0:
                    edad = 1
                elif h == 1 and m == 1:
                    generos[0] = 0
                    generos[1] = 1
                elif m == 0 and h >= 2:
                    generos[0] = 0
                    generos[1] = 0
                elif h == 0 and m >= 2:
                    generos[0] = 1
                    generos[1] = 1
            else:
                edad = 1
        # Obtener edades y agregar personas.
        edades = self.simplificador(generos, RANGOS_EDAD[edad], RANGOS_EDAD[edad+1]-1)
        for per in range(2):
            self.personas.append(Persona(edades[per], generos[per], 1))

    def simplificador(self, generos, edadmin, edadmax):
        """ Calcular edad de los hermanos. """
        global poblacion
        edades = []
        # Encontrar una edad factible para el primer hermano.
        edades.append(self.elegir_personas(edadmin, edadmax, generos[0]))
        # Calcular la diferencia de edad según una probabilidad.
        elecciones = [[1, 2], [4, 5], [7, 10], [12, 20]]
        asumar = np.random.choice(len(elecciones), p=self.INPUTS_FAMILIADOR["simplificador"]["probabilidad_diferencia"])
        asumar = np.random.randint(elecciones[asumar][0], elecciones[asumar][1] + 1)
        # Aleatoriamente se elige si el hermano 1 es el mayor o el menor (multiplicar asumar por -1).
        if np.random.randint(2):
            asumar*=-1
        # Corregir irregularidades.
        edadprimero = edades[0]
        if edadprimero + asumar > 91: # Para que no se busquen personas de mas de 95
            asumar = 0
        if edadprimero > 91:
            edadprimero = 91
        if edadprimero + asumar <= 24: # Para que no se busquen niños
            asumar = 0
        # Encontrar una edad factible para el segundo hermano.
        edades.append(self.elegir_personas(edadprimero+asumar, -3, generos[1]))
        return edades