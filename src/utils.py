""" Contiene constantes y funciones para el programa. """

import json
import numpy as np
import pandas as pd

MAYORIA_EDAD = 25
MAX_AGENTES = 10000000
NOMBRE_FICHERO = "resources/plans_3.xml"
# PATHS
PATH_DATOS = "resources/input_data/"
PATH_CENSO = PATH_DATOS + "Censos/"
PATH_CONSORCIO = PATH_DATOS + "Consorcio/"
PATH_CATASTRO = PATH_DATOS + "Catastro/"
PATH_JSON_FAMILIADOR = PATH_DATOS + "inputs_familiador.json"
PATH_JSON_PLANEADOR = PATH_DATOS + "inputs_planeador.json"

# DATOS PARA EL PLANEADOR.
with open(PATH_JSON_PLANEADOR) as f:
    INPUT_DATA = json.load(f)

# Datos del tamaño de las casas.
TAM_CASAS = INPUT_DATA["tam_casas"]
# Límites del mapa.
MAX_X = INPUT_DATA["max_x"]
MAX_Y = INPUT_DATA["max_y"]
MIN_X = INPUT_DATA["min_x"]
MIN_Y = INPUT_DATA["min_y"]

def leer_catastro(distrito):
    """ Lee los ficheros del catastro y devuelve tres listas de coordenadas de casas. """
    df = pd.read_csv(PATH_CATASTRO + "casasd" + str(distrito)+ ".csv")
    df[["x", "y"]] = df[["x", "y"]] / 100
    # Casas grandes.
    casas_g = df.loc[df.iloc[:,-1]>TAM_CASAS[1]].iloc[:,:-1].values.tolist()
    # Casas medianas.
    casas_p = df.loc[df.iloc[:,-1]<TAM_CASAS[0]].iloc[:,:-1].values.tolist()
    # Casas pequeñas.
    casas_m = df.loc[(df.iloc[:,-1]<=TAM_CASAS[1]) & (df.iloc[:,-1] >= TAM_CASAS[0])].iloc[:,:-1].values.tolist()
    return casas_g, casas_m, casas_p

def leer_censo(distrito):
    """ Devuelve los datos del censo. """
    # Listas de edades por género.
    df = pd.read_csv(PATH_CENSO + "distrito_" + str(distrito)+ ".csv", delimiter=";")
    hombres = df.iloc[25:,0].to_numpy().sum() # Número de hombres adultos.
    mujeres = df.iloc[25:,1].to_numpy().sum() # Número de mujeres adultas.
    ninyos = df.iloc[:25,0].to_numpy().sum() # Número de varones menores de 25.
    ninyas = df.iloc[:25,1].to_numpy().sum() # Número de mujeres menores de 25.
    return df.iloc[:,0], df.iloc[:,1], hombres, mujeres, ninyos, ninyas

def buscar_clave(hash_table: dict, clave: any):
    """ Devuelve el valor corresponiente a una clave en un diccionario
        de claves compuestas. """
    for i, cl in enumerate(hash_table["claves"]):
        if (type(cl) == list and clave in cl) or (clave == cl):
            return hash_table["valores"][i]
    return -1

def probabilidad_disminuida(min, max):
    """ Devuelve un número en un rango, mayor probabilidad de que salga más bajo. """
    return round(np.random.beta(2, 5) * (max - min) + min)

# Nombres de las columnas de los ficheros del consorcio.
all_cols = ["id_hog","id_per", "id_via", "sexo", "trabajo", "carnet", "hora_ini", 
                    "hora_fin", "mot_origen", "mot_destino", "vehiculo", "edad", 
                    "num_veh", "num_miembros_fam", "num_adultos", "pueblo_dest"]

# Lista auxiliar para las strings de los planes.
num_to_xml = [
    ["m", "f"],
    [["yes", "always"], ["no", "never"]],
    ["no", "yes", "no", "yes", "no", "no", "yes", "yes"]
]