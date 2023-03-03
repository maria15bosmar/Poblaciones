""" Maneja todo lo que tiene que ver con el mapa. """

import pandas as pd
from utils import *

class Cuadrante:
    """ Representa un cuadrante de la cuadrícula del mapa. """
    def __init__(self, nueva):
        self.x1 = nueva[0] # Primera longitud.
        self.x2 = nueva[1] # Segunda longitud.
        self.y1 = nueva[2] # Primera latitud.
        self.y2 = nueva[3] # Segunda latitud.
        # Número de edificios de cada tipo en el cuadrante.
        # ##### CAMBIAR A DICCIONARIO EXTRAÍDO DE JSON
        self.work = 0
        self.medical = 0
        self.leisure = 0
        self.shopping = 0
        self.education = 0


def usosinmuebles(mapa, x_inicial, y_inicial):
    """ Lee el fichero de inmuebles y los añade a cada cuadrante segun su tipología. """
    # Leer datos de no viviendas del catastro.
    df = pd.read_csv(PATH_CATASTRO + "inmuebles.csv")
    df["x"] = df["x"].astype(str).apply(lambda x: x[:-2]).astype(int)
    df["y"] = df["y"].astype(str).apply(lambda x: x[:-2]).astype(int)
    # Limpiar los datos que se salgan de las coordenadas que queremos.
    df["x"] = df[df["x"] < MAX_X]["x"]
    df["y"] = df[df["y"] > MAX_Y]["y"]
    df = df.dropna()
    # Crear cuadrículas.
    df["x"] = ((df["x"] - x_inicial) // 400).astype(int)
    df["y"] = ((y_inicial - df["y"]) // 400).astype(int)
    df = df.join(pd.DataFrame({"celda": df["x"].values + df["y"].values * 15}))
    df = df.dropna()
    df["celda"] = df["celda"].astype(int)
    # Colocar los distintos tipos en inmuebles en su correspondiente cuadrícula.
    for t in df["tipo"].unique():
        df2 = df.loc[df["tipo"] == t]
        for c in df2["celda"].unique():
            df3 = df.loc[df["celda"] == c]
            if t == "I" or t == "O":
                mapa[c].work += df3["tamanyo"].values.sum()
            if t == "Y":
                mapa[c].medical += df3["tamanyo"].values.sum()
            if t == "K" or t == "T" or t == "G" or t == "R":
                mapa[c].leisure += df3["tamanyo"].values.sum()
            if t == "C":
                mapa[c].shopping += df3["tamanyo"].values.sum()
            if t == "E":
                mapa[c].education += df3["tamanyo"].values.sum()
            return mapa


def raster():
    """ Crea la cuadrícula del mapa. """
    mapa = []
    # Generar los objetos cuadrante y colocarlos en una matriz.
    for i in range (15):
        for j in range (15):
            nueva = [MIN_X + 400 * (j), MIN_X + 400 * (j + 1), 
                MIN_Y - 400 * (i), MIN_Y - 400 * (i + 1)]
            mapa.append(Cuadrante(nueva))
    # Introducir los inmuebles en el mapa.
    mapa = usosinmuebles(mapa, MIN_X, MIN_Y)
    return mapa
