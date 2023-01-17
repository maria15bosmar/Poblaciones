""" Define un tipo de familia genérico. """

import json
import numpy as np
from utils import PATH_JSON_FAMILIADOR

class Tipo_familia:
    id_fam = -1
    id_pers = -1
    def __init__(self, poblacion, num_ciudadanos, n_pers) -> None:
        with open(PATH_JSON_FAMILIADOR) as f:
            self.INPUTS_FAMILIADOR = json.load(f)
        self.poblacion = poblacion
        self.num_ciudadanos = num_ciudadanos
        self.personas = []
        self.n_pers = n_pers
        Tipo_familia.id_fam += 1

    def formar_familia(self):
        return self.personas
        
    def quasiadultos(self, cantidad):
        """ Comprueba que existan jóvenes de entre 18 y 24 años. """
        boolean = [0, 0]
        i = 18
        # Se devuelve el número de hombres jóvenes y mujeres jóvenes que quedan.
        while i <= 24 and (boolean[0] < cantidad or boolean[1] < cantidad):
            for gen in range(2):
                if self.poblacion[gen][i] >= 1:
                    boolean[gen] += self.poblacion[gen][i]
            i += 1
        return boolean
    
    def elegir_personas(self, edadmin, edadmax, genero):
        """ Devuelve una edad factible para una persona. """
        # Excepciones a tratar.
        if edadmin == 85:
            edadmax = 95
        # Edad concreta y si no superior (segundo hijo).
        if edadmax == -1:
            edadmax = edadmin + 4
            edad = edadmin
        # Mismo caso que -1 pero para adultos.
        elif edadmax == -3:
            edadmax = edadmin + 4
            edad = edadmin
            if edadmax > 95:
                edadmax = 95
        # Persona con una edad predefinida
        elif edadmax == -2:
            if edadmin >= 27 and edadmin <= 93:
                edad = edadmin
                edadmin = edad - 2
                edadmax = edad + 2
            elif edadmin < 27:
                edad = edadmin
                edadmax = edad + 4
            elif edadmin == 94:
                edad = edadmin
                edadmin = edad - 3
                edadmax = edad + 1
            elif edadmin >= 95:
                edad = edadmin
                edadmin = edad - 4
                edadmax = 95
        # Si no, se hace aleatoriamente
        else:
            edad = np.random.randint(edadmin, edadmax+1)
        # Lista de posibles edades que se van a probar en orden.
        rango = list(range(edad, edadmax+1))
        rango.extend(list(range(edadmin, edad)))
        # Se busca a la persona en el rango determinado.
        for i in rango:
            if self.poblacion[genero][i] > 0:
                self.poblacion[genero][i] -= 1
                if i <= 24: # Si es un niño.
                    self.num_ciudadanos[2 + genero] -= 1
                else: # Si es un adulto.
                    self.num_ciudadanos[genero] -= 1
                return i
        # No se encuentra a una persona.
        if edadmax < 24:   # No quedan hijos en ese rango. Probar con hijos mayores de hasta 24 años.
            return self.elegir_personas(edadmax, 24, genero)
        elif edadmax == 24:  # Probamos para cualquier edad de niño.
            return self.elegir_personas(0, 24, genero)
        # No se encuentran adultos. Hay que probar todos los rangos de edad hasta hallar alguno.
        elif edadmax >= 25:
            if edadmax > 90:
                return self.elegir_personas(25, 34, genero)
            else:
                return self.elegir_personas(edadmin + (edadmax-edadmin+1), edadmax + (edadmax-edadmin+1), genero)
            
    def sexador_hijos(self, numero):
        """ Se da un género a un número de hijos dado. """
        generos = []
        # Se copia el número de niños y de niñas.
        num_nin = self.num_ciudadanos[2:].copy()
        for i in range(numero):
            # Se comprueba que queden personas de un género elegido aleatoriamente.
            while True:
                nuevo = np.random.randint(2)
                # Si se encuentran se resta una persona a la copia.
                if num_nin[nuevo] > 0:
                    num_nin[nuevo]-=1
                    generos.append(nuevo)
                    break
        # Se devuelve el género o la lista de géneros.
        if numero == 1:
            return generos[0]
        return generos
    
    def siguientes_hijos(self, edad1, n_ninyos):
        """ Calcular edades coherentes en caso de que haya más de un hijo en una familia."""
        # Se crea una lista de géneros de los hijos.
        if n_ninyos == 1:
            genero_demas = []
            genero_demas.append(self.sexador_hijos(n_ninyos))
        else:
            genero_demas = self.sexador_hijos(n_ninyos)
        edades, hijos = [edad1], [] # Edades de los hijos y personas nuevas.
        # Seleccionar una diferencia de edad para cada hijo con respecto al anterior.
        elecciones = [0, 1, 2, [3, 9], [10, 20]]
        diferencias = np.random.choice(len(elecciones), n_ninyos, p=self.INPUTS_FAMILIADOR["siguientes_hijos"]["probabilidad_diferencia"])
        # Se establece una edad para cada hijo dadas las diferencias.
        for i in range(n_ninyos):
            # Si la diferencia es un número se suma.
            if diferencias[i] < 3:
                edades.append(edades[-1] + elecciones[diferencias[i]])
            # Si es un rango se calcula la diferencia con probabilidad disminuida.
            else:
                edades.append(edades[-1] + probabilidad_disminuida(elecciones[diferencias[i]][0], elecciones[diferencias[i]][1]))
            # Si no quedan adultos de ese género, se prueba con jóvenes.
            if edades[-1] + 4 > 24 and num_ciudadanos[genero_demas[i]] == 0:
                nuevo_hijo = elegir_personas(20, -1, genero_demas[i])
            else:
                nuevo_hijo = elegir_personas(edades[i], -1, genero_demas[i])
            # Agregar la persona.
            id_pers += 1
            hijos.append(Persona(id_pers, nuevo_hijo, genero_demas[i]))
        return hijos