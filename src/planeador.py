import xml.etree.ElementTree as et
import numpy as np
import pandas as pd
from utils import *

def familias_reales():
    """ Devuelve un array de 8 columnas con los 8 tipos de familias reales. """
    all_fams = []
    for tipo in range(1, 9):
        print(tipo)
        df = pd.read_csv(PATH_CONSORCIO + f"ptipologia_{tipo}.csv")
        fam_tipo = []
        for id_hog in df["id_hog"].unique():
            df2 = df.loc[df["id_hog"] == id_hog]
            fam_plans = []
            for id_per in df2["id_per"].unique():
                pers_df = df2.loc[df["id_per"] == id_per].values
                fam_plans.append(pers_df)
            fam_tipo.append(fam_plans)
        all_fams.append(fam_tipo)
    return np.array(all_fams)
        
def traspaso(fam_consorcio, fam_sintetica, fichero_salida, mapa, tipologia):
    terminado = False
    num_personas_sinte = len(fam_sintetica.personas)
    num_hijos_sinte = 0
    if tipologia >= 3:    # Se comprueba que coincida el numero de adultos en ambas familias real y sintetica
        parabucle = 0
        familiapta = True
        match = False
        num_adultos_sinte = num_personas_sinte  # Caso tipologias 3 y 4 todos son adultos
        if tipologia >= 5:  # Caso tipologias 5 6 7 y 8 ver cuantos son adultos y cuantos niños
            num_adultos_sinte = 0
            hogar_joven = 0
            for i in range(num_personas_sinte):
                if fam_sintetica.personas[i] > 24:
                    num_adultos_sinte += 1
                    hogar_joven += 1
                if fam_sintetica.personas[i] <= 24:
                    num_hijos_sinte += 1
            if hogar_joven == 1 and (tipologia == 6 or tipologia == 8): # Parejas jovenes uno de los dos de entre 18 y 24 con hijos se comprueba que este bien para aceptarla o no
                num_joven, joven = 0, 0
                for i in range(num_personas_sinte):
                    if 17 < fam_sintetica.personas[i] <= 24:  # Se comprueba si hay un solo un progenitor de entre 18 y 24
                        num_joven += 1
                        joven = i
                if num_joven == 1:
                    pareja = 0
                    for j in range(num_personas_sinte):
                        if joven != j and fam_sintetica.personas[joven] - fam_sintetica.personas[j] <= 15: # Busca a alguien que no pueda ser su hijo para luego comprobar que sea su pareja
                            if fam_sintetica.personas[j] >= 18 and fam_sintetica.personas[joven] - fam_sintetica.personas[j] > -15: # Se comprueba que pueda ser su pareja si tiene mas de 18 y se llevan menos de 15
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
