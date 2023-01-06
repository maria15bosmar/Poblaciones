import pandas as pd

MAYORIA_EDAD = 25
# PATHS
PATH_DATOS = "resources/input_data/"
PATH_CENSO = PATH_DATOS + "Censos/"
PATH_CONSORCIO = PATH_DATOS + "Consorcio/"
PATH_CATASTRO = PATH_DATOS + "Catastro/"
PATH_JSON = PATH_DATOS + "probabilities.json"

TAM_CASAS = (60, 100)
MAX_X = 438447
MAX_Y = 4462216
MIN_X = 432447
MIN_Y = 4468216

# PERSONAS
RANGOS_EDAD = [18, 25, 35, 45, 55, 65, 75, 85, 96]
DIFERENCIAS_EDAD = [
    (.1916, 0.0, .1159, 0.0, .6925),
    (.2373, .0322, .0768, .0146, .6391),
    (.2926, .0362, .1116, .0738, .4858),
    (.3203, .0414, .1205, .0830, .4348),
    (.3480, .0465, .1294, .0922, .3839),
    (.3251, .0493, .1063, .1088, .4105),
    (.3488, .0439, .1157, .0833, .4083),
    (.3286, .0412, .1201, .1001, .4100),
    (.3366, .0398, .1507, .0638, .4091),
    (.2953, .0365, .1252, .0608, .4822),
    (.3267, .0410, .1139, .0872, .4312),
    (.3419, .0375, .1372, .0348, .4486),
    (.3283, .0260, .1391, .0712, .4354),
    (.3670, .1202, .1754, .1578, .1796),
    (.5123, .1651, .0964, .1165, .1097)
]

CANTIDAD_DIFERENCIA = [(0, 1), (-1), (2, 3), (-2, -3), (4, 5)]

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
    for i in hash_table.keys():
        if (type(i) == tuple and clave in i) or (clave == i):
            return hash_table[i]
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

MODO = {
    (1, 2, 3, 4, 5, 6, 7, 8, 9): "pt", (10): "taxi", 
    (11, 12, 13 ,14, 15, 16, 17, 18, 19, 23): "car",
    (20, 21, 22): "bicicle", (24): "walk"
}

LUGAR = {
    1 : "home",
    (2, 3, 7): "work",
    4: "education",
    5: "shopping",
    6: "medical",
    (8, 9, 10, 11, 12): "leisure"
}

# Código del lugar : (coordenada_x, coordenada_y)
VIAJES_FUERA = {
    (5, 113, 148, 161): (428447, 4464616), # Alcalá de Henares, Pinto, Torrejon de Ardoz, Valdemoro
    (6, 79): (437647, 4468216), # Alcobendas, Madrid
    7 : (432447, 4465716), # Alcorcon
    (22, 45, 80, 115, 127): (432847, 4468216), # Boadilla del Monte, Colmenar Viejo, Majadahonda, Pozuelo de Alarcon, Las Rozas
    (58, 73): (433600, 4462216), # Fuenlabrada, Humanes
    (65, 106): (436847, 4463016), # Getafe, Parla
    92: (432447, 4463016) # Mostoles
}