
class cuadrante:
  def __init__(self, nueva):
    self.x1 = nueva[0]
    self.x2 = nueva[1]
    self.y1 = nueva[2]
    self.y2 = nueva[3]
    self.work = 0
    self.medical = 0
    self.leisure = 0
    self.shopping = 0
    self.education = 0


def usosinmuebles(mapa, x_inicial, y_inicial):  # Lee el fichero de inmuebles y los añade a cada cuadrante segun su tipologia
    fichero = open('Catastro\inmuebles.csv', 'r+')
    texto = fichero.readlines()
    numero_lineas = len(texto)
    max_Y = 4462216
    for i in range(numero_lineas):
        bool = True
        csvX, csvY, csvtipo, csvtam = texto[i].split(';') # Se guardan los datos del csv en variables
        csvtam = csvtam.replace("\n", "")
        csvX = csvX[:-2]
        csvY = csvY[:-2]
        dist_afinal_X = (int(csvX) - x_inicial) // 400  # Se calcula la celda correspondiente en X
        dist_afinal_Y = (y_inicial - int(csvY)) // 400  # Se calcula la celda correspondiente en Y
        if int(csvX) >= 438447:      # En caso de ser mayor o igual a max_X no es valido el edificio
            bool = False
        if int(csvY) <= 4462216:     # En caso de ser menor o igual a max_Y no es valido el edificio
            bool = False
        if bool == True:
            celda = dist_afinal_X + dist_afinal_Y * 15  # Se calcula el cuadrante donde se situa el edificio
            if csvtipo == "I" or csvtipo == "O":    # Dependiendo de cada tipo se aumenta un tipo
                mapa[celda].work += int(csvtam)
            if csvtipo == "Y":
                mapa[celda].medical += int(csvtam)
            if csvtipo == "K" or csvtipo == "T" or csvtipo == "G" or csvtipo == "R":
                mapa[celda].leisure += int(csvtam)
            if csvtipo == "C":
                mapa[celda].shopping += int(csvtam)
            if csvtipo == "E":
                mapa[celda].education += int(csvtam)
    fichero.close()
    return mapa


def raster():   # Crea la cuadricula del mapa de leganes
    x_inicial = 432447      # MAX X: 438447
    y_inicial = 4468216     # MAX Y: 4462216
    mapa = []
    for i in range (15):
        for j in range (15):
            nueva = [x_inicial + 400 * (j), x_inicial + 400 * (j + 1), y_inicial - 400 * (i), y_inicial - 400 * (i + 1)]
            mapa.append(cuadrante(nueva))
    mapa = usosinmuebles(mapa, x_inicial, y_inicial)
    return mapa


