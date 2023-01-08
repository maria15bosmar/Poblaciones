import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
from utils import *
from persona import Persona
from facilities import raster
from xml.dom import minidom
import copy
import math

def planear(lista_familias: list):
    mapa = raster()
    familias = familias_reales()
    copia_fams = copy.deepcopy(familias)
    with open('population.xml','w') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE plans SYSTEM "http://www.matsim.org/files/dtd/plans_v4.dtd">\n\n')
    ET_padre = ET.Element("population")
    for i, familia in enumerate(lista_familias):
        tipo = familia.tipofamilia
        vacio = traspaso(familias[tipo-1], familia, ET_padre, mapa, tipo)
        print("Se han completado " + str(i) + " familias")
    if vacio == -1 or vacio == -3:
        if len(familias[tipo - 1]) >= len(copia_fams[tipo - 1]) / 2:
            familias[tipo - 1] = copy.deepcopy(copia_fams[tipo - 1])
        else:
            familias[tipo - 1] = familias[tipo - 1] + copy.deepcopy(copia_fams[tipo - 1])
    with open('population.xml','a') as f:
        f.write(minidom.parseString(ET.tostring(ET_padre)).toprettyxml(indent="\t"))

def familias_reales():
    """ Devuelve un array de 8 columnas con los 8 tipos de familias reales. """
    all_fams = []
    for tipo in range(1, 9):
        # Agregar la lista de planes de un tipo de familia a la lista de todos los tipos.
        print(tipo)
        df = pd.read_csv(PATH_CONSORCIO + f"ptipologia_{tipo}.csv")
        fam_tipo = []
        for id_hog in df["id_hog"].unique():
            # Agregar la lista de planes de una familia a la lista de planes de tipo de familia.
            df2 = df.loc[df["id_hog"] == id_hog]
            fam_plans = []
            for id_per in df2["id_per"].unique():
                # Agregar los planes de una persona a la lista de planes de familia.
                pers_df = df2.loc[df["id_per"] == id_per].values.tolist()
                #pers_df[all_cols] = pers_df[all_cols].astype(int)

                fam_plans.append(pers_df)
            fam_tipo.append(fam_plans)
        all_fams.append(fam_tipo)
    #return np.array(all_fams) # [tipo] [familia] [persona] [plan]
    return all_fams # [tipo] [familia] [persona] [plan]

def masceros(numero):   # Añade ceros a las horas para que tengan bien el formato
    if (len(str(numero)) == 1):
        numero = "000" + str(numero)
    elif (len(str(numero)) == 2):
        numero = "00" + str(numero)
    elif (len(str(numero)) == 3):
        numero = "0" + str(numero)
    return numero

def tipodeviaje(destinostr, cuadrante, mapa):
    if destinostr == "work":
        puntos = mapa[cuadrante].work
    elif destinostr == "education":
        puntos = mapa[cuadrante].education
    elif destinostr == "shopping":
        puntos = mapa[cuadrante].shopping
    elif destinostr == "medical":
        puntos = mapa[cuadrante].medical
    elif destinostr == "carry":     ## Falta por implementar carry
        puntos = mapa[cuadrante].work
    elif destinostr == "leisure":
        puntos = mapa[cuadrante].leisure
    return puntos

def trav_time(hora_ini, hora_fin):
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
    duracion = masceros(duracion)
    duracion = duracion[:2] + ":" + duracion[2:]
    return duracion

def pesoscuadrante(listapuntos, destinostr, mapa): # Toma todos los puntos del circulo y saca de los cuadrantes los valores del tipo buscado
    cuadrante_anterior, sumapuntuacion = -1, 0
    listacuadrantes,  listacuadrantes_aux = [], []
    for k in listapuntos:
        x_actual = k[0]
        y_actual = k[1]
        if MIN_X <= x_actual < MAX_X and MIN_Y > y_actual >= MAX_Y:
            dist_afinal_X = (x_actual - MIN_X) // 400  # Se calcula el cuadrante en X
            dist_afinal_Y = (MIN_Y - y_actual) // 400  # Se calcula el cuadrante en Y
            if dist_afinal_X == 15: # En el caso de que la x sea igual a x_final fallaria por ser division entera
                dist_afinal_X = 14
            if dist_afinal_Y == 15: # En el caso de que la y sea igual a y_final fallaria por ser division entera
                dist_afinal_Y = 14
            cuadrante = dist_afinal_X + dist_afinal_Y * 15  # Se calcula el cuadrante donde se situa el edificio
            if cuadrante != cuadrante_anterior:  # En caso de no haber revisado ya ese cuadrante se inserta
                edificios = tipodeviaje(destinostr, cuadrante, mapa)
                if edificios > 0:
                    sumapuntuacion += edificios
                    listacuadrantes.append([cuadrante, sumapuntuacion, x_actual, y_actual])  # Se guarda la suma de puntuaciones para luego usar el random
                listacuadrantes_aux.append([cuadrante, sumapuntuacion, x_actual, y_actual])
                cuadrante_anterior = cuadrante
    if sumapuntuacion == 0 and len(listacuadrantes_aux) > 0:    # Si no hay puntuacion para el tipo de viaje se escoje aleatoriamente un cuadrante
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

def coordenadas(x_anterior, y_anterior, distancia, destinostr, pueblo_dest, pueblo_orig, mapa):
    x_nueva, y_nueva = 1, 1
    if pueblo_dest != 74:  # Si la persona se desplaza fuera del municipio se dan las cordenadas de la carretera por donde sale del mapa
        x_nueva, y_nueva = buscar_clave(VIAJES_FUERA, pueblo_dest)
    else:                                       # En caso de quedarse en el municipio se ven los lugares posibles a los que ir
        grados_girados = 0
        listapuntos = []
        if pueblo_dest == pueblo_orig:
            radio = round(distancia * 1000)
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
        if x_anterior + radio > 438447 and x_anterior - radio < 432447 and y_anterior + radio > 4468216 and x_anterior - radio < 4462216: #Si se sale por todos los lados del mapa se reduce el radio
            radio = round(radio/2)
        x_nueva = x_anterior + radio    #Primer punto a comprobar [x+radio, y]
        listapuntos.append([x_nueva, y_anterior])
        grados_girados += grados
        while grados_girados <= 90:  # Se hayan los puntos del 1 cuadrante
            alpha = grados_girados * math.pi / 180  # Pasar grados a radianes
            cos_x_nueva = math.cos(alpha)
            sin_y_nueva = math.sin(alpha)
            x_nueva = round(x_anterior + radio * cos_x_nueva)
            y_nueva = round(y_anterior + radio * sin_y_nueva)
            listapuntos.append([x_nueva, y_nueva])
            grados_girados += grados
        puntos_cuadrante_1 = len(listapuntos)
        if grados_girados - grados == 90:  # En caso de tener un punto en 90 grados no hay que aplicarle simetria a ese punto
            puntos_cuadrante_1 -= 1 # Se resta 1 porque en caso de tener un pto en 90 grados, para i = 0 se cogeria este punto al ser el ultimo de la lista y asi se pilla el anterior
        for i in range(puntos_cuadrante_1):  # Se hayan los puntos del 2 cuadrante
            x_nueva = listapuntos[puntos_cuadrante_1 - 1 - i][0]  # Se resta 1 por ser una lista que si no outofindex
            y_nueva = listapuntos[puntos_cuadrante_1 - 1 - i][1]
            dist_en_x = x_nueva - x_anterior
            listapuntos.append([x_nueva - 2 * dist_en_x, y_nueva])  # Simetria del punto respecto al eje de ordenadas
        puntos_cuadrante_1y2 = len(listapuntos) - 2  # A los puntos en x - radio y x + radio no se les aplica simetria
        for j in range(puntos_cuadrante_1y2):  # Se hayan los puntos del 3 y 4 cuadrante
            x_nueva = listapuntos[puntos_cuadrante_1y2 - j][0]
            y_nueva = listapuntos[puntos_cuadrante_1y2 - j][1]
            dist_en_y = y_nueva - y_anterior
            listapuntos.append([x_nueva, y_nueva - 2 * dist_en_y])  # Simetria del punto respecto al eje de abcisas
        x_nueva, y_nueva = pesoscuadrante(listapuntos, destinostr, mapa)
        if x_nueva is None or y_nueva is None:
            pass
    return x_nueva, y_nueva

def ordenar(fam_consorcio, fam_sintetica, num_hijos_sinte):
    persona, consorcio, consorcio_copia = [], [], []
    num_per_consorcio = int(fam_consorcio[0][0][0][14])
    num_hijos_consorcio = int(fam_consorcio[0][0][0][14]) - int(fam_consorcio[0][0][0][15])
    diferencia_hijos = num_hijos_consorcio - num_hijos_sinte
    for i in range(num_per_consorcio):
        # Diferencia hijos si hay problemas.
        if int(fam_consorcio[0][i][0][12]) <= 24:
            if diferencia_hijos > 0:
                #np.delete(fam_consorcio[0], i, 0)
                fam_consorcio[0].pop(i)
                num_per_consorcio -= 1
            elif diferencia_hijos < 0:
                copia = copy.deepcopy(fam_consorcio[0][i])
                fam_consorcio[0].append(copia)
                #np.append(copia, axis = 0)
                num_per_consorcio += 1
            break
    fam_consorcio[0].sort(reverse=True, key = lambda p: p[0][12])
    """for k in range(num_per_consorcio):
        persona = Persona(int(fam_consorcio[0][k][0][1]), int(fam_consorcio[0][k][0][3])-1, int(fam_consorcio[0][k][0][12])) # Edad, genero e id de la persona le resto uno al genero para que coincida con 0 h 1 m
        consorcio.append(persona)
    consorcio_copia = copy.deepcopy(consorcio)
    consorcio.sort(reverse=True, key = lambda p: p.edad)"""
    """ins = False
    # Inserción ordenada.
    for i in range(len(consorcio)):
        if consorcio[i].edad < persona.edad:
            consorcio.insert(i, persona)
            ins = True
            break
    if not ins:
        consorcio.append(persona)"""
    # Ordenar la pareja si no está bien.
    if len(consorcio) - num_hijos_sinte == 2:
        if fam_consorcio[0][0][0][12] != fam_sintetica.personas[0].edad and fam_consorcio[0][1][0][12] != fam_sintetica.personas[1].edad:
           fam_consorcio[0][0][0][12], fam_consorcio[0][1][0][12] = fam_consorcio[0][1][0][12], fam_consorcio[0][0][0][12]
    """for l in range(num_per_consorcio):
        if consorcio_copia[l].edad != consorcio[l].edad:    #Si no coinciden estan desordenados
            for x in range(l+1, num_per_consorcio):      # buscamos entonces la posicion en la que estaba la persona originalmente
                if consorcio_copia[x][2] == consorcio[l][2]:  # Una vez encontrada la posicion en la copia modificamos esta y la lista principal
                    fam_consorcio[0][0][l], fam_consorcio[0][0][x] = fam_consorcio[0][0][x], fam_consorcio[0][0][l]
                    consorcio_copia[l], consorcio_copia[x] = consorcio_copia[x], consorcio_copia[l]
                    break"""

def traspaso(fam_consorcio, fam_sintetica, padre_ET, mapa, tipologia):
    """ Se escriben los planes de una familia. """
    # COMPROBAR QUE FAMILIA ES APTA.
    num_hijos_sinte = 0
    # Se comprueba que coincida el numero de adultos en ambas familias real y sintetica.
    if tipologia >= 3:    
        parabucle = 0
        familiapta = True
        match = False
        num_adultos_sinte = len(fam_sintetica.personas) 
        # Caso tipologias 3 y 4 todos son adultos.
        # Caso tipologias 5, 6, 7 y 8 ver cuantos son adultos y cuantos niños.
        if tipologia >= 5:  
            num_adultos_sinte = 0
            hogar_joven = 0
            for persona in fam_sintetica.personas:
                if persona.edad > 24:
                    num_adultos_sinte += 1
                    hogar_joven += 1
                if persona.edad <= 24:
                    num_hijos_sinte += 1
            # Parejas jovenes uno de los dos de entre 18 y 24 con hijos.
            if hogar_joven == 1 and (tipologia == 6 or tipologia == 8): 
                num_joven = 0
                for persona in fam_sintetica.personas:
                    # Se comprueba si hay un solo un progenitor de entre 18 y 24
                    if 17 < persona.edad <= 24:
                        num_joven += 1
                        joven = persona
                if num_joven == 1:
                    pareja = 0
                    for persona2 in fam_sintetica.personas:
                        # Busca a alguien que no pueda ser su hijo para luego comprobar que sea su pareja.
                        if joven != persona2 and joven.edad - persona2.edad <= 15:
                            # Se comprueba que pueda ser su pareja si tiene mas de 18 y se llevan menos de 15
                            if persona2.edad >= 18 and joven.edad - persona2.edad > -15:
                                pareja += 1    # No puede ser su hijo pero sí su pareja
                            else:   # No puede ser su hijo ni su pareja. Familia no válida.
                                pareja = 0
                                break
                    if pareja == 1:
                        num_adultos_sinte += 1
                        num_hijos_sinte -= 1
                    else:
                        familiapta = False
                else:
                    familiapta = False
            # Parejas jovenes los dos de entre 18 y 24 con hijos.
            if hogar_joven == 0 and (tipologia == 6 or tipologia == 8):
                pareja = []
                for persona in fam_sintetica.personas:
                    # Se comprueba si hay dos progenitores de entre 18 y 24
                    if 17 < persona.edad <= 24:
                        pareja.append(persona)
                # Si los hay se comprueba que el resto de la familia puedan ser sus hijos es decir los tuvierron como min a los 15
                if len(pareja) == 2:
                    posible = True
                    for persona in fam_sintetica.personas:
                        if persona != pareja[0] and persona != pareja[1]:
                            if pareja[0].edad - persona.edad < 15 or pareja[1].edad - persona.edad < 15:
                                # Se ha comprobado que uno de los hijos por edad no puede ser hijo de uno de los progenitores. Familia no válida.
                                posible = False 
                                break
                    if posible == True:
                        num_adultos_sinte += 2
                        num_hijos_sinte -= 2
                    else:
                        familiapta = False
                else:
                    familiapta = False
        # Una vez comprobado que la familia sea apta.
        # COMPROBACIÓN DE COMPATIBILIDAD DE FAMILIA Y CONSORCIO.
        if familiapta == True:
            while match == False:
                num_adultos_consorcio = int(fam_consorcio[0][0][0][15])
                num_hijos_consorcio = int(fam_consorcio[0][0][0][14]) - num_adultos_consorcio
                # Si coinciden el numero de adulto y como mucho hay un niño sinte mas se asignan los planes.
                if num_adultos_sinte == num_adultos_consorcio and abs(num_hijos_sinte - num_hijos_consorcio) <= 1:
                    match = True
                    if tipologia >= 5:  # tipologias 5 6 7 y 8 que tienen niños
                        fam_sintetica.sort_personas()
                else:   # Si no coincide se quita la familia del consorcio de la lista y se pone atras
                    fam_consorcio.append(fam_consorcio.pop(0))
                    parabucle += 1
                    if parabucle == len(fam_consorcio):
                        return -1   # No quedan familias que se ajusten al tipo que ha salido
        else:
            return -2   # La familia sintetica no es apta
        ordenar(fam_consorcio, fam_sintetica, num_hijos_sinte)
    for persona in fam_sintetica.personas:
        # Caso de que la persona del consorcio no tenga planes
        if int(fam_consorcio[0][0][0][2]) == -1:
            fam_consorcio[0].pop(0)  # Se borra a la persona que no tenia planes
            # Si no quedan más personas en la familia se borra la familia
            if len(fam_consorcio[0]) == 0:
                fam_consorcio.pop(0)
        else:
            generostr = num_to_xml[0][persona.genero]
            carnet = int(fam_consorcio[0][0][0][5])
            carnetstr = num_to_xml[1][carnet] if carnet == 1 else num_to_xml[1][0]
            trabajostr = num_to_xml[2][tipologia-1]
            # Construir el árbol XML.
            persona_ET = ET.SubElement(padre_ET, 'person')
            persona_ET.set("id", str(persona.id))
            persona_ET.set("sex", generostr)
            persona_ET.set("age", str(persona.edad))
            persona_ET.set("license", carnetstr[0])
            persona_ET.set("car_avail", carnetstr[1])
            persona_ET.set("employed", trabajostr)
            # Escribir planes en el árbol XML.
            plan_ET = ET.SubElement(persona_ET, "plan")
            plan_ET.set("selected", "yes")
            # Mientras queden planes por escribir sobre esa persona.
            terminado = False
            while not terminado:
                hora_ini = int(fam_consorcio[0][0][0][6])
                hora_fin = int(fam_consorcio[0][0][0][7])
                hora_ini = masceros(hora_ini)
                hora_fin = masceros(hora_fin)
                duracion = trav_time(hora_ini, hora_fin)
                hora_ini = str(hora_ini)[:2] + ":" + str(hora_ini)[2:]
                hora_fin = str(hora_fin)[:2] + ":" + str(hora_fin)[2:]
                modestr = buscar_clave(MODO, fam_consorcio[0][0][0][10])
                origenstr = buscar_clave(LUGAR, int(fam_consorcio[0][0][0][8]))
                destinostr = buscar_clave(LUGAR, int(fam_consorcio[0][0][0][9]))
                id_viaje = fam_consorcio[0][0][0][2] - 1
                if id_viaje == 0:   # En caso de que sea el primer viaje se pone la estancia en casa hasta la hora de salir
                    x_anterior = fam_sintetica.casa[0]
                    y_anterior = fam_sintetica.casa[1]
                    act_ET = ET.SubElement(plan_ET, "act")
                    act_ET.set("type", origenstr)
                    act_ET.set("x", str(x_anterior))
                    act_ET.set("y", str(y_anterior))
                    act_ET.set("start_time", "00:00")
                    act_ET.set("dur", str(hora_ini))
                    act_ET.set("end_time", str(hora_ini))
                if destinostr == "home":
                    x_nueva = fam_sintetica.casa[0]
                    y_nueva = fam_sintetica.casa[1]
                else:
                    x_nueva, y_nueva = coordenadas(round(float(x_anterior)), 
                        round(float(y_anterior)),fam_consorcio[0][0][0][11], 
                        destinostr, int(fam_consorcio[0][0][0][16]), 
                        int(fam_consorcio[0][0][0][17]),mapa)
                # Nuevo desplazamiento.
                leg_ET = ET.SubElement(plan_ET, "leg")
                leg_ET.set("mode", modestr)
                leg_ET.set("dep_time", str(hora_ini))
                leg_ET.set("trav_time", str(duracion))
                leg_ET.set("arr_time", str(hora_fin))
                # Nueva actividad.
                act_ET = ET.SubElement(plan_ET, "act")
                act_ET.set("type", destinostr)
                act_ET.set("x", str(x_nueva))
                act_ET.set("y", str(y_nueva))
                act_ET.set("start_time", str(hora_ini))
                # En caso de que solo le queda un plan por hacer a la persona
                if len(fam_consorcio[0][0]) == 1:  
                    hora_ini_aux = hora_ini.replace(":", "")
                    duracionfinal = trav_time(hora_ini_aux, 2400)
                    act_ET.set("dur", str(duracionfinal))
                    act_ET.set("end_time", "24:00")
                else: # Si quedan más.
                    act_ET.set("dur", str(duracion))
                    act_ET.set("end_time", str(hora_fin))
                x_anterior = x_nueva
                y_anterior = y_nueva
                fam_consorcio[0][0].pop(0) # Se elimina el plan ya asignado
                # Si no quedan mas personas en la familia se borra la familia
                if len(fam_consorcio[0][0]) == 0:
                    # Se borra a la persona que no tiene ya planes
                    fam_consorcio[0].pop(0)  
                    terminado = True
                if len(fam_consorcio[0]) == 0:
                    fam_consorcio.pop(0)
               
    if len(fam_consorcio) == 0:
        return -3
    else:
        return 0