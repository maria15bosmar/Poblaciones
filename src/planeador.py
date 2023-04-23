""" Módulo de planeador. Gestiona los planes que se asignan a las familias sintéticas. """

import xml.etree.ElementTree as ET
from xml.dom import minidom
import copy, math
import numpy as np
import pandas as pd
from entidades.plan import Plan
from facilities import raster
from utils import *

def planear(lista_familias: list):
    """ Función principal. Asigna los planes y escribe el fichero de población."""
    # Cargar el mapa.
    mapa = raster()
    # Cargar datos del consorcio sobre las familias reales.
    familias = familias_reales()
    copia_fams = copy.deepcopy(familias)
    # Escribir el header del fichero de salida.
    with open(NOMBRE_FICHERO,'w') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE population SYSTEM "http://www.matsim.org/files/dtd/population_v5.dtd">\n\n')
    # Raíz del árbol XML.
    ET_padre = ET.Element("population")
    # Por cada familia sintética.
    for i, familia in enumerate(lista_familias):
        tipo = familia.tipofamilia
        # Se le asignan los planes.
        vacio = traspaso(familias[tipo-1], familia, ET_padre, mapa, tipo)
        print("Se han completado " + str(i) + " familias")
        # Si alguna de las listas de familias reales ha quedado vacía, se restaura con una copia.
        if vacio == -1 or vacio == -3:
            if len(familias[tipo - 1]) >= len(copia_fams[tipo - 1]) / 2:
                familias[tipo - 1] = copy.deepcopy(copia_fams[tipo - 1])
            else:
                familias[tipo - 1] = familias[tipo - 1] + copy.deepcopy(copia_fams[tipo - 1])
    # Escribir el árbol XML con los planes en el fichero de salida.
    with open(NOMBRE_FICHERO,'a') as f:
        xml = minidom.parseString(ET.tostring(ET_padre, xml_declaration=False)).toprettyxml(indent="\t")
        line_break_position = xml.find('\n') + 1
        headless_xml = xml[line_break_position:]
        f.write(headless_xml)

def familias_reales():
    """ Devuelve una matriz de 8 columnas con los 8 tipos de familias reales. """
    all_fams = []
    # Para cada tipo de familia.
    for tipo in range(1, 9):
        # Agregar la lista de planes de un tipo de familia a la lista de todos los tipos.
        print(tipo)
        df = pd.read_csv(PATH_CONSORCIO + f"ptipologia_{tipo}.csv")
        fam_tipo = []
        # Por cada familia.
        for id_hog in df["id_hog"].unique():
            # Agregar la lista de planes de una familia a la lista de planes de tipo de familia.
            df2 = df.loc[df["id_hog"] == id_hog]
            fam_plans = []
            # Por cada persona en una familia.
            for id_per in df2["id_per"].unique():
                # Agregar los planes de una persona a la lista de planes de familia.
                pers_plans = []
                for plan in df2.loc[df["id_per"] == id_per].values.tolist():
                    pers_plans.append(Plan(plan, tipo))
                fam_plans.append(pers_plans)
            fam_tipo.append(fam_plans)
        all_fams.append(fam_tipo)
    return all_fams # [tipo] [familia] [persona] [plan]

def ordenar(fam_consorcio, fam_sintetica, num_hijos_sinte):
    """ Ordena una familia del consorcio para que los planes sean
    consistentes con las personas de la familia sintética. """
    consorcio = []
    # Obtener número total de personas y de hijos.
    num_per_consorcio = int(fam_consorcio[0][0][0].num_miembros)
    num_hijos_consorcio = int(fam_consorcio[0][0][0].num_miembros) - int(fam_consorcio[0][0][0].num_adultos)
    diferencia_hijos = num_hijos_consorcio - num_hijos_sinte
    # Si hay diferencias en el número de hijos se agrega o elimina uno del consorcio.
    for i in range(num_per_consorcio):
        if int(fam_consorcio[0][i][0].edad) <= 24:
            # Si el consorcio tiene un hijo de más.
            if diferencia_hijos > 0:
                fam_consorcio[0].pop(i)
                num_per_consorcio -= 1
            # Si el consorcio tiene un hijo de menos.
            elif diferencia_hijos < 0:
                copia = copy.deepcopy(fam_consorcio[0][i])
                fam_consorcio[0].append(copia)
                num_per_consorcio += 1
            break
    # Ordenar la familia del consorcio por edad.
    fam_consorcio[0].sort(reverse=True, key = lambda p: p[0].edad)
    # Ordenar la pareja si no está bien.
    if len(consorcio) - num_hijos_sinte == 2:
        if (fam_consorcio[0][0][0].edad != fam_sintetica.personas[0].edad and
            fam_consorcio[0][1][0].edad != fam_sintetica.personas[1].edad):
            fam_consorcio[0][0][0].edad, fam_consorcio[0][1][0].edad = fam_consorcio[0][1][0].edad, fam_consorcio[0][0][0].edad

def traspaso(fam_consorcio, fam_sintetica, padre_ET, mapa, tipologia):
    """ Se escriben los planes de una familia. """
    ### COMPROBACIÓN DE COMPATIBILIDAD DE FAMILIA Y CONSORCIO.
    # Se comprueba que coincida el numero de adultos en ambas familias real y sintetica.
    # Para las tipología 1 y 2 no hace falta hacer comprobación ya que no hay hijos
    if tipologia >= 3:
        match = False
        parabucle = 0
        while match is False:
            num_adultos_consorcio = int(fam_consorcio[0][0][0].num_adultos)
            num_hijos_consorcio = int(fam_consorcio[0][0][0].num_miembros) - num_adultos_consorcio
            # Si coinciden el número de adultos y como mucho
            # hay un niño más se asignan los planes.
            if (fam_sintetica.n_adultos == num_adultos_consorcio and
                abs(fam_sintetica.n_hijos - num_hijos_consorcio) <= 1):
                match = True
                # tipologias 5, 6, 7 y 8 que tienen niños
                if tipologia >= 5:
                    fam_sintetica.sort_personas()
            # Si no coincide se quita la familia del consorcio de la lista y se pone atrás.
            else:
                fam_consorcio.append(fam_consorcio.pop(0))
                parabucle += 1
                # No quedan familias que se ajusten al tipo que ha salido.
                if parabucle == len(fam_consorcio):
                    return -1
        ordenar(fam_consorcio, fam_sintetica, fam_sintetica.n_hijos)
    ### ESCRIBIR LOS PLANES.
    for persona in fam_sintetica.personas:
        # Caso de que la persona del consorcio no tenga planes
        if int(fam_consorcio[0][0][0].id_via) == -2:
            fam_consorcio[0].pop(0)  # Se borra a la persona que no tenia planes.
            # Si no quedan más personas en la familia se borra la familia
            if len(fam_consorcio[0]) == 0:
                fam_consorcio.pop(0)
        else:
            # Construir el árbol XML.
            plan_ET = fam_consorcio[0][0][0].generate_persona_xml(padre_ET, persona, tipologia)
            # Bucle para escribir los planes.
            terminado = False
            while not terminado:
                fam_consorcio[0][0][0].generate_plan_xml(plan_ET, mapa, fam_sintetica, persona)
                # Se elimina el plan ya asignado.
                fam_consorcio[0][0].pop(0)
                # Si no quedan mas personas en la familia se borra la familia
                if len(fam_consorcio[0][0]) == 0:
                    # Se borra a la persona que no tiene ya planes
                    fam_consorcio[0].pop(0)
                    terminado = True
                if len(fam_consorcio[0]) == 0:
                    fam_consorcio.pop(0)
    # Si no quedan familias en el consorcio se solicita que se restaure la lista.
    if len(fam_consorcio) == 0:
        return -3
    else:
        return 0
