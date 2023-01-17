""" Familia monoparental. """

import numpy as np
from tipo_familia import Tipo_familia
from persona import Persona

class Monopar(Tipo_familia):
    def __init__(self, poblacion, num_ciudadanos) -> None:
        super().__init__(poblacion, num_ciudadanos)

    def formar_familia(self, genero_padre):
        ninyos, monopar = 1, 1
        DATOS_TIPO3 = self.INPUTS_FAMILIADOR["familiador"][str(self.n_pers)]
        RANGOS_EDAD = self.INPUTS_FAMILIADOR["familiador"]["rangos_edad"]
        # Edad del padre/madre.
        PORC_EDADES = DATOS_TIPO3["monopar"]["edad"]
        edad = np.random.choice(range(1,6), 1, p=PORC_EDADES)[0]
        padre = self.elegir_personas(RANGOS_EDAD[edad], RANGOS_EDAD[edad+1]-1, genero_padre)
        self.personas.append(Persona(Tipo_familia.id_pers, padre, genero_padre))
        Tipo_familia.id_pers += 1
        # Edad y género del primer hijo.
        sexo_hijo = self.sexador_hijos(1)
        if padre <= 38:
            hijo = self.elegir_personas(0, padre-15, sexo_hijo)
        else:
            hijo = self.elegir_personas(0, 24, sexo_hijo)
        self.personas.append(Persona(id_pers, hijo, sexo_hijo))
        id_pers += 1
        # Siguiente hijo.
        self.personas.extend(siguientes_hijos( hijo, 1))
        return self.personas