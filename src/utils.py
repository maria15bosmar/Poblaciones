import pandas as pd

MAYORIA_EDAD = 25
# PATHS
PATH_DATOS = "antiguo/"
PATH_CENSO = PATH_DATOS + "Censos/"
PATH_CONSORCIO = PATH_DATOS + "Consorcio/"
PATH_CATASTRO = PATH_DATOS + "Catastro/"

TAM_CASAS = (60, 100)

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
PROB_TRABAJO = (0.255, (0.269, 0.259, 0.22, (0.403, 0.825)), (0.183, 0.045, 0.042), 
    (0.208, 0.01, 0.019), (0.027, 0))

def leer_catastro(distrito):
    df = pd.read_csv(PATH_CATASTRO + "casasd" + str(distrito)+ ".csv", delimiter=";", header=None)
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
