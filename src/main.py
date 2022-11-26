from constantes import *
import pandas as pd

def leer_censo(distrito):
    """ Returns population datasets. """
    df = pd.read_csv(PATH_CENSO + "distrito_" + str(distrito)+ ".csv", delimiter=";")
    hombres = df.iloc[25:,0]
    mujeres = df.iloc[25:,1]
    ninyos = df.iloc[:25,0]
    ninyas = df.iloc[:25,1]
    return df.iloc[:,0], df.iloc[:,1], hombres, mujeres, ninyos, ninyas

def leer_catastro(distrito):
    df = pd.read_csv(PATH_CATASTRO + "casasd" + str(distrito)+ ".csv", delimiter=";", header=None)
    casas_g = df.loc[df.iloc[:,-1]>TAM_CASAS[1]].iloc[:,:-1]
    casas_p = df.loc[df.iloc[:,-1]<TAM_CASAS[0]].iloc[:,:-1]
    casas_m = df.loc[(df.iloc[:,-1]<=TAM_CASAS[1]) & (df.iloc[:,-1]>=TAM_CASAS[0])].iloc[:,:-1]
    return casas_g, casas_m, casas_p

print(leer_catastro(1))
