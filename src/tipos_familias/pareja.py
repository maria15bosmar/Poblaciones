""" Familia de pareja. """

from tipos_familias.tipo_familia import Tipo_familia
from entidades.persona import Persona
import numpy as np
from utils import probabilidad_disminuida

class Pareja(Tipo_familia):
    def __init__(self, poblacion, num_ciudadanos, n_pers, subtipos) -> None:
        super().__init__(poblacion, num_ciudadanos, n_pers, subtipos)

    def check_posible(self):
        if self.num_ciudadanos[0] + self.num_ciudadanos[1] > 1:
            if self.n_pers > 2:
                if self.num_ciudadanos[2] + self.num_ciudadanos[3] > self.n_pers - 2:
                    return 0
            else:
                return 0
        return -1

    def generar_personas(self):
        DATOS_TIPO = self.INPUTS_FAMILIADOR["familiador"][str(self.n_pers)]
        if self.n_pers > 2:
            self.ninyos = 1
            # Género y edad del primer hijx.
            sexo_hijo = self.sexador_hijos(1)
            edad_hijo = self.elegir_personas(0, 24, sexo_hijo)
            self.personas.append(Persona(edad_hijo, sexo_hijo))
            # Pareja.
            PORC_EDAD_MADRE = DATOS_TIPO["pareja"]["edad_madre"]
            seleccion = np.random.choice(range(15, 46, 5), p=PORC_EDAD_MADRE)
            edad_madre = np.random.randint(seleccion, seleccion+5)
            self.personas.extend(self.parejador(edad_madre+edad_hijo))
            # Resto de hijxs.
            self.personas.extend(self.siguientes_hijos(edad_hijo, 1))
        else:
            pers1, pers2 = self.parejador(0)
            self.personas += [pers1, pers2]
        return self.personas

    def parejador(self, hay_ninyos):
        """ Devuelve una pareja facible. """
        EDADES = [18, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]
        PORC_EDAD = self.INPUTS_FAMILIADOR["parejador"]["edad_porcentajes"]
        # Elegir la edad de la primera persona (normalmente la mujer en parejas heterosexuales).
        # Se hace en función de la edad del hijo.
        for ind, ninyos in enumerate(range(25, 75, 5)):
            if hay_ninyos >= ninyos and hay_ninyos <= ninyos+4:
                age_range1 = ind + 1
        if hay_ninyos <= 24 and hay_ninyos > 0:
            age_range1 = 0
        # Si no hay niños el range de edad es aleatorio.
        if hay_ninyos == 0:
            age_range1 = np.random.choice(len(PORC_EDAD), p=PORC_EDAD)
        # Se elige la edad de la primera persona.
        # Tener en cuenta la diferencia de edad madre/hijo para madres jóvenes.
        if age_range1 == 0:
            if hay_ninyos != 0:
                if hay_ninyos < 18:
                    age1 = 18
                else:
                    age1 = hay_ninyos
            # Si no quedan posibles madres jóvenes se pasa a adultas.
            if self.quasiadultos(2)[1] == 0:
                age1 = 25
            else:
                aux = EDADES[age_range1 + 1]
                age1 = np.random.randint(aux, aux + 5)
        # Si no hay problemas se elige aleatoriamente la primera edad.
        else:
            aux = EDADES[age_range1]
            age1 = np.random.randint(aux, aux + 5)
        # Se elige si es homogamia, hipogamia (alta/baja) o hipergamia (alta/baja) según unas probabilidades.
        tipo_pareja = np.random.choice(5, p=self.INPUTS_FAMILIADOR["parejador"]["probabilidad_diferencia"][age_range1])
        # La diferencia de edad es fija si no es muy elevada.
        posible_dif = self.INPUTS_FAMILIADOR["parejador"]["diferencia_edad"][tipo_pareja]
        if type(posible_dif) is int:
            diferencia = posible_dif
        else:
            if tipo_pareja <= 3:
                diferencia = np.random.choice(posible_dif)
            # Si la diferencia es elevada se calcula con una probabilidad disminuída.
            else:
                diferencia_base = np.random.choice(posible_dif)
                diferencia = probabilidad_disminuida(diferencia_base, diferencia_base+5)
                if tipo_pareja == 5:
                    diferencia *= -1
        # Se obtiene la segunda edad dada la diferencia.
        age2 = age1 + diferencia
        if age2 > 95:
            age2 = 95
        ages = [age2, age1]
        # Se comprueba que existan dos por genero para parejas homosexuales.
        if age1 <= 24 or age2 <= 24:
            gens = self.quasiadultos(2)
            for i in range(2):
                if gens[i] < 2 and ages[i] <= 24:
                    ages[i] = 25
        # Se elige tipo de pareja.
        # Si solo hay hombres, gay. Si solo hay mujeres, lesbianas. Si hay uno de cada, heteros.
        elecciones = ((0, 0), (1, 1), (1, 0))
        tipo = elecciones[np.random.choice(3, p=self.INPUTS_FAMILIADOR["parejador"]["tipo_pareja"])]
        if self.num_ciudadanos[0] < 1:
            tipo = (1, 1)
        elif self.num_ciudadanos[1] < 1:
            tipo = (0, 0)
        elif self.num_ciudadanos[0] == 1 and self.num_ciudadanos[1] == 1:
            tipo = (1, 0)
        # Obtener las personas y devolverlas.
        age1 = self.elegir_personas(age1, -2, tipo[0])
        age2 = self.elegir_personas(age2, -2, tipo[1])
        per1 = Persona(age1, tipo[0])
        per2 = Persona(age2, tipo[1])
        return per1, per2