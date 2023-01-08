import pandas as pd
import json

MAYORIA_EDAD = 25
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

TAM_CASAS = INPUT_DATA["tam_casas"]
MAX_X = INPUT_DATA["max_x"]
MAX_Y = INPUT_DATA["max_y"]
MIN_X = INPUT_DATA["min_x"]
MIN_Y = INPUT_DATA["min_y"]

def leer_catastro(distrito):
    df = pd.read_csv(PATH_CATASTRO + "casasd" + str(distrito)+ ".csv")
    df[["x", "y"]] = df[["x", "y"]] / 100
    casas_g = df.loc[df.iloc[:,-1]>TAM_CASAS[1]].iloc[:,:-1].values.tolist()
    casas_p = df.loc[df.iloc[:,-1]<TAM_CASAS[0]].iloc[:,:-1].values.tolist()
    casas_m = df.loc[(df.iloc[:,-1]<=TAM_CASAS[1]) & (df.iloc[:,-1]>=TAM_CASAS[0])].iloc[:,:-1].values.tolist()
    return casas_g, casas_m, casas_p

def leer_censo(distrito):
    """ Returns population datasets. """
    df = pd.read_csv(PATH_CENSO + "distrito_" + str(distrito)+ ".csv", delimiter=";")
    hombres = df.iloc[25:,0].to_numpy().sum()
    mujeres = df.iloc[25:,1].to_numpy().sum()
    ninyos = df.iloc[:25,0].to_numpy().sum()
    ninyas = df.iloc[:25,1].to_numpy().sum()
    return df.iloc[:,0], df.iloc[:,1], hombres, mujeres, ninyos, ninyas

def buscar_clave(hash_table: dict, clave: any):
    """ Devuelve el valor corresponiente a una clave en un diccionario
        de claves compuestas. """
    for i, cl in enumerate(hash_table["claves"]):
        if (type(cl) == list and clave in cl) or (clave == cl):
            return hash_table["valores"][i]
    return -1

# PLANEADOR
all_cols = ["id_hog","id_per", "id_via", "sexo", "trabajo", "carnet", 
                    "hora_ini", "hora_fin", "mot_origen", "mot_destino", "vehiculo", "edad", 
                    "num_veh", "num_miembros_fam", "num_adultos", "pueblo_dest"]

num_to_xml = [
    ["m", "f"],
    [["yes", "always"], ["no", "never"]],
    ["no", "yes", "no", "yes", "no", "no", "yes", "yes"]
]