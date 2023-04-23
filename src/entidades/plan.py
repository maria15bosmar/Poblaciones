""" Representa un Plan. """

import xml.etree.ElementTree as ET
import math
import numpy as np
from utils import num_to_xml, buscar_clave, INPUT_SALIDA, INPUT_GEO, MAX_X, MAX_Y, MIN_X, MIN_Y

class Plan:
    def __init__(self, datos, tipo) -> None:
        self.id_pers = datos[1]
        self.id_hog = datos[0]
        self.id_via = datos[2] - 1
        self.num_adultos = datos[15]
        self.num_miembros = datos[14]
        self.edad = datos[12]
        if self.id_via != -2:
            self.genero = datos[3]
            carnet = num_to_xml[1][int(datos[5])] if datos[5] == 1 else num_to_xml[1][0]
            self.license = carnet[0]
            self.car_avail = carnet[1]
            self.employed = num_to_xml[2][tipo-1]
            self.hora_ini = self.__to_hora(datos[6])
            self.hora_fin = self.__to_hora(datos[7])
            self.duracion = self.__trav_time(self.hora_ini, self.hora_fin)
            self.mot_origen = buscar_clave(INPUT_SALIDA["lugar"], int(datos[8]))
            self.mot_destino = buscar_clave(INPUT_SALIDA["lugar"], int(datos[9]))
            self.vehiculo = buscar_clave(INPUT_SALIDA["modo"], int(datos[10]))
            self.distancia = datos[11]
            self.pueblo_dest = datos[16]
            self.pueblo_orig = datos[17]

    def generate_persona_xml(self, root, persona, tipologia):
        ET_persona = ET.SubElement(root, 'person')
        ET_persona.set("id", str(persona.id))
        ET_persona.set("sex", num_to_xml[0][persona.genero])
        ET_persona.set("age", str(persona.edad))
        ET_persona.set("license", self.license)
        ET_persona.set("car_avail", self.car_avail)
        ET_persona.set("employed", num_to_xml[2][tipologia-1])
        plan_ET = ET.SubElement(ET_persona, "plan")
        plan_ET.set("selected", "yes")
        return plan_ET
    
    def generate_plan_xml(self, root, mapa, fam_sintetica, persona):
        
        if self.id_via == 0:
            act_ET = ET.SubElement(root, "act")
            act_ET.set("type", self.mot_origen)
            act_ET.set("x", str(persona.posicion[0]))
            act_ET.set("y", str(persona.posicion[1]))
            act_ET.set("start_time", "00:00")
            #act_ET.set("dur", str(hora_ini))
            act_ET.set("end_time", self.hora_ini)
        if self.mot_destino == "home":
            x_nueva = fam_sintetica.casa[0]
            y_nueva = fam_sintetica.casa[1]
        else:
            x_nueva, y_nueva = self.__coordenadas(round(float(persona.posicion[0])),
                round(float(persona.posicion[1])), mapa)
        leg_ET = ET.SubElement(root, "leg")
        leg_ET.set("mode", self.vehiculo)
        leg_ET.set("dep_time", self.hora_ini)
        leg_ET.set("trav_time", self.duracion)
        leg_ET.set("arr_time", self.hora_fin)
        # Nueva actividad.
        act_ET = ET.SubElement(root, "act")
        act_ET.set("type", self.mot_destino)
        act_ET.set("x", str(x_nueva))
        act_ET.set("y", str(y_nueva))
        act_ET.set("start_time", self.hora_ini)
        act_ET.set("end_time", self.hora_fin)
        persona.posicion = [x_nueva, y_nueva]
    
    @staticmethod
    def __to_hora(numero):
        """Añade ceros a las horas para que tengan bien el formato"""
        hora = str(int(numero))
        while len(hora) < 4:
            hora = "0" + hora
        str(hora)[:2] + ":" + str(hora)[2:]
        return hora
    
    def __trav_time(self, hora_ini, hora_fin):
        """ Obtiene la duración de un viaje dadas una hora inicial y una final. """
        h1 = str(hora_ini)[:2]
        m1 = str(hora_ini)[2:]
        h2 = str(hora_fin)[:2]
        m2 = str(hora_fin)[2:]
        min1 = int(m1) + int(h1) * 60
        min2 = int(m2) + int(h2) * 60
        duracion = min2 - min1
        if duracion >= 60:
            horas = duracion // 60
            minutos = str(duracion - 60 * horas)
            if len(str(minutos)) == 1:
                minutos = "0" + str(minutos)
            duracion = str(horas) + str(minutos)
        duracion = self.__to_hora(duracion)
        return duracion
    
    def __pesoscuadrante(self, listapuntos, mapa):
        """ Toma todos los puntos del círculo y saca de los cuadrantes los valores del tipo buscado. """
        cuadrante_anterior, sumapuntuacion = -1, 0
        listacuadrantes,  listacuadrantes_aux = [], []
        for punto in listapuntos:
            x_actual = punto[0]
            y_actual = punto[1]
            if MIN_X <= x_actual < MAX_X and MIN_Y > y_actual >= MAX_Y:
                dist_afinal_X = (x_actual - MIN_X) // 400  # Se calcula el cuadrante en X.
                dist_afinal_Y = (MIN_Y - y_actual) // 400  # Se calcula el cuadrante en Y.
                # En el caso de que la x sea igual a x_final fallaria por ser division entera.
                if dist_afinal_X == 15:
                    dist_afinal_X = 14
                # En el caso de que la y sea igual a y_final fallaria por ser division entera.
                if dist_afinal_Y == 15:
                    dist_afinal_Y = 14
                # Se calcula el cuadrante donde se situa el edificio.
                cuadrante = dist_afinal_X + dist_afinal_Y * 15
                # En caso de no haber revisado ya ese cuadrante se inserta.
                if cuadrante != cuadrante_anterior:
                    edificios = mapa[cuadrante].edificios[self.mot_destino]
                    if edificios > 0:
                        sumapuntuacion += edificios
                        # Se guarda la suma de puntuaciones para luego usar el random.
                        listacuadrantes.append([cuadrante, sumapuntuacion, x_actual, y_actual])
                    listacuadrantes_aux.append([cuadrante, sumapuntuacion, x_actual, y_actual])
                    cuadrante_anterior = cuadrante
        # Si no hay puntuacion para el tipo de viaje se escoje aleatoriamente un cuadrante.
        if sumapuntuacion == 0 and len(listacuadrantes_aux) > 0:
            aleatorio = np.random.randint(0, len(listacuadrantes_aux))
            x_nueva = listacuadrantes_aux[aleatorio][2]
            y_nueva = listacuadrantes_aux[aleatorio][3]
        else:
            puntero = np.random.randint(0, sumapuntuacion + 1)
            for l in listacuadrantes:
                if l[1] >= puntero:
                    x_nueva = l[2]
                    y_nueva = l[3]
                    break
        return x_nueva, y_nueva

    def __coordenadas(self, x_anterior, y_anterior, mapa):
        """ Devuelve las coordenadas del destino de un viaje. """
        x_nueva, y_nueva = 1, 1
        # Si la persona se desplaza fuera del municipio se dan las cordenadas de la carretera por donde sale del mapa.
        if self.pueblo_dest != INPUT_GEO["codigo_ciudad"]:
            x_nueva, y_nueva = buscar_clave(INPUT_GEO["viajes_fuera"], self.pueblo_dest)
        else:
            # En caso de quedarse en el municipio se ven los lugares posibles a los que ir.
            grados_girados = 0
            listapuntos = []
            if self.pueblo_dest == self.pueblo_orig:
                radio = round(self.distancia * 1000)
                if radio <= 500:
                    grados = 20
                elif 500 < radio <= 1000:
                    grados = 10
                elif 1000 < radio <= 3000:
                    grados = 5
                elif 3000 < radio <= 8400:
                    grados = 2.5
                elif radio > 8400:
                    radio = 4000
                    grados = 2.5
            else:
                radio = 4000
                grados = 2.5
            #Si se sale por todos los lados del mapa se reduce el radio
            if (x_anterior + radio > MAX_X and x_anterior - radio < MIN_X and
                y_anterior + radio > MIN_Y and x_anterior - radio < MAX_Y):
                radio = round(radio/2)
            # Primer punto a comprobar [x + radio, y]
            x_nueva = x_anterior + radio
            listapuntos.append([x_nueva, y_anterior])
            grados_girados += grados
            while grados_girados <= 90:  # Se hallan los puntos del 1 cuadrante
                alpha = grados_girados * math.pi / 180  # Pasar grados a radianes
                listapuntos.append([round(x_anterior + radio * math.cos(alpha)), 
                                    round(y_anterior + radio * math.sin(alpha))])
                grados_girados += grados
            puntos_cuadrante_1 = len(listapuntos)
            # En caso de tener un punto en 90 grados no hay que aplicarle simetria a ese punto.
            if grados_girados - grados == 90:
                # Se resta 1 porque en caso de tener un pto en 90 grados, para i = 0 se cogería
                # este punto al ser el último de la lista y asi se pilla el anterior.
                puntos_cuadrante_1 -= 1
            # Se hayan los puntos del 2 cuadrante
            for i, punto in enumerate(reversed(listapuntos)):
                if grados_girados - grados == 90 and i == 0:
                    continue
                # Simetría del punto respecto al eje de ordenadas.
                listapuntos.append([punto[0] - 2 * (punto[0] - x_anterior), punto[1]])
            # A los puntos en x - radio y x + radio no se les aplica simetría.
            # Se hallan los puntos del 3 y 4 cuadrante.
            for i, punto in enumerate(reversed(listapuntos)):
                if i in (0, 1):
                    continue
                # Simetría del punto respecto al eje de abcisas
                listapuntos.append([punto[0], punto[1] - 2 * (punto[1] - y_anterior)])
            x_nueva, y_nueva = self.__pesoscuadrante(listapuntos, mapa)
            if x_nueva is None or y_nueva is None:
                pass
        return x_nueva, y_nueva
