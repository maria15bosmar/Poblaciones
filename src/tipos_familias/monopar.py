""" Familia monoparental. """

import numpy as np
from tipos_familias.tipo_familia import Tipo_familia
from entidades.persona import Persona

class Monopar(Tipo_familia):
    def __init__(self, poblacion, num_ciudadanos, n_pers, subtipos, genero_padre) -> None:
        super().__init__(poblacion, num_ciudadanos, n_pers, subtipos)
        self.genero_padre = genero_padre

    def check_posible(self):
        if self.num_ciudadanos[self.genero_padre] > 0 and self.num_ciudadanos[2] + self.num_ciudadanos[3] >= self.n_pers - 1:
            return 0
        return -1

    def generar_personas(self):
        self.ninyos, self.monopar = 1, 1
        DATOS_TIPO = self.INPUTS_FAMILIADOR["familiador"][str(self.n_pers)]
        RANGOS_EDAD = self.INPUTS_FAMILIADOR["familiador"]["rangos_edad"]
        # Edad del padre/madre.
        PORC_EDADES = DATOS_TIPO["monopar"]["edad"]
        edad = np.random.choice(range(len(PORC_EDADES)), p=PORC_EDADES)
        padre = self.elegir_personas(RANGOS_EDAD[edad], RANGOS_EDAD[edad+1] - 1, self.genero_padre)
        self.personas.append(Persona(padre, self.genero_padre, 1))
        # Edad y género del primer hijo.
        sexo_hijo = self.sexador_hijos(1)
        if padre <= 38:
            hijo = self.elegir_personas(0, padre-15, sexo_hijo)
        else:
            hijo = self.elegir_personas(0, 24, sexo_hijo)
        self.personas.append(Persona(hijo, sexo_hijo, 0))
        if self.n_pers > 2:
            # Siguiente hijo.
            self.personas.extend(self.siguientes_hijos(hijo, self.n_pers - 2))
            return self.personas