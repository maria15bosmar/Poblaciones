import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
from utils import *
from persona import Persona
import copy

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
                pers_df = df2.loc[df["id_per"] == id_per].values
                fam_plans.append(pers_df)
            fam_tipo.append(fam_plans)
        all_fams.append(fam_tipo)
    #return np.array(all_fams) # [tipo] [familia] [persona] [plan]
    return all_fams # [tipo] [familia] [persona] [plan]

def ordenar(fam_consorcio, fam_sintetica, num_hijos_sinte):
    persona, consorcio, consorcio_copia = [], [], []
    num_per_consorcio = int(fam_consorcio[0][0][14])
    num_hijos_consorcio = int(fam_consorcio[0][0][14]) - int(fam_consorcio[0][0][15])
    direncia_hijos = num_hijos_consorcio - num_hijos_sinte
    for i in range(num_hijos_consorcio):
        # Diferencia hijos si hay problemas.
        if int(fam_consorcio[i][0][12]) <= 24:
            if direncia_hijos > 0:
                #np.delete(fam_consorcio, i, 0)
                fam_consorcio.pop(i)
                num_per_consorcio -= 1
            else:
                copia = np.deepcopy(fam_consorcio[i])
                fam_consorcio.append(copia)
                #np.append(copia, axis = 0)
                num_per_consorcio += 1
            break
    fam_consorcio.sort(reverse=True, key = lambda p: p[0][12])
    """for k in range(num_per_consorcio):
        persona = Persona(int(fam_consorcio[k][0][1]), int(fam_consorcio[k][0][3])-1, int(fam_consorcio[k][0][12])) # Edad, genero e id de la persona le resto uno al genero para que coincida con 0 h 1 m
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
        if fam_consorcio[0][0][12] != fam_sintetica.personas[0].edad and fam_consorcio[1][0][12] != fam_sintetica.personas[1].edad:
           fam_consorcio[0][0][12], fam_consorcio[1][0][12] = fam_consorcio[1][0][12], fam_consorcio[0][0][12]
    """for l in range(num_per_consorcio):
        if consorcio_copia[l].edad != consorcio[l].edad:    #Si no coinciden estan desordenados
            for x in range(l+1, num_per_consorcio):      # buscamos entonces la posicion en la que estaba la persona originalmente
                if consorcio_copia[x][2] == consorcio[l][2]:  # Una vez encontrada la posicion en la copia modificamos esta y la lista principal
                    fam_consorcio[0][l], fam_consorcio[0][x] = fam_consorcio[0][x], fam_consorcio[0][l]
                    consorcio_copia[l], consorcio_copia[x] = consorcio_copia[x], consorcio_copia[l]
                    break"""

def traspaso(fam_consorcio, fam_sintetica, padre_ET, mapa, tipologia):
    num_hijos_sinte = 0
    if tipologia >= 3:    # Se comprueba que coincida el numero de adultos en ambas familias real y sintetica
        parabucle = 0
        familiapta = True
        match = False
        num_adultos_sinte = len(fam_sintetica.personas)  # Caso tipologias 3 y 4 todos son adultos
        if tipologia >= 5:  # Caso tipologias 5, 6, 7 y 8 ver cuantos son adultos y cuantos niños
            num_adultos_sinte = 0
            hogar_joven = 0
            for persona in fam_sintetica.personas:
                if persona.edad > 24:
                    num_adultos_sinte += 1
                    hogar_joven += 1
                if persona.edad <= 24:
                    num_hijos_sinte += 1
            if hogar_joven == 1 and (tipologia == 6 or tipologia == 8): # Parejas jovenes uno de los dos de entre 18 y 24 con hijos se comprueba que este bien para aceptarla o no
                num_joven = 0
                for persona in fam_sintetica.personas:
                    if 17 < persona.edad <= 24:  # Se comprueba si hay un solo un progenitor de entre 18 y 24
                        num_joven += 1
                        joven = persona
                if num_joven == 1:
                    pareja = 0
                    for persona2 in fam_sintetica.personas:
                        if joven != persona2 and joven.edad - persona2.edad <= 15: # Busca a alguien que no pueda ser su hijo para luego comprobar que sea su pareja
                            if persona2.edad >= 18 and joven.edad - persona2.edad > -15: # Se comprueba que pueda ser su pareja si tiene mas de 18 y se llevan menos de 15
                                pareja += 1    # Se ha encontrado uno que no puede ser su hijo pero si su pareja
                            else:   # Se ha encontrado uno que no puede ser su hijo ni su pareja luego se invalida la familia
                                pareja = 0
                                break
                    if pareja == 1:
                        num_adultos_sinte += 1
                        num_hijos_sinte -= 1
                    else:
                        familiapta = False
                else:
                    familiapta = False
            if hogar_joven == 0 and (tipologia == 6 or tipologia == 8):  # Parejas jovenes los dos de entre 18 y 24 con hijos se comprueba que este bien para aceptarla o no
                pareja = []
                for persona in fam_sintetica.personas:
                    if 17 < persona.edad <= 24:  # Se comprueba si hay dos progenitores de entre 18 y 24
                        pareja.append(persona)
                if len(pareja) == 2: # Si los hay se comprueba que el resto de la familia puedan ser sus hijos es decir los tuvierron como min a los 15
                    posible = True
                    for persona in fam_sintetica.personas:
                        if persona != pareja[0] and persona != pareja[1]:
                            if pareja[0].edad - persona.edad < 15 or pareja[1].edad - persona.edad < 15:
                                posible = False # Se ha comprobado que uno de los hijos por edad no puede ser hijo de uno de los progenitores luego ya no es una familia valida
                                break
                    if posible == True:
                        num_adultos_sinte += 2
                        num_hijos_sinte -= 2
                    else:
                        familiapta = False
                else:
                    familiapta = False
        # Una vez comprobado que la familia sea apta.
        if familiapta == True:
            while match == False:
                num_adultos_consorcio = int(fam_consorcio[0][0][0][15])
                num_hijos_consorcio = int(fam_consorcio[0][0][0][14]) - num_adultos_consorcio
                if num_adultos_sinte == num_adultos_consorcio and num_hijos_sinte - num_hijos_consorcio <= 1:  # Si coinciden el numero de adulto y como mucho hay un niño sinte mas se asignan los planes
                    match = True
                    if tipologia >= 5:  # tipologias 5 6 7 y 8 que tienen niños
                        fam_sintetica.sort_personas()
                else:   # Si no coincide se quita la familia del consorcio de la lista y se pone atras
                    fam_consorcio.append(fam_consorcio.pop(0))
                    parabucle += 1
                    if parabucle == len(fam_consorcio):
                        return -1   ## No quedan familias que se ajusten al tipo que ha salido
        else:
            return -2   # La familia sintetica no es apta
        ordenar(fam_consorcio[0], fam_sintetica, num_hijos_sinte)
    for persona in fam_sintetica.personas:
        if int(fam_consorcio[0][0][0][2]) == -1:    # Caso de que la persona del consorcio no tenga planes
            fam_consorcio[0].pop(0)  # Se borra a la persona que no tenia planes
            if len(fam_consorcio[0]) == 0:  # Si no quedan mas personas en la familia se borra la familia
                fam_consorcio.pop(0)
        else:
            generostr = num_to_xml[0][persona.genero]
            carnet = fam_consorcio[0][0][0][5]
            carnetstr = num_to_xml[1][carnet] if carnet == 1 else num_to_xml[1][0]
            trabajostr = num_to_xml[2][tipologia-1]
            # Construir el árbol XML.
            persona_ET = ET.SubElement(padre_ET, 'person')
            persona_ET.set("id", persona.id)
            persona_ET.set("sex", generostr)
            persona_ET.set("age", persona.edad)
            persona_ET.set("license", carnetstr[0])
            persona_ET.set("car_avail", carnetstr[1])
            persona_ET.set("employed", trabajostr)
            # Escribir planes en el árbol XML.
            plan_ET = ET.SubElement(persona_ET, "plan")
            plan_ET.set("selected", "yes")
            terminado = False
            while not terminado:
                # LÍNEA 510
                pass
