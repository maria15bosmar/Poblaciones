import random
import sys
import copy
from planeador import planear
from familia import familia



distrito = 1
id_familias, id_personas = 1, 1
lista_familias = []
def censo():
    global distrito
    hombres, mujeres = [],[]
    totalniñas, totalniños, totalmujeresadultas, totalhombresadultos  = 0, 0, 0, 0
    dir = 'Censos\distrito_.csv'
    index = dir.find('.')
    dir = dir[:index] + str(distrito) + dir[index:]

    fichero = open(dir, 'r+')
    texto = fichero.readlines()
    numero_lineas = len(texto)
    for i in range(numero_lineas):
        if(i>0):
            h, m = texto[i].split(';')
            m = m.replace("\n", "")
            hombres.append(int(h))
            mujeres.append(int(m))
            if(i < 26):  # Es 26 y no 25 porque la primera linea del csv contiene simbolos raros los adultos son a partir de 25
                totalniñas = totalniñas + int(m)
                totalniños = totalniños + int(h)
            else:
                totalmujeresadultas = totalmujeresadultas + int(m)
                totalhombresadultos = totalhombresadultos + int(h)
    distrito += 1
    fichero.close()
    return hombres, mujeres, totalniñas, totalniños, totalmujeresadultas, totalhombresadultos;

def catastro():#12295 21381 34885 53893 65466 70640
    global distrito
    casasp, casasm, casasg, coordenadas = [],[],[],[]
    dir = 'Catastro\casasd.csv'
    index = dir.find('.')
    dir = dir[:index] + str(distrito) + dir[index:]

    fichero = open(dir, 'r+')
    texto = fichero.readlines()
    numero_lineas = len(texto)
    for i in range(numero_lineas):
    #if(i>0):
        csvX, csvY, csvtam = texto[i].split(';')
        csvtam = csvtam.replace("\n", "")
        csvX = csvX[:-2] + "." + csvX[-2:]
        csvY = csvY[:-2] + "." + csvY[-2:]
        coordenadas = [csvX, csvY]
        if int(csvtam) < 60:
            casasp.append(coordenadas)
        elif int(csvtam) >= 60 and int(csvtam) <= 100:
            casasm.append(coordenadas)
        else:
            casasg.append(coordenadas)
    fichero.close()
    return casasp, casasm, casasg;


def numaleatorio():
    return random.randrange(0, 1001)/10


def escogepersonas(lista,edadmin,edadmax,genero):
    global totalniñas
    global totalniños
    global totalmujeresadultas
    global totalhombresadultos
    if edadmax == -1:
        edadmax = edadmin + 4
        edad = edadmin
        """if edadmax > 24:
            #edadmax = 24"""
    if edadmax == -3:  # En caso de edadmax = -1 significa que queremos una edad concreta y si no superior (segundo hijo) y -3 para adulto
        edadmax = edadmin + 4
        edad = edadmin
        if edadmax > 95:
            edadmax = 95
    elif edadmax == -2: # Persona con una edad predefinida
        if edadmin >= 27 and edadmin <=93:
            edad = edadmin
            edadmin = edad - 2
            edadmax = edad + 2
        elif edadmin < 27:
            edad = edadmin
            edadmax = edad + 4
        elif edadmin == 94:
            edad = edadmin
            edadmin = edad - 3
            edadmax = edad + 1
        elif edadmin == 95:
            edad = edadmin
            edadmin = edad - 4
            edadmax = edad
    else:   # Si no, se hace aleatoriamente
        edad = random.randint(edadmin, edadmax)

    boolean = False
    iteraciones = 0
    while boolean != True and iteraciones != edadmax-edadmin + 1 : #bucle para coger personas de la lista
        if lista[edad] > 0:  # Si quedan personas con esa edad la quitamos y terminamos
            print("Borramos a una persona de la lista con " + str(edad) + " años")
            lista[edad] -= 1
            boolean = True
        else:               # Si no quedan personas con esa edad miramos con otra edad dentro del rango
            if edad == edadmax:
                edad = edadmin
            else:
                edad += 1
        iteraciones += 1
    if boolean == True: # Se encuentra una persona
        if genero == 0:
            if edad <= 24:
                totalniños -= 1
                print("Un niño menos " + str(edad))
            else:
                totalhombresadultos -= 1
                print("Un hombre menos " + str(edad))
        elif genero == 1:
            if edad <= 24:
                totalniñas -= 1
                print("Una niña menos " + str(edad))
            else:
                totalmujeresadultas -= 1
                print("Una mujer menos " + str(edad))
        return edad
    else: # No se encuentra una persona
        if edadmax < 24:   # No quedan hijos en ese rango probar con hijos mayores de hasta 24 años
            return escogepersonas(lista, edadmax, 24, genero)
        elif edadmax == 24:  # Probamos para cualquier edad de niño
                return escogepersonas(lista, 0, 24, genero)
        elif edadmax >= 25:
            if edadmax > 90:
                return escogepersonas(lista, 25, 34, genero)
            else:
                return escogepersonas(lista, edadmin + (edadmax-edadmin+1), edadmax + (edadmax-edadmin+1), genero)

def siguienteshijos(hombres, mujeres, edad_primer_hijo, numniños, totalniños, totalniñas, id_personas, personas):
    genero_demas_hijo = sexadorhijos(totalniños, totalniñas, numniños)
    edad_demas_hijos, hijos = [], []
    diferencia = []
    for i in range(numniños):
        diferencia.append(numaleatorio())
        if diferencia[i] >= 0 and diferencia[i] < 1.5:  # Son gemelos o mellizos y tienen la misma edad
            if i == 0:
                edad_demas_hijos.append(edad_primer_hijo)
            else:
                edad_demas_hijos.append(edad_demas_hijos[i-1])
        elif diferencia[i] >= 1.5 and diferencia[i] < 19.0: # Age gap de 1 año
            if i == 0:
                edad_demas_hijos.append(edad_primer_hijo + 1)
            else:
                edad_demas_hijos.append(edad_demas_hijos[i-1] + 1)
        elif diferencia[i] >= 19.0 and diferencia[i] < 36.2: # Age gap de 2 años
            if i == 0:
                edad_demas_hijos.append(edad_primer_hijo + 2)
            else:
                edad_demas_hijos.append(edad_demas_hijos[i-1] + 2)
        elif diferencia[i] >= 36.2 and diferencia[i] < 95.0: # Age gap de entre 3 y 9 años
            agegap = disminucionprobalistica(3, 9, 0)
            if i == 0:
                edad_demas_hijos.append(edad_primer_hijo + agegap)
            else:
                edad_demas_hijos.append(edad_demas_hijos[i-1] + agegap)
        elif diferencia[i] >= 95.0 and diferencia[i] <= 100.0:  # Age gap de mas de 10 años
            agegap = disminucionprobalistica(10, 20, 0)
            if i == 0:
                edad_demas_hijos.append(edad_primer_hijo + agegap)
            else:
                edad_demas_hijos.append(edad_demas_hijos[i-1] + agegap)
        if genero_demas_hijo[i] == 0:
            if edad_demas_hijos[i]+4 > 24 and totalhombresadultos == 0:
                nuevo_hijo = escogepersonas(hombres, 20, -1, 0)
                hijos.append(nuevo_hijo)
            else:
                nuevo_hijo = escogepersonas(hombres, edad_demas_hijos[i], -1, 0)
                hijos.append(nuevo_hijo)
        elif genero_demas_hijo[i] == 1:
            if edad_demas_hijos[i]+4 > 24 and totalmujeresadultas == 0:
                nuevo_hijo = escogepersonas(mujeres, 20, -1, 1)
                hijos.append(nuevo_hijo)
            else:
                nuevo_hijo = escogepersonas(mujeres, edad_demas_hijos[i], -1, 1)
                hijos.append(nuevo_hijo)
        personas.extend([id_personas + i, hijos[i], genero_demas_hijo[i]])
    return personas


def parejador(hombres, mujeres, hayniños, personas):
    global id_personas
    global totalmujeresadultas
    global totalhombresadultos
    if hayniños == 0:  # En caso de ser una pareja sin hijos no se va a tener en cuenta la edad para que haya de todas las edades
        rango_edad_ella = numaleatorio()
    else:
        if hayniños <= 24:  # En caso de haber hijos hay que tener en cuenta la edad a la que los tuvo
            rango_edad_ella = 0
        elif hayniños >= 25 and hayniños <= 29:
            rango_edad_ella = 1.1
        elif hayniños >= 30 and hayniños <= 34:
            rango_edad_ella = 4.8
        elif hayniños >= 35 and hayniños <= 39:
            rango_edad_ella = 13.1
        elif hayniños >= 40 and hayniños <= 44:
            rango_edad_ella = 26.0
        elif hayniños >= 45 and hayniños <= 49:
            rango_edad_ella = 38.9
        elif hayniños >= 50 and hayniños <= 54:
            rango_edad_ella = 51.7
        elif hayniños >= 55 and hayniños <= 59:
            rango_edad_ella = 63.0
        elif hayniños >= 60 and hayniños <= 64:
            rango_edad_ella = 72.5
        elif hayniños >= 65 and hayniños <= 69:
            rango_edad_ella = 80.2
        elif hayniños >= 70 and hayniños <= 74:
            rango_edad_ella = 87.0
    diferencia_edad = numaleatorio()
    if rango_edad_ella >= 0 and rango_edad_ella < 1.1:  # Mujer de menos de 24
        haychico, haychica = quasiadultos(hombres, mujeres, 2)  # se comprueba que existan mujeres jovener menores de 24
        if hayniños == 0:
            edad_ella = random.randint(20, 25)
        else:
            if hayniños < 18:
                edad_ella = 18
            else:
                edad_ella = hayniños
        if haychica == 0:
            edad_ella = 25
        if diferencia_edad >= 0 and diferencia_edad < 19.2:  # Ambos tienen la misma edad o el 1 año mas (homogamia)
            homogamia = random.randint(0, 1)
            if homogamia == 0:
                edad_el = edad_ella
            elif homogamia == 1:
                edad_el = edad_ella + 1
        elif diferencia_edad >= 19.2 and diferencia_edad < 30.8:  # El es 2 o 3 años mayor que ella (hipergamia etárea moderada masculina)
            hipergamiamoma = random.randint(0, 1)
            if hipergamiamoma == 0:  # El es 2 años mayor
                edad_el = edad_ella + 2
            elif hipergamiamoma == 1:  # El es 3 años mayor
                edad_el = edad_ella + 3
        elif diferencia_edad >= 30.8 and diferencia_edad <= 100.0:  # El es mucho mayor (hipergamia etárea elevada masculina)
            if (95 - edad_ella + 4) % 2 == 0:
                edad_el = disminucionprobalistica(edad_ella + 4, 95, 0)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(edad_ella + 5, 95, 0)
    elif rango_edad_ella >= 1.1 and rango_edad_ella < 4.8:  # Mujer entre 25-29
        if hayniños == 0:
            edad_ella = random.randint(25, 30)
        else:
            edad_ella = hayniños
        if diferencia_edad >= 0 and diferencia_edad < 23.7:  # Ambos tienen la misma edad o el 1 año mas (homogamia)
            homogamia = random.randint(0, 1)
            if homogamia == 0:
                edad_el = edad_ella
            elif homogamia == 1:
                edad_el = edad_ella + 1
        elif diferencia_edad >= 23.7 and diferencia_edad < 27.0:  # Ella es un año mayor que el (hipergamia etárea moderada femenina)
            edad_el = edad_ella - 1
        elif diferencia_edad >= 27.0 and diferencia_edad < 34.6:  # El es 2 o 3 años mayor que ella (hipergamia etárea moderada masculina)
            hipergamiamoma = random.randint(0, 1)
            if hipergamiamoma == 0:  # El es 2 años mayor
                edad_el = edad_ella + 2
            elif hipergamiamoma == 1:  # El es 3 años mayor
                edad_el = edad_ella + 3
        elif diferencia_edad >= 34.6 and diferencia_edad < 36.1:  # Ella es mucho mayor (hipergamia etárea elevada femenina)
            if (edad_ella - 2 - 20) % 2 == 0:
                edad_el = disminucionprobalistica(20, edad_ella - 2, 1)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(20, edad_ella - 3, 1)
        elif diferencia_edad >= 36.1 and diferencia_edad <= 100.0:  # El es mucho mayor (hipergamia etárea elevada masculina)
            if (95 - edad_ella + 4) % 2 == 0:
                edad_el = disminucionprobalistica(edad_ella + 4, 95, 0)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(edad_ella + 5, 95, 0)
    elif rango_edad_ella >= 4.8 and rango_edad_ella < 13.1:  # Mujer entre 30-34
        if hayniños == 0:
            edad_ella = random.randint(30, 35)
        else:
            edad_ella = hayniños
        if diferencia_edad >= 0 and diferencia_edad < 29.3:  # Ambos tienen la misma edad o el 1 año mas (homogamia)
            homogamia = random.randint(0, 1)
            if homogamia == 0:
                edad_el = edad_ella
            elif homogamia == 1:
                edad_el = edad_ella + 1
        elif diferencia_edad >= 29.3 and diferencia_edad < 32.9:  # Ella es un año mayor que el (hipergamia etárea moderada femenina)
            edad_el = edad_ella - 1
        elif diferencia_edad >= 32.9 and diferencia_edad < 44.0:  # El es 2 o 3 años mayor que ella (hipergamia etárea moderada masculina)
            hipergamiamoma = random.randint(0, 1)
            if hipergamiamoma == 0:  # El es 2 años mayor
                edad_el = edad_ella + 2
            elif hipergamiamoma == 1:  # El es 3 años mayor
                edad_el = edad_ella + 3
        elif diferencia_edad >= 44.0 and diferencia_edad < 51.4:  # Ella es mucho mayor (hipergamia etárea elevada femenina)
            if (edad_ella - 2 - 20) % 2 == 0:
                edad_el = disminucionprobalistica(20, edad_ella - 2, 1)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(20, edad_ella - 3, 1)
        elif diferencia_edad >= 51.4 and diferencia_edad <= 100.0:  # El es mucho mayor (hipergamia etárea elevada masculina)
            if (95 - edad_ella + 4) % 2 == 0:
                edad_el = disminucionprobalistica(edad_ella + 4, 95, 0)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(edad_ella + 5, 95, 0)
    elif rango_edad_ella >= 13.1 and rango_edad_ella < 26.0:  # Mujer entre 35-39
        if hayniños == 0:
            edad_ella = random.randint(35, 40)
        else:
            edad_ella = hayniños
        if diferencia_edad >= 0 and diferencia_edad < 34.8:  # Ambos tienen la misma edad o el 1 año mas (homogamia)
            homogamia = random.randint(0, 1)
            if homogamia == 0:
                edad_el = edad_ella
            elif homogamia == 1:
                edad_el = edad_ella + 1
        elif diferencia_edad >= 34.8 and diferencia_edad < 39.5:  # Ella es un año mayor que el (hipergamia etárea moderada femenina)
            edad_el = edad_ella - 1
        elif diferencia_edad >= 39.5 and diferencia_edad < 52.4:  # El es 2 o 3 años mayor que ella (hipergamia etárea moderada masculina)
            hipergamiamoma = random.randint(0, 1)
            if hipergamiamoma == 0:  # El es 2 años mayor
                edad_el = edad_ella + 2
            elif hipergamiamoma == 1:  # El es 3 años mayor
                edad_el = edad_ella + 3
        elif diferencia_edad >= 52.4 and diferencia_edad < 61.6:  # Ella es mucho mayor (hipergamia etárea elevada femenina)
            if (edad_ella - 2 - 20) % 2 == 0:
                edad_el = disminucionprobalistica(20, edad_ella - 2, 1)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(20, edad_ella - 3, 1)
        elif diferencia_edad >= 61.6 and diferencia_edad <= 100.0:  # El es mucho mayor (hipergamia etárea elevada masculina)
            if (95 - edad_ella + 4) % 2 == 0:
                edad_el = disminucionprobalistica(edad_ella + 4, 95, 0)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(edad_ella + 5, 95, 0)
    elif rango_edad_ella >= 26.0 and rango_edad_ella < 38.9:  # Mujer entre 40-44
        if hayniños == 0:
            edad_ella = random.randint(40, 45)
        else:
            edad_ella = hayniños
        if diferencia_edad >= 0 and diferencia_edad < 34.8:  # Ambos tienen la misma edad o el 1 año mas (homogamia)
            homogamia = random.randint(0, 1)
            if homogamia == 0:
                edad_el = edad_ella
            elif homogamia == 1:
                edad_el = edad_ella + 1
        elif diferencia_edad >= 34.8 and diferencia_edad < 39.5:  # Ella es un año mayor que el (hipergamia etárea moderada femenina)
            edad_el = edad_ella - 1
        elif diferencia_edad >= 39.5 and diferencia_edad < 52.4:  # El es 2 o 3 años mayor que ella (hipergamia etárea moderada masculina)
            hipergamiamoma = random.randint(0, 1)
            if hipergamiamoma == 0:  # El es 2 años mayor
                edad_el = edad_ella + 2
            elif hipergamiamoma == 1:  # El es 3 años mayor
                edad_el = edad_ella + 3
        elif diferencia_edad >= 52.4 and diferencia_edad < 61.6:  # Ella es mucho mayor (hipergamia etárea elevada femenina)
            if (edad_ella - 2 - 20) % 2 == 0:
                edad_el = disminucionprobalistica(20, edad_ella - 2, 1)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(20, edad_ella - 3, 1)
        elif diferencia_edad >= 61.6 and diferencia_edad <= 100.0:  # El es mucho mayor (hipergamia etárea elevada masculina)
            if (95 - edad_ella + 4) % 2 == 0:
                edad_el = disminucionprobalistica(edad_ella + 4, 95, 0)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(edad_ella + 5, 95, 0)
    elif rango_edad_ella >= 38.9 and rango_edad_ella < 51.7:  # Mujer entre 45-49
        if hayniños == 0:
            edad_ella = random.randint(45, 50)
        else:
            edad_ella = hayniños
        if diferencia_edad >= 0 and diferencia_edad < 32.5:  # Ambos tienen la misma edad o el 1 año mas (homogamia)
            homogamia = random.randint(0, 1)
            if homogamia == 0:
                edad_el = edad_ella
            elif homogamia == 1:
                edad_el = edad_ella + 1
        elif diferencia_edad >= 32.5 and diferencia_edad < 37.4:  # Ella es un año mayor que el (hipergamia etárea moderada femenina)
            edad_el = edad_ella - 1
        elif diferencia_edad >= 37.4 and diferencia_edad < 48.1:  # El es 2 o 3 años mayor que ella (hipergamia etárea moderada masculina)
            hipergamiamoma = random.randint(0, 1)
            if hipergamiamoma == 0:  # El es 2 años mayor
                edad_el = edad_ella + 2
            elif hipergamiamoma == 1:  # El es 3 años mayor
                edad_el = edad_ella + 3
        elif diferencia_edad >= 48.1 and diferencia_edad < 59.0:  # Ella es mucho mayor (hipergamia etárea elevada femenina)
            if (edad_ella - 2 - 20) % 2 == 0:
                edad_el = disminucionprobalistica(20, edad_ella - 2, 1)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(20, edad_ella - 3, 1)
        elif diferencia_edad >= 59.0 and diferencia_edad <= 100.0:  # El es mucho mayor (hipergamia etárea elevada masculina)
            if (95 - edad_ella + 4) % 2 == 0:
                edad_el = disminucionprobalistica(edad_ella + 4, 95, 0)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(edad_ella + 5, 95, 0)
    elif rango_edad_ella >= 51.7 and rango_edad_ella < 63.0:  # Mujer entre 50-54
        if hayniños == 0:
            edad_ella = random.randint(50, 55)
        else:
            edad_ella = hayniños
        if diferencia_edad >= 0 and diferencia_edad < 34.9:  # Ambos tienen la misma edad o el 1 año mas (homogamia)
            homogamia = random.randint(0, 1)
            if homogamia == 0:
                edad_el = edad_ella
            elif homogamia == 1:
                edad_el = edad_ella + 1
        elif diferencia_edad >= 34.9 and diferencia_edad < 39.3:  # Ella es un año mayor que el (hipergamia etárea moderada femenina)
            edad_el = edad_ella - 1
        elif diferencia_edad >= 39.3 and diferencia_edad < 50.8:  # El es 2 o 3 años mayor que ella (hipergamia etárea moderada masculina)
            hipergamiamoma = random.randint(0, 1)
            if hipergamiamoma == 0:  # El es 2 años mayor
                edad_el = edad_ella + 2
            elif hipergamiamoma == 1:  # El es 3 años mayor
                edad_el = edad_ella + 3
        elif diferencia_edad >= 50.8 and diferencia_edad < 59.2:  # Ella es mucho mayor (hipergamia etárea elevada femenina)
            if (edad_ella - 2 - 20) % 2 == 0:
                edad_el = disminucionprobalistica(20, edad_ella - 2, 1)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(20, edad_ella - 3, 1)
        elif diferencia_edad >= 59.2 and diferencia_edad <= 100.0:  # El es mucho mayor (hipergamia etárea elevada masculina)
            if (95 - edad_ella + 4) % 2 == 0:
                edad_el = disminucionprobalistica(edad_ella + 4, 95, 0)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(edad_ella + 5, 95, 0)
    elif rango_edad_ella >= 63.0 and rango_edad_ella < 72.5:  # Mujer entre 55-59
        if hayniños == 0:
            edad_ella = random.randint(55, 60)
        else:
            edad_ella = hayniños
        if diferencia_edad >= 0 and diferencia_edad < 32.9:  # Ambos tienen la misma edad o el 1 año mas (homogamia)
            homogamia = random.randint(0, 1)
            if homogamia == 0:
                edad_el = edad_ella
            elif homogamia == 1:
                edad_el = edad_ella + 1
        elif diferencia_edad >= 32.9 and diferencia_edad < 37.0:  # Ella es un año mayor que el (hipergamia etárea moderada femenina)
            edad_el = edad_ella - 1
        elif diferencia_edad >= 37.0 and diferencia_edad < 49.0:  # El es 2 o 3 años mayor que ella (hipergamia etárea moderada masculina)
            hipergamiamoma = random.randint(0, 1)
            if hipergamiamoma == 0:  # El es 2 años mayor
                edad_el = edad_ella + 2
            elif hipergamiamoma == 1:  # El es 3 años mayor
                edad_el = edad_ella + 3
        elif diferencia_edad >= 49.0 and diferencia_edad < 59.0:  # Ella es mucho mayor (hipergamia etárea elevada femenina)
            if (edad_ella - 2 - 20) % 2 == 0:
                edad_el = disminucionprobalistica(20, edad_ella - 2, 1)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(20, edad_ella - 3, 1)
        elif diferencia_edad >= 59.0 and diferencia_edad <= 100.0:  # El es mucho mayor (hipergamia etárea elevada masculina)
            if (95 - edad_ella + 4) % 2 == 0:
                edad_el = disminucionprobalistica(edad_ella + 4, 95, 0)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(edad_ella + 5, 95, 0)
    elif rango_edad_ella >= 72.5 and rango_edad_ella < 80.2:  # Mujer entre 60-64
        if hayniños == 0:
            edad_ella = random.randint(60, 65)
        else:
            edad_ella = hayniños
        if diferencia_edad >= 0 and diferencia_edad < 33.7:  # Ambos tienen la misma edad o el 1 año mas (homogamia)
            homogamia = random.randint(0, 1)
            if homogamia == 0:
                edad_el = edad_ella
            elif homogamia == 1:
                edad_el = edad_ella + 1
        elif diferencia_edad >= 33.7 and diferencia_edad < 37.6:  # Ella es un año mayor que el (hipergamia etárea moderada femenina)
            edad_el = edad_ella - 1
        elif diferencia_edad >= 37.6 and diferencia_edad < 52.7:  # El es 2 o 3 años mayor que ella (hipergamia etárea moderada masculina)
            hipergamiamoma = random.randint(0, 1)
            if hipergamiamoma == 0:  # El es 2 años mayor
                edad_el = edad_ella + 2
            elif hipergamiamoma == 1:  # El es 3 años mayor
                edad_el = edad_ella + 3
        elif diferencia_edad >= 52.7 and diferencia_edad < 59.1:  # Ella es mucho mayor (hipergamia etárea elevada femenina)
            if (edad_ella - 2 - 20) % 2 == 0:
                edad_el = disminucionprobalistica(20, edad_ella - 2, 1)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(20, edad_ella - 3, 1)
        elif diferencia_edad >= 59.1 and diferencia_edad <= 100.0:  # El es mucho mayor (hipergamia etárea elevada masculina)
            if (95 - edad_ella + 4) % 2 == 0:
                edad_el = disminucionprobalistica(edad_ella + 4, 95, 0)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(edad_ella + 5, 95, 0)
    elif rango_edad_ella >= 80.2 and rango_edad_ella < 87.0:  # Mujer entre 65-69
        if hayniños == 0:
            edad_ella = random.randint(65, 70)
        else:
            edad_ella = hayniños
        if diferencia_edad >= 0 and diferencia_edad < 29.5:  # Ambos tienen la misma edad o el 1 año mas (homogamia)
            homogamia = random.randint(0, 1)
            if homogamia == 0:
                edad_el = edad_ella
            elif homogamia == 1:
                edad_el = edad_ella + 1
        elif diferencia_edad >= 29.5 and diferencia_edad < 33.2:  # Ella es un año mayor que el (hipergamia etárea moderada femenina)
            edad_el = edad_ella - 1
        elif diferencia_edad >= 33.2 and diferencia_edad < 45.7:  # El es 2 o 3 años mayor que ella (hipergamia etárea moderada masculina)
            hipergamiamoma = random.randint(0, 1)
            if hipergamiamoma == 0:  # El es 2 años mayor
                edad_el = edad_ella + 2
            elif hipergamiamoma == 1:  # El es 3 años mayor
                edad_el = edad_ella + 3
        elif diferencia_edad >= 45.7 and diferencia_edad < 51.8:  # Ella es mucho mayor (hipergamia etárea elevada femenina)
            if (edad_ella - 2 - 20) % 2 == 0:
                edad_el = disminucionprobalistica(20, edad_ella - 2, 1)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(20, edad_ella - 3, 1)
        elif diferencia_edad >= 51.8 and diferencia_edad <= 100.0:  # El es mucho mayor (hipergamia etárea elevada masculina)
            if (95 - edad_ella + 4) % 2 == 0:
                edad_el = disminucionprobalistica(edad_ella + 4, 95, 0)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(edad_ella + 5, 95, 0)
    elif rango_edad_ella >= 87.0 and rango_edad_ella < 92.3:  # Mujer entre 70-74
        if hayniños == 0:
            edad_ella = random.randint(70, 75)
        else:
            edad_ella = hayniños
        if diferencia_edad >= 0 and diferencia_edad < 32.7:  # Ambos tienen la misma edad o el 1 año mas (homogamia)
            homogamia = random.randint(0, 1)
            if homogamia == 0:
                edad_el = edad_ella
            elif homogamia == 1:
                edad_el = edad_ella + 1
        elif diferencia_edad >= 32.7 and diferencia_edad < 36.8:  # Ella es un año mayor que el (hipergamia etárea moderada femenina)
            edad_el = edad_ella - 1
        elif diferencia_edad >= 36.8 and diferencia_edad < 48.2:  # El es 2 o 3 años mayor que ella (hipergamia etárea moderada masculina)
            hipergamiamoma = random.randint(0, 1)
            if hipergamiamoma == 0:  # El es 2 años mayor
                edad_el = edad_ella + 2
            elif hipergamiamoma == 1:  # El es 3 años mayor
                edad_el = edad_ella + 3
        elif diferencia_edad >= 48.2 and diferencia_edad < 56.9:  # Ella es mucho mayor (hipergamia etárea elevada femenina)
            if (edad_ella - 2 - 20) % 2 == 0:
                edad_el = disminucionprobalistica(20, edad_ella - 2, 1)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(20, edad_ella - 3, 1)
        elif diferencia_edad >= 56.9 and diferencia_edad <= 100.0:  # El es mucho mayor (hipergamia etárea elevada masculina)
            if (95 - edad_ella + 4) % 2 == 0:
                edad_el = disminucionprobalistica(edad_ella + 4, 95, 0)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(edad_ella + 5, 95, 0)
    elif rango_edad_ella >= 92.3 and rango_edad_ella < 96.6:  # Mujer entre 75-79
        edad_ella = random.randint(75, 80)
        if diferencia_edad >= 0 and diferencia_edad < 34.2:  # Ambos tienen la misma edad o el 1 año mas (homogamia)
            homogamia = random.randint(0, 1)
            if homogamia == 0:
                edad_el = edad_ella
            elif homogamia == 1:
                edad_el = edad_ella + 1
        elif diferencia_edad >= 34.2 and diferencia_edad < 37.9:  # Ella es un año mayor que el (hipergamia etárea moderada femenina)
            edad_el = edad_ella - 1
        elif diferencia_edad >= 37.9 and diferencia_edad < 51.7:  # El es 2 o 3 años mayor que ella (hipergamia etárea moderada masculina)
            hipergamiamoma = random.randint(0, 1)
            if hipergamiamoma == 0:  # El es 2 años mayor
                edad_el = edad_ella + 2
            elif hipergamiamoma == 1:  # El es 3 años mayor
                edad_el = edad_ella + 3
        elif diferencia_edad >= 51.7 and diferencia_edad < 55.1:  # Ella es mucho mayor (hipergamia etárea elevada femenina)
            if (edad_ella - 2 - 20) % 2 == 0:
                edad_el = disminucionprobalistica(20, edad_ella - 2, 1)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(20, edad_ella - 3, 1)
        elif diferencia_edad >= 55.1 and diferencia_edad <= 100.0:  # El es mucho mayor (hipergamia etárea elevada masculina)
            if (95 - edad_ella + 4) % 2 == 0:
                edad_el = disminucionprobalistica(edad_ella + 4, 95, 0)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(edad_ella + 5, 95, 0)
    elif rango_edad_ella >= 96.6 and rango_edad_ella < 98.8:  # Mujer entre 80-84
        edad_ella = random.randint(80, 85)
        if diferencia_edad >= 0 and diferencia_edad < 32.8:  # Ambos tienen la misma edad o el 1 año mas (homogamia)
            homogamia = random.randint(0, 1)
            if homogamia == 0:
                edad_el = edad_ella
            elif homogamia == 1:
                edad_el = edad_ella + 1
        elif diferencia_edad >= 32.8 and diferencia_edad < 35.4:  # Ella es un año mayor que el (hipergamia etárea moderada femenina)
            edad_el = edad_ella - 1
        elif diferencia_edad >= 35.4 and diferencia_edad < 49.3:  # El es 2 o 3 años mayor que ella (hipergamia etárea moderada masculina)
            hipergamiamoma = random.randint(0, 1)
            if hipergamiamoma == 0:  # El es 2 años mayor
                edad_el = edad_ella + 2
            elif hipergamiamoma == 1:  # El es 3 años mayor
                edad_el = edad_ella + 3
        elif diferencia_edad >= 49.3 and diferencia_edad < 56.5:  # Ella es mucho mayor (hipergamia etárea elevada femenina)
            if (edad_ella - 2 - 20) % 2 == 0:
                edad_el = disminucionprobalistica(20, edad_ella - 2, 1)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(20, edad_ella - 3, 1)
        elif diferencia_edad >= 56.5 and diferencia_edad <= 100.0:  # El es mucho mayor (hipergamia etárea elevada masculina)
            if (95 - edad_ella + 4) % 2 == 0:
                edad_el = disminucionprobalistica(edad_ella + 4, 95, 0)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(edad_ella + 5, 95, 0)
    elif rango_edad_ella >= 98.8 and rango_edad_ella < 99.8:  # Mujer entre 85-89
        edad_ella = random.randint(85, 90)
        if diferencia_edad >= 0 and diferencia_edad < 36.7:  # Ambos tienen la misma edad o el 1 año mas (homogamia)
            homogamia = random.randint(0, 1)
            if homogamia == 0:
                edad_el = edad_ella
            elif homogamia == 1:
                edad_el = edad_ella + 1
        elif diferencia_edad >= 36.7 and diferencia_edad < 48.7:  # Ella es un año mayor que el (hipergamia etárea moderada femenina)
            edad_el = edad_ella - 1
        elif diferencia_edad >= 48.7 and diferencia_edad < 66.3:  # El es 2 o 3 años mayor que ella (hipergamia etárea moderada masculina)
            hipergamiamoma = random.randint(0, 1)
            if hipergamiamoma == 0:  # El es 2 años mayor
                edad_el = edad_ella + 2
            elif hipergamiamoma == 1:  # El es 3 años mayor
                edad_el = edad_ella + 3
        elif diferencia_edad >= 66.3 and diferencia_edad < 82.0:  # Ella es mucho mayor (hipergamia etárea elevada femenina)
            if (edad_ella - 2 - 20) % 2 == 0:
                edad_el = disminucionprobalistica(20, edad_ella - 2, 1)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(20, edad_ella - 3, 1)
        elif diferencia_edad >= 82.0 and diferencia_edad <= 100.0:  # El es mucho mayor (hipergamia etárea elevada masculina)
            if (95 - edad_ella + 4) % 2 == 0:
                edad_el = disminucionprobalistica(edad_ella + 4, 95, 0)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(edad_ella + 5, 95, 0)
    elif rango_edad_ella >= 99.8 and rango_edad_ella <= 100:  # Mujer entre 90-95
        edad_ella = random.randint(90, 95)
        if diferencia_edad >= 0 and diferencia_edad < 51.2:  # Ambos tienen la misma edad o el 1 año mas (homogamia)
            edad_el = edad_ella
        elif diferencia_edad >= 51.2 and diferencia_edad < 67.8:  # Ella es un año mayor que el (hipergamia etárea moderada femenina)
            edad_el = edad_ella - 1
        elif diferencia_edad >= 67.8 and diferencia_edad < 77.4:  # El es 2 o 3 años mayor que ella (hipergamia etárea moderada masculina)
            hipergamiamoma = random.randint(0, 1)
            if hipergamiamoma == 0 and edad_ella + 2 <= 95:  # El es 2 años mayor
                edad_el = edad_ella + 2
            elif hipergamiamoma == 1 and edad_ella + 3 <= 95:  # El es 3 años mayor
                edad_el = edad_ella + 3
            else:
                edad_el = edad_ella
        elif diferencia_edad >= 77.4 and diferencia_edad < 89.0:  # Ella es mucho mayor (hipergamia etárea elevada femenina)
            if (edad_ella - 2 - 20) % 2 == 0:
                edad_el = disminucionprobalistica(20, edad_ella - 2, 1)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(20, edad_ella - 3, 1)
        elif diferencia_edad >= 89.0 and diferencia_edad <= 100.0:  # El es mucho mayor (hipergamia etárea elevada masculina)
            if (95 - edad_ella) % 2 == 0:
                edad_el = disminucionprobalistica(edad_ella, 95, 0)  # disminucionprobalistica() solo funciona para impares
            else:
                edad_el = disminucionprobalistica(edad_ella - 1, 95, 0)
    tipo_pareja = numaleatorio()
    boolean = False
    if totalmujeresadultas == 1:    #arregla un bug que no suele pasar
        z = 25
        while z <= 95 and boolean == False:  # Arriba se comprobo si hay adultos pero no si hay personas de 18 a 24 aqui se hace la comprobacion
            if mujeres[z] >= 1:
                boolean = True
            z += 1
        if boolean == True:
            tipo_pareja = 0
        else:
            print("dfdas")
    if totalhombresadultos == 1:  # arregla un bug que no suele pasar
        z = 25
        while z <= 95 and boolean == False:  # Arriba se comprobo si hay adultos pero no si hay personas de 18 a 24 aqui se hace la comprobacion
            if hombres[z] >= 1:
                boolean = True
            z += 1
        if boolean == True:
            tipo_pareja = 1
    if boolean == False:
        if totalmujeresadultas == 0:  # Si solo hay hombres se hace pareja gay
            tipo_pareja = 0
        elif totalhombresadultos == 0:  # Si solo hay mujeres se hace pareja lesbiana
            tipo_pareja = 1
        elif totalhombresadultos == 1 and totalmujeresadultas == 1: # Si solo queda un chico y una chica se hace pareja de distinto sexo
            tipo_pareja = 2
    if edad_el <= 24 or edad_ella <= 24:
        haychico, haychica = quasiadultos(hombres, mujeres, 2)  # se comprueba que existan dos por genero para parejas gays
        if haychico < 2 and edad_el <= 24:
            edad_el = 25
        if haychica < 2 and edad_ella <= 24:
            edad_ella = 25
    if tipo_pareja >= 0 and tipo_pareja < 0.9:  # Pareja Gay
        el = escogepersonas(hombres,edad_el, -2, 0)
        ella = escogepersonas(hombres,edad_ella, -2, 0)
        personas.extend([id_personas, el, 0, id_personas + 1, ella, 0])
    elif tipo_pareja >= 0.9 and tipo_pareja < 1.3:  # Pareja Lesbiana
        el = escogepersonas(mujeres, edad_el, -2, 1)
        ella = escogepersonas(mujeres, edad_ella, -2, 1)
        personas.extend([id_personas, el, 1, id_personas + 1, ella, 1])
    elif tipo_pareja >= 1.3 and tipo_pareja <= 100.0:  # Pareja de distinto sexo
        el = escogepersonas(hombres, edad_el, -2, 0)
        ella = escogepersonas(mujeres, edad_ella, -2, 1)
        personas.extend([id_personas, el, 0, id_personas + 1, ella, 1])
    return personas






def sexadorhijos (totalniños, totalniñas, numniñosaescoger): # da genero a los hijos teniendo en cuenta que queden o no niños suficientes de ambos sexos
    genero_hijos = []
    for z in range(numniñosaescoger):
        genero_hijos.append(random.randint(0, 1))
    if totalniños < numniñosaescoger or totalniñas < numniñosaescoger:  # En el caso de que no queden niños suficientes asignamos sexos
        copia_totalniñas = totalniñas
        copia_totalniños = totalniños
        for x in range(numniñosaescoger):
            if copia_totalniños == 0:
                genero_hijos[x] = 1
                copia_totalniñas -= 1
            elif copia_totalniñas == 0:
                genero_hijos[x] = 0
                copia_totalniños -= 1
            else:
                if genero_hijos[x] == 0:
                    copia_totalniños -= 1
                elif genero_hijos[x] == 1:
                    copia_totalniñas -= 1
    return genero_hijos


def disminucionprobalistica(inicio, fin, invertido): # Va reduciendo las probabilidades cuanta mas edad sea [0-30% 1-25% 2-20% 3-15% 4-10%]
    edad_hijo = numaleatorio()
    porcentajes = []
    particiones = fin - inicio + 1 # cantidad de edades posibles
    porcentajemitad = 100 / particiones # porcentaje en caso de todos iguales
    medio = (particiones-1) / 2 # mitad de particiones
    aux = int(medio)
    if invertido == 0:
        for i in range (aux + 1): # metemos los porcentajes de la mitad incluida hacia la derecha
            ameter = porcentajemitad / (aux + 2)
            porcentajes.append(porcentajemitad - ameter * i)
        for j in range(aux): # metemos los porcentajes de la mitad sin incluirla hacia la izquierda
            porcentajes.insert(0, porcentajemitad + ameter * (j+1))
    elif invertido == 1:
        for i in range (aux + 1): # metemos los porcentajes de la mitad incluida hacia la derecha
            ameter = porcentajemitad / (aux + 2)
            porcentajes.append(porcentajemitad + ameter * i)
        for j in range(aux): # metemos los porcentajes de la mitad sin incluirla hacia la izquierda
            porcentajes.insert(0, porcentajemitad - ameter * (j+1))
    for k in range(particiones):
        if k != 0:
            porcentajes[k] = porcentajes[k] + porcentajes[k-1]
        if edad_hijo <= porcentajes[k]:
            return inicio + k
        elif(k == particiones - 1):  # Como se van perdiendo decimales el ultimo porcentaje no llega nunca al 100 por eso si se llega a este caso devolvemos el ultimo
            return inicio + k


def simplificador (genero_1, genero_2, edadmin, edadmax, hombres, mujeres): #metodo asociado a los hermanos
    asumar = 0
    edades = []
    if genero_1 == 0:
        edades.append(escogepersonas(hombres, edadmin, edadmax, 0))
    elif genero_1 == 1:
        edades.append(escogepersonas(mujeres, edadmin, edadmax, 1))
    diferencia_edad = numaleatorio()
    if diferencia_edad >= 0 and diferencia_edad < 26.0:  # Diferencia entre 0 y 2
        asumar = random.randint(1,2)
    elif diferencia_edad >= 26.0 and diferencia_edad < 60.9:  # Diferencia entre 3 y 5
        asumar = random.randint(4,5)
    elif diferencia_edad >= 60.9 and diferencia_edad < 88.1:  # Diferencia entre 6 y 10
        asumar = random.randint(7,10)
    elif diferencia_edad >= 88.1 and diferencia_edad <= 100.0:  # Diferencia de mas de 11
        asumar = random.randint(12,20)
    mayoromenor = random.randint(0,1)
    edadprimero = edades[0]
    if mayoromenor == 0:
        asumar = asumar * -1
    if edadprimero + asumar > 91: # Para que no se busquen personas de mas de 95
        asumar = 0
    if edadprimero > 91:
        edadprimero = 91
    if edadprimero + asumar <= 24: # Para que no se busquen niños
        asumar = 0
    if genero_2 == 0:
        edades.append(escogepersonas(hombres, edadprimero+asumar, -3, 0))
    elif genero_2 == 1:
        edades.append(escogepersonas(mujeres, edadprimero+asumar, -3, 1))
    return edades

def quasiadultos (hombres, mujeres, cantidad):
    maleboolean = 0
    femaleboolean = 0
    i = 18
    while i <= 24 and (maleboolean < cantidad or femaleboolean < cantidad): # Arriba se comprobo si hay adultos pero no si hay personas de 18 a 24 aqui se hace la comprobacion
        if hombres[i] > 1:
            maleboolean += hombres[i]
        if mujeres[i] > 1:
            femaleboolean += mujeres[i]
        i += 1
    return maleboolean, femaleboolean

def tipodefamilia(tamfamilia, empleo, niños, monopar):
    if tamfamilia == 1 and empleo == 0 and niños == 0:                      #Unipersonal    EnelParo    Sinniños
        tipo = 1
    elif tamfamilia == 1 and empleo == 1 and niños == 0:                    #Unipersonal    Trabajando  Sinniños
        tipo = 2
    elif tamfamilia >= 2 and empleo == 0 and niños == 0:                    #Multipersonal  EnelParo    Sinniños
        tipo = 3
    elif tamfamilia >= 2 and empleo == 1 and niños == 0:                    #Multipersonal  Trabajando  Sinniños
        tipo = 4
    elif tamfamilia >= 2 and empleo == 0 and niños == 1 and monopar == 1:   #Multipersonal  EnelParo    Conniños    Monoparental
        tipo = 5
    elif tamfamilia >= 2 and empleo == 0 and niños == 1 and monopar == 0:   #Multipersonal  EnelParo    Conniños    NoMonoparental
        tipo = 6
    elif tamfamilia >= 2 and empleo == 1 and niños == 1 and monopar == 1:   #Multipersonal  Trabajando  Conniños    Monoparental
        tipo = 7
    elif tamfamilia >= 2 and empleo == 1 and niños == 1 and monopar == 0:   #Multipersonal  Trabajando  Conniños    NoMonoparental
        tipo = 8
    return tipo

def familiador(hombres, mujeres):
    # PASO 1
    tamfamilia = numaleatorio()
    global id_personas
    global id_familias
    global lista_familias
    global totalniñas
    global totalniños
    global totalmujeresadultas
    global totalhombresadultos
    personas = []
    # PASO 2
    if tamfamilia >= 0 and tamfamilia < 25.7 and totalmujeresadultas + totalhombresadultos > 0: # Familia unipersonal
        sexo = 0
        # PASO 3
        edad = numaleatorio()
        genero = numaleatorio()
        if totalmujeresadultas == 0: #Para el caso de que no queden mas mujeres escogemos un hombre
            genero = 0
        elif totalhombresadultos == 0: #Para el caso de que no queden mas hombres escogemos una mujer
            genero = 100
        if edad >= 0 and edad < 1.7:  # Persona entre 18-24
            haychico, haychica = quasiadultos(hombres, mujeres, 1)  # se comprueba que existan dos por genero para parejas gays
            if genero < 45.1:
                if haychico >= 1: # Si hay chicos
                    unipersonal = escogepersonas(hombres, 18, 24, 0)
                elif haychica >= 1: # Si no hay chicos pero si chicas
                    unipersonal = escogepersonas(mujeres, 18, 24, 1)
                    sexo = 1
                else: # Si no hay adolescentes pasamos a adultos
                    unipersonal = escogepersonas(hombres, 25, 34, 0)
            else:
                if haychica >= 1: # Si hay chicas
                    unipersonal = escogepersonas(mujeres, 18, 24, 1)
                    sexo = 1
                elif haychico >= 1: # Si no hay chicas pero si chicos
                    unipersonal = escogepersonas(hombres, 18, 24, 0)
                else: # Si no hay adolescentes pasamos a adultos
                    unipersonal = escogepersonas(mujeres, 25, 34, 1)
                    sexo = 1
        elif edad >= 1.7 and edad < 14.1:  # Persona entre 25-34
            if genero < 48.7:
                unipersonal = escogepersonas(hombres, 25, 34, 0)
            else:
                unipersonal = escogepersonas(mujeres, 25, 34, 1)
                sexo = 1
        elif edad >= 14.1 and edad < 29.0:  # Persona entre 35-44
            if genero < 53.6:
                unipersonal = escogepersonas(hombres, 35, 44, 0)
            else:
                unipersonal = escogepersonas(mujeres, 35, 44, 1)
                sexo = 1
        elif edad >= 29.0 and edad < 44.1:  # Persona entre 45-54
            if genero < 53.4:
                unipersonal = escogepersonas(hombres, 45, 54, 0)
            else:
                unipersonal = escogepersonas(mujeres, 45, 54, 1)
                sexo = 1
        elif edad >= 44.1 and edad < 58.9:  # Persona entre 54-64
            if genero < 43.6:
                unipersonal = escogepersonas(hombres, 55, 64, 0)
            else:
                unipersonal = escogepersonas(mujeres, 55, 64, 1)
                sexo = 1
        elif edad >= 58.9 and edad < 73.2:  # Persona entre 65-74
            if genero < 29.4:
                unipersonal = escogepersonas(hombres, 65, 74, 0)
            else:
                unipersonal = escogepersonas(mujeres, 65, 74, 1)
                sexo = 1
        elif edad >= 73.2 and edad < 88.1:  # Persona entre 75-84
            if genero < 20.3:
                unipersonal = escogepersonas(hombres, 75, 84, 0)
            else:
                unipersonal = escogepersonas(mujeres, 75, 84, 1)
                sexo = 1
        elif edad >= 58.9 and edad <= 100.0:  # Persona mayor de 85
            if genero < 18.2:
                unipersonal = escogepersonas(hombres, 85, 95, 0)
            else:
                unipersonal = escogepersonas(mujeres, 85, 95, 1)
                sexo = 1
        personas.extend([id_personas, unipersonal, sexo])
        probtrabajo = numaleatorio()
        if probtrabajo >= 0 and probtrabajo < 25.5:
            trabajo = 0
        elif probtrabajo >= 25.5 and probtrabajo <= 100.0:
            trabajo = 1
        tipofamilia = tipodefamilia(1, trabajo, 0, -1)
        lista_familias.append(familia(id_familias, personas, casasp, casasm, casasg, tipofamilia))
        id_personas += 1
        id_familias += 1




    elif tamfamilia >= 25.7 and tamfamilia < 55.9: # Familia de 2
        tipo = numaleatorio()
        if tipo >= 0 and tipo < 18.1 and totalmujeresadultas > 0 and totalniños + totalniñas > 0:  # Familia Monoparental Madre
            genero_hijo = sexadorhijos(totalniños, totalniñas, 1)
            edad_madre = numaleatorio() # Persona entre 15-24 no es representativo
            if edad_madre >= 0 and edad_madre < 2.0:  # Persona entre 25-34
                madre = escogepersonas(mujeres, 25, 34, 1)
            elif edad_madre >= 2.0 and edad_madre < 17.0:  # Persona entre 35-44
                madre = escogepersonas(mujeres, 35, 44, 1)
            elif edad_madre >= 17.0 and edad_madre < 43.8:  # Persona entre 45-54
                madre = escogepersonas(mujeres, 45, 54, 1)
            elif edad_madre >= 43.8 and edad_madre < 64.5:  # Persona entre 55-64
                madre = escogepersonas(mujeres, 55, 64, 1)
            elif edad_madre >= 64.5 and edad_madre <= 100.0:  # Persona de más de 65
                madre = escogepersonas(mujeres, 65, 95, 1)
            if madre <= 38:  # Para que las madres solo puedan tener hijos a partir de los 15 años
                if genero_hijo[0] == 0:
                    hijo = escogepersonas(hombres,0,madre-15, 0)
                elif genero_hijo[0] == 1:
                    hijo = escogepersonas(mujeres, 0, madre-15, 1)
            if madre > 38:
                if genero_hijo[0] == 0:
                    hijo = escogepersonas(hombres, 0, 24, 0)
                elif genero_hijo[0] == 1:
                    hijo = escogepersonas(mujeres, 0, 24, 1)
            personas.extend([id_personas, madre, 1, id_personas+1, hijo, genero_hijo[0]])
            probtrabajo = numaleatorio()
            if probtrabajo >= 0 and probtrabajo < 26.9:
                trabajo = 0
            elif probtrabajo >= 26.9 and probtrabajo <= 100.0:
                trabajo = 1
            tipofamilia = tipodefamilia(2, trabajo, 1, 1)
            lista_familias.append(familia(id_familias, personas, casasp, casasm, casasg, tipofamilia))
            id_personas += 2
            id_familias += 1

        elif tipo >= 18.1 and tipo < 22.0 and totalhombresadultos > 0 and totalniños + totalniñas > 0:  # Familia Monoparental Padre
            genero_hijo = sexadorhijos(totalniños, totalniñas, 1)
            edad_padre = numaleatorio()  # Persona entre 15-24 no es representativo
            if edad_padre >= 0 and edad_padre < 2.0:  # Persona entre 25-34
                padre = escogepersonas(hombres, 25, 34, 0)
            elif edad_padre >= 2.0 and edad_padre < 17.0:  # Persona entre 35-44
                padre = escogepersonas(hombres, 35, 44, 0)
            elif edad_padre >= 17.0 and edad_padre < 43.8:  # Persona entre 45-54
                padre = escogepersonas(hombres, 45, 54, 0)
            elif edad_padre >= 43.8 and edad_padre < 64.5:  # Persona entre 55-64
                padre = escogepersonas(hombres, 55, 64, 0)
            elif edad_padre >= 64.5 and edad_padre <= 100.0:  # Persona de más de 65
                padre = escogepersonas(hombres, 65, 95, 0)
            if padre <= 38:  # Para que los padres solo puedan tener hijos a partir de los 15 años
                if genero_hijo[0] == 0:
                    hijo = escogepersonas(hombres, 0, padre - 15, 0)
                elif genero_hijo[0] == 1:
                    hijo = escogepersonas(mujeres, 0, padre - 15, 1)
            if padre > 38:
                if genero_hijo[0] == 0:
                    hijo = escogepersonas(hombres, 0, 24, 0)
                elif genero_hijo[0] == 1:
                    hijo = escogepersonas(mujeres, 0, 24, 1)
            personas.extend([id_personas, padre, 0, id_personas + 1, hijo, genero_hijo[0]])
            probtrabajo = numaleatorio()
            if probtrabajo >= 0 and probtrabajo < 25.9:
                trabajo = 0
            elif probtrabajo >= 25.9 and probtrabajo <= 100.0:
                trabajo = 1
            tipofamilia = tipodefamilia(2, trabajo, 1, 1)
            lista_familias.append(familia(id_familias, personas, casasp, casasm, casasg, tipofamilia))
            id_personas += 2
            id_familias += 1

        elif tipo >= 22.0 and tipo < 89.4 and totalhombresadultos + totalmujeresadultas > 1:  # Pareja adulta
            personas = parejador(hombres, mujeres, 0, personas)
            probtrabajo = numaleatorio()
            if probtrabajo >= 0 and probtrabajo < 22.0:
                trabajo = 0
            elif probtrabajo >= 22.0 and probtrabajo <= 100.0:
                trabajo = 1
            tipofamilia = tipodefamilia(2, trabajo, 0, -1)
            lista_familias.append(familia(id_familias, personas, casasp, casasm, casasg, tipofamilia))
            id_personas += 2
            id_familias += 1

        elif tipo >= 89.4 and tipo <= 100.0 and totalhombresadultos + totalmujeresadultas > 1:  # Personas que no forman ningún núcleo familiar entre sí
            subtipo = numaleatorio()

            if subtipo >= 0 and subtipo < 40.2:  # Hermanos
                rango_edad = numaleatorio()
                genero = numaleatorio()
                boolean = False
                if totalmujeresadultas == 1:  # arregla un bug que no suele pasar
                    z = 25
                    while z <= 95 and boolean == False:  # Arriba se comprobo si hay adultos pero no si hay personas de 18 a 24 aqui se hace la comprobacion
                        if mujeres[z] >= 1:
                            boolean = True
                        z += 1
                    if boolean == True:
                        genero = 30.3
                if totalhombresadultos == 1:  # arregla un bug que no suele pasar
                    z = 25
                    while z <= 95 and boolean == False:  # Arriba se comprobo si hay adultos pero no si hay personas de 18 a 24 aqui se hace la comprobacion
                        if hombres[z] >= 1:
                            boolean = True
                        z += 1
                    if boolean == True:
                        genero = 0
                    else:
                        print("gdsgsd")
                if boolean == False:
                    if totalhombresadultos == 0:# Si no hay hombres forzamos a que sean mujeres
                        genero = 0
                    elif totalmujeresadultas == 0:
                        genero = 30.3
                    elif totalmujeresadultas == 1 and totalhombresadultos == 1:
                        genero = 58.0
                if genero >= 0 and genero < 30.3:  # Ambas chicas
                    genero_1 = 1
                    genero_2 = 1
                elif genero >= 30.3 and genero < 58.0:  # Ambos chicos
                    genero_1 = 0
                    genero_2 = 0
                elif genero >= 58.0 and genero <= 100.0:  # Un chico y una chica
                    genero_1 = 0
                    genero_2 = 1
                if rango_edad >= 0 and rango_edad < 4.3:  # Persona entre 18-24
                    haychico, haychica = quasiadultos(hombres, mujeres, 2) # se comprueba que existan dos personas por genero
                    if totalmujeresadultas > 1 and totalhombresadultos > 1: # si hay adolescentes pero luego con la diferencia de edad coge un adulto y no hay adultos falla por eso con esto nos aseguramos
                        if haychico >= 2 and haychica >= 2:
                            edades = simplificador(genero_1, genero_2, 18, 24, hombres, mujeres)
                        elif haychico == 1 and haychica == 1:
                            edades = simplificador(0, 1, 18, 24, hombres, mujeres)
                        elif haychico == 0 and haychica >= 2:
                            edades = simplificador(1, 1, 18, 24, hombres, mujeres)
                        elif haychico >= 2 and haychica == 0:
                            edades = simplificador(0, 0, 18, 24, hombres, mujeres)
                        else:
                            edades = simplificador(genero_1, genero_2, 25, 34, hombres, mujeres)
                    else:
                        edades = simplificador(genero_1, genero_2, 25, 34, hombres, mujeres)
                elif rango_edad >= 4.3 and rango_edad < 14.0:  # Persona entre 25-34
                    edades = simplificador(genero_1, genero_2, 25, 34, hombres, mujeres)
                elif rango_edad >= 14.0 and rango_edad < 24.7:  # Persona entre 35-44
                    edades = simplificador(genero_1, genero_2, 35, 44, hombres, mujeres)
                elif rango_edad >= 24.7 and rango_edad < 41.2:  # Persona entre 45-54
                    edades = simplificador(genero_1, genero_2, 45, 54, hombres, mujeres)
                elif rango_edad >= 41.2 and rango_edad < 64.4:  # Persona entre 55-64
                    edades = simplificador(genero_1, genero_2, 55, 64, hombres, mujeres)
                elif rango_edad >= 64.4 and rango_edad < 83.5:  # Persona entre 65-74
                    edades = simplificador(genero_1, genero_2, 65, 74, hombres, mujeres)
                elif rango_edad >= 83.5 and rango_edad < 93.2:  # Persona entre 75-84
                    edades = simplificador(genero_1, genero_2, 75, 84, hombres, mujeres)
                elif rango_edad >= 93.2 and rango_edad <= 100:  # Persona de más de 85
                    edades = simplificador(genero_1, genero_2, 85, 95, hombres, mujeres)
                personas.extend([id_personas, edades[0], genero_1, id_personas + 1, edades[1], genero_2])
                probtrabajo = numaleatorio()
                if probtrabajo >= 0 and probtrabajo < 40.3:
                    trabajo = 0
                elif probtrabajo >= 40.3 and probtrabajo <= 100.0:
                    trabajo = 1
                tipofamilia = tipodefamilia(2, trabajo, 0, -1)
                lista_familias.append(familia(id_familias, personas, casasp, casasm, casasg, tipofamilia))  # Sacar fuera si termino otro familiar y sin parentesco
                id_personas += 2
                id_familias += 1

            elif subtipo >= 40.2 and subtipo < 48.4 and totalniños + totalniñas > 0:  # Abuelo-Nieto                                    CUIDADO EL PORCENTAJE ES 48.4 y no es <= es solo <
                generoabuelo = numaleatorio()
                generonieto = numaleatorio()
                rango_edad_nieto = numaleatorio()
                if generoabuelo >= 0 and generoabuelo < 14.8:  # Abuelo
                    genero_abu = 0
                elif generoabuelo >= 14.8 and generoabuelo <= 100.0:  # Abuela
                    genero_abu = 1
                if generonieto >= 0 and generonieto < 61.7:  # Nieto
                    genero_nie = 0
                elif generonieto >= 61.7 and generonieto <= 100.0:  # Nieta
                    genero_nie = 1
                if totalniños == 0:
                    genero_nie = 1
                elif totalniñas == 0:
                    genero_nie = 0
                if totalhombresadultos == 0:
                    genero_abu = 1
                elif totalmujeresadultas == 0:
                    genero_abu = 0
                if rango_edad_nieto >= 38.3 and genero_nie == 0 and totalhombresadultos == 0:
                    rango_edad_nieto = 0
                elif rango_edad_nieto >= 38.3 and genero_nie == 1 and totalmujeresadultas == 0:
                    rango_edad_nieto = 0
                if rango_edad_nieto >= 0 and rango_edad_nieto < 3.2:  # Persona entre 0-9
                    if genero_nie == 0:
                        nieto = escogepersonas(hombres, 0, 9, 0)
                    elif genero_nie == 1:
                        nieto = escogepersonas(mujeres, 0, 9, 1)
                elif rango_edad_nieto >= 3.2 and rango_edad_nieto < 22.4:  # Persona entre 10-19
                    if genero_nie == 0:
                        nieto = escogepersonas(hombres, 10, 19, 0)
                    elif genero_nie == 1:
                        nieto = escogepersonas(mujeres, 10, 19, 1)
                elif rango_edad_nieto >= 22.4 and rango_edad_nieto < 38.3:  # Persona entre 20-24
                    if genero_nie == 0:
                        nieto = escogepersonas(hombres, 20, 24, 0)
                    elif genero_nie == 1:
                        nieto = escogepersonas(mujeres, 20, 24, 1)
                elif rango_edad_nieto >= 38.3 and rango_edad_nieto < 70.5:  # Persona entre 25-29
                    if genero_nie == 0:
                        nieto = escogepersonas(hombres, 25, 29, 0)
                    elif genero_nie == 1:
                        nieto = escogepersonas(mujeres, 25, 29, 1)
                elif rango_edad_nieto >= 70.5 and rango_edad_nieto < 89.1:  # Persona entre 30-34
                    if genero_nie == 0:
                        nieto = escogepersonas(hombres, 30, 34, 0)
                    elif genero_nie == 1:
                        nieto = escogepersonas(mujeres, 30, 34, 1)
                elif rango_edad_nieto >= 89.1 and rango_edad_nieto < 95.6:  # Persona entre 35-39
                    if genero_nie == 0:
                        nieto = escogepersonas(hombres, 35, 39, 0)
                    elif genero_nie == 1:
                        nieto = escogepersonas(mujeres, 35, 39, 1)
                elif rango_edad_nieto >= 95.1 and rango_edad_nieto <= 100.0:  # Persona mayor a 40
                    dismin = disminucionprobalistica(40, 50, 0)
                    if genero_nie == 0:
                        nieto = escogepersonas(hombres, dismin, -2, 0)
                    elif genero_nie == 1:
                        nieto = escogepersonas(mujeres, dismin, -2, 1)
                inicio = 0
                mindifedad = nieto + 40
                if mindifedad > 45:
                    inicio = 6
                if mindifedad > 55:
                    inicio = 17
                if mindifedad > 65:
                    inicio = 66
                if mindifedad > 75:
                    inicio = 293
                if mindifedad > 85:
                    inicio = 669
                rango_edad_abuelo = random.randrange(inicio, 1001) / 10
                if rango_edad_abuelo >= 0 and rango_edad_abuelo < 0.6:  # Persona entre 34-44
                    dismin = disminucionprobalistica(34, 44, 1)
                    if genero_abu == 0:
                        abuelo = escogepersonas(hombres, dismin, -2, 0)
                    elif genero_abu == 1:
                        abuelo = escogepersonas(mujeres, dismin, -2, 1)
                elif rango_edad_abuelo >= 0.6 and rango_edad_abuelo < 1.7:  # Persona entre 45-54
                    if genero_abu == 0:
                        abuelo = escogepersonas(hombres, 45, 54, 0)
                    elif genero_abu == 1:
                        abuelo = escogepersonas(mujeres, 45, 54, 1)
                elif rango_edad_abuelo >= 1.7 and rango_edad_abuelo < 6.6:  # Persona entre 55-64
                    if genero_abu == 0:
                        abuelo = escogepersonas(hombres, 55, 64, 0)
                    elif genero_abu == 1:
                        abuelo = escogepersonas(mujeres, 55, 64, 1)
                elif rango_edad_abuelo >= 6.6 and rango_edad_abuelo < 29.3:  # Persona entre 65-74
                    if genero_abu == 0:
                        abuelo = escogepersonas(hombres, 65, 74, 0)
                    elif genero_abu == 1:
                        abuelo = escogepersonas(mujeres, 65, 74, 1)
                elif rango_edad_abuelo >= 29.3 and rango_edad_abuelo < 66.9:  # Persona entre 75-84
                    if genero_abu == 0:
                        abuelo = escogepersonas(hombres, 75, 84, 0)
                    elif genero_abu == 1:
                        abuelo = escogepersonas(mujeres, 75, 84, 1)
                elif rango_edad_abuelo >= 66.9 and rango_edad_abuelo <= 100.0:  # Persona entre 85-95
                    if genero_abu == 0:
                        abuelo = escogepersonas(hombres, 85, 95, 0)
                    elif genero_abu == 1:
                        abuelo = escogepersonas(mujeres, 85, 95, 1)
                personas.extend([id_personas, abuelo, genero_abu, id_personas + 1, nieto, genero_nie])
                probtrabajo = numaleatorio()
                if probtrabajo >= 0 and probtrabajo < 82.5:
                    trabajo = 0
                elif probtrabajo >= 82.5 and probtrabajo <= 100.0:
                    trabajo = 1
                if nieto > 24:
                    tipofamilia = tipodefamilia(2, trabajo, 0, -1)
                else:
                    tipofamilia = tipodefamilia(2, trabajo, 1, 1)
                lista_familias.append(familia(id_familias, personas, casasp, casasm, casasg, tipofamilia)) #Sacar fuera si termino otro familiar y sin parentesco
                id_personas += 2
                id_familias += 1
            '''
            elif subtipo >= 48.4 and subtipo < 59.1:  # Otro familiar
                padre = escogepersonas(hombres, 45, 54, 0)
            elif subtipo >= 59.1 and subtipo <= 100.0:  # Sin parentesco
                padre = escogepersonas(hombres, 55, 64, 0)
            id_personas += 2
            id_familias += 1
            '''




    elif tamfamilia >= 55.9 and tamfamilia < 76.0: # Familia de 3
        tipo = numaleatorio()
        if tipo >= 0 and tipo < 11.5 and totalmujeresadultas > 0 and totalniños + totalniñas > 1:  # Familia Monoparental Madre con dos hijos
            genero_primer_hijo = sexadorhijos(totalniños, totalniñas, 1)
            edad_madre = numaleatorio()  # Persona entre 15-24 no es representativo
            if edad_madre >= 0 and edad_madre < 2.0:  # Persona entre 25-34
                madre = escogepersonas(mujeres, 25, 34, 1)
            elif edad_madre >= 2.0 and edad_madre < 17.0:  # Persona entre 35-44
                madre = escogepersonas(mujeres, 35, 44, 1)
            elif edad_madre >= 17.0 and edad_madre < 43.8:  # Persona entre 45-54
                madre = escogepersonas(mujeres, 45, 54, 1)
            elif edad_madre >= 43.8 and edad_madre < 64.5:  # Persona entre 55-64
                madre = escogepersonas(mujeres, 55, 64, 1)
            elif edad_madre >= 64.5 and edad_madre <= 100.0:  # Persona de más de 65
                madre = escogepersonas(mujeres, 65, 95, 1)
            if madre <= 38:  # Para que las madres solo puedan tener hijos a partir de los 15 años
                if genero_primer_hijo[0] == 0:
                    edad_primer_hijo = escogepersonas(hombres, 0, madre - 15, 0)
                elif genero_primer_hijo[0] == 1:
                    edad_primer_hijo = escogepersonas(mujeres, 0, madre - 15, 1)
            if madre > 38:
                if genero_primer_hijo[0] == 0:
                    edad_primer_hijo = escogepersonas(hombres, 0, 24, 0)
                elif genero_primer_hijo[0] == 1:
                    edad_primer_hijo = escogepersonas(mujeres, 0, 24, 1)
            personas.extend([id_personas, madre, 1, id_personas + 1, edad_primer_hijo, genero_primer_hijo[0]])
            personas = siguienteshijos(hombres, mujeres, edad_primer_hijo, 1, totalniños, totalniñas, id_personas + 2, personas)
            probtrabajo = numaleatorio()
            if probtrabajo >= 0 and probtrabajo < 18.3:
                trabajo = 0
            elif probtrabajo >= 18.3 and probtrabajo <= 100.0:
                trabajo = 1
            if personas[7] > 24:    #Prueba de que un hijo ya es mayor y ya no es monoparental
                tipofamilia = tipodefamilia(3, trabajo, 1, 0)
            else:
                tipofamilia = tipodefamilia(3, trabajo, 1, 1)
            lista_familias.append(familia(id_familias, personas, casasp, casasm, casasg, tipofamilia))
            id_personas += 3
            id_familias += 1


        elif tipo >= 11.5 and tipo < 13.7 and totalhombresadultos > 0 and totalniños + totalniñas > 1:  # Familia Monoparental Padre con dos hijos
            genero_primer_hijo = sexadorhijos(totalniños, totalniñas, 1)
            edad_padre = numaleatorio()  # Persona entre 15-24 no es representativo
            if edad_padre >= 0 and edad_padre < 2.0:  # Persona entre 25-34
                padre = escogepersonas(hombres, 25, 34, 0)
            elif edad_padre >= 2.0 and edad_padre < 17.0:  # Persona entre 35-44
                padre = escogepersonas(hombres, 35, 44, 0)
            elif edad_padre >= 17.0 and edad_padre < 43.8:  # Persona entre 45-54
                padre = escogepersonas(hombres, 45, 54, 0)
            elif edad_padre >= 43.8 and edad_padre < 64.5:  # Persona entre 55-64
                padre = escogepersonas(hombres, 55, 64, 0)
            elif edad_padre >= 64.5 and edad_padre <= 100.0:  # Persona de más de 65
                padre = escogepersonas(hombres, 65, 95, 0)
            if padre <= 38:  # Para que los padres solo puedan tener hijos a partir de los 15 años
                if genero_primer_hijo[0] == 0:
                    edad_primer_hijo = escogepersonas(hombres, 0, padre - 15, 0)
                elif genero_primer_hijo[0] == 1:
                    edad_primer_hijo = escogepersonas(mujeres, 0, padre - 15, 1)
            if padre > 38:
                if genero_primer_hijo[0] == 0:
                    edad_primer_hijo = escogepersonas(hombres, 0, 24, 0)
                elif genero_primer_hijo[0] == 1:
                    edad_primer_hijo = escogepersonas(mujeres, 0, 24, 1)
            personas.extend([id_personas, padre, 0, id_personas + 1, edad_primer_hijo, genero_primer_hijo[0]])
            personas = siguienteshijos(hombres, mujeres, edad_primer_hijo, 1, totalniños, totalniñas, id_personas + 2, personas)
            probtrabajo = numaleatorio()
            if probtrabajo >= 0 and probtrabajo < 4.5:
                trabajo = 0
            elif probtrabajo >= 4.5 and probtrabajo <= 100.0:
                trabajo = 1
            if personas[7] > 24:    #Prueba de que un hijo ya es mayor y ya no es monoparental
                tipofamilia = tipodefamilia(3, trabajo, 1, 0)
            else:
                tipofamilia = tipodefamilia(3, trabajo, 1, 1)
            lista_familias.append(familia(id_familias, personas, casasp, casasm, casasg, tipofamilia))
            id_personas += 3
            id_familias += 1


        elif (tipo >= 13.7 and tipo < 87.7 and totalhombresadultos + totalmujeresadultas > 1 and totalniños + totalniñas > 0):  # Pareja con un hijo
            genero_hijo = sexadorhijos(totalniños, totalniñas, 1)
            if genero_hijo[0] == 0:
                edad_hijo = escogepersonas(hombres, 0, 24, 0)
            elif genero_hijo[0] == 1:
                edad_hijo = escogepersonas(mujeres, 0, 24, 1)
            edad_nacimiento = numaleatorio()  # Primero se saca estadisticamente a que edad tuvo la madre el hijo para luego sacar la edad de la madre
            if (edad_nacimiento >= 0 and edad_nacimiento < 1.8):  # La madre dio a luz cuando tenia entre 15-19
                edad_madre = random.randint(15, 19)
                personas = parejador(hombres, mujeres, edad_madre + edad_hijo, personas)
            elif (edad_nacimiento >= 1.8 and edad_nacimiento < 9.3):  # La madre dio a luz cuando tenia entre 20-24
                edad_madre = random.randint(20, 24)
                personas = parejador(hombres, mujeres, edad_madre + edad_hijo, personas)
            elif (edad_nacimiento >= 9.3 and edad_nacimiento < 26.7):  # La madre dio a luz cuando tenia entre 25-29
                edad_madre = random.randint(25, 29)
                personas = parejador(hombres, mujeres, edad_madre + edad_hijo, personas)
            elif (edad_nacimiento >= 26.7 and edad_nacimiento < 59.3):  # La madre dio a luz cuando tenia entre 30-34
                edad_madre = random.randint(30, 34)
                personas = parejador(hombres, mujeres, edad_madre + edad_hijo, personas)
            elif (edad_nacimiento >= 59.3 and edad_nacimiento < 89.6):  # La madre dio a luz cuando tenia entre 35-39
                edad_madre = random.randint(35, 39)
                personas = parejador(hombres, mujeres, edad_madre + edad_hijo, personas)
            elif (edad_nacimiento >= 89.6 and edad_nacimiento < 99.1):  # La madre dio a luz cuando tenia entre 40-44
                edad_madre = random.randint(40, 44)
                personas = parejador(hombres, mujeres, edad_madre + edad_hijo, personas)
            elif (edad_nacimiento >= 99.1 and edad_nacimiento <= 100.0):  # La madre dio a luz cuando tenia mas de 45
                edad_madre = random.randint(45, 49)
                personas = parejador(hombres, mujeres, edad_madre + edad_hijo, personas)
            personas.extend([id_personas + 2, edad_hijo, genero_hijo[0]])  # Sumamos 2 al id porque en el parejador se metieron los padres
            probtrabajo = numaleatorio()
            if probtrabajo >= 0 and probtrabajo < 4.2:
                trabajo = 0
            elif probtrabajo >= 4.2 and probtrabajo <= 100.0:
                trabajo = 1
            tipofamilia = tipodefamilia(3, trabajo, 1, 0)
            lista_familias.append(familia(id_familias, personas, casasp, casasm, casasg, tipofamilia))
            id_personas += 3
            id_familias += 1

        # REVISAR NUMERO DE ADULTOS Y NIÑOS DISPONIBLES DISTINTAS FORMAS DE FAMILIAS
        '''elif (tipo >= 87.7 and tipo < 96.6 and totalhombresadultos + totalmujeresadultas > 2 and totalniños + totalniñas > 0):  # Núcleo familiar con otras personas que no forman núcleo familiar (Abuelo)
            id_personas += 3
            id_familias += 1


        elif (tipo >= 96.6 and tipo <= 100.0 and totalhombresadultos + totalmujeresadultas > 2):  # Personas que no forman ningún núcleo familiar entre sí
            id_personas += 3
            id_familias += 1'''


    elif tamfamilia >= 76.0 and tamfamilia < 93.6: # Familia de 4
        tipo = numaleatorio()
        if tipo >= 0 and tipo < 2.9 and totalmujeresadultas > 0 and totalniños + totalniñas > 2:  # Familia Monoparental Madre con tres hijos
            genero_primer_hijo = sexadorhijos(totalniños, totalniñas, 1)
            edad_madre = numaleatorio()  # Persona entre 15-24 no es representativo
            if edad_madre >= 0 and edad_madre < 2.0:  # Persona entre 25-34
                madre = escogepersonas(mujeres, 25, 34, 1)
            elif edad_madre >= 2.0 and edad_madre < 17.0:  # Persona entre 35-44
                madre = escogepersonas(mujeres, 35, 44, 1)
            elif edad_madre >= 17.0 and edad_madre < 43.8:  # Persona entre 45-54
                madre = escogepersonas(mujeres, 45, 54, 1)
            elif edad_madre >= 43.8 and edad_madre < 64.5:  # Persona entre 55-64
                madre = escogepersonas(mujeres, 55, 64, 1)
            elif edad_madre >= 64.5 and edad_madre <= 100.0:  # Persona de más de 65
                madre = escogepersonas(mujeres, 65, 95, 1)
            if madre <= 38:  # Para que las madres solo puedan tener hijos a partir de los 15 años
                if genero_primer_hijo[0] == 0:
                    edad_primer_hijo = escogepersonas(hombres, 0, madre - 15, 0)
                elif genero_primer_hijo[0] == 1:
                    edad_primer_hijo = escogepersonas(mujeres, 0, madre - 15, 1)
            if madre > 38:
                if genero_primer_hijo[0] == 0:
                    edad_primer_hijo = escogepersonas(hombres, 0, 24, 0)
                elif genero_primer_hijo[0] == 1:
                    edad_primer_hijo = escogepersonas(mujeres, 0, 24, 1)
            personas.extend([id_personas, madre, 1, id_personas + 1, edad_primer_hijo, genero_primer_hijo[0]])
            personas = siguienteshijos(hombres, mujeres, edad_primer_hijo, 2, totalniños, totalniñas, id_personas + 2, personas)
            probtrabajo = numaleatorio()
            if probtrabajo >= 0 and probtrabajo < 20.8:
                trabajo = 0
            elif probtrabajo >= 20.8 and probtrabajo <= 100.0:
                trabajo = 1
            if personas[7] > 24 or personas[10] > 24:  # Prueba de que un hijo ya es mayor y ya no es monoparental
                tipofamilia = tipodefamilia(4, trabajo, 1, 0)
            else:
                tipofamilia = tipodefamilia(4, trabajo, 1, 1)
            lista_familias.append(familia(id_familias, personas, casasp, casasm, casasg, tipofamilia))
            id_personas += 4
            id_familias += 1

        elif tipo >= 2.9 and tipo < 3.2 and totalhombresadultos > 0 and totalniños + totalniñas > 2:  # Familia Monoparental Padre con tres hijos
            genero_primer_hijo = sexadorhijos(totalniños, totalniñas, 1)
            edad_padre = numaleatorio()  # Persona entre 15-24 no es representativo
            if edad_padre >= 0 and edad_padre < 2.0:  # Persona entre 25-34
                padre = escogepersonas(hombres, 25, 34, 0)
            elif edad_padre >= 2.0 and edad_padre < 17.0:  # Persona entre 35-44
                padre = escogepersonas(hombres, 35, 44, 0)
            elif edad_padre >= 17.0 and edad_padre < 43.8:  # Persona entre 45-54
                padre = escogepersonas(hombres, 45, 54, 0)
            elif edad_padre >= 43.8 and edad_padre < 64.5:  # Persona entre 55-64
                padre = escogepersonas(hombres, 55, 64, 0)
            elif edad_padre >= 64.5 and edad_padre <= 100.0:  # Persona de más de 65
                padre = escogepersonas(hombres, 65, 95, 0)
            if padre <= 38:  # Para que las madres solo puedan tener hijos a partir de los 15 años
                if genero_primer_hijo[0] == 0:
                    edad_primer_hijo = escogepersonas(hombres, 0, padre - 15, 0)
                elif genero_primer_hijo[0] == 1:
                    edad_primer_hijo = escogepersonas(mujeres, 0, padre - 15, 1)
            if padre > 38:
                if genero_primer_hijo[0] == 0:
                    edad_primer_hijo = escogepersonas(hombres, 0, 24, 0)
                elif genero_primer_hijo[0] == 1:
                    edad_primer_hijo = escogepersonas(mujeres, 0, 24, 1)
            personas.extend([id_personas, padre, 0, id_personas + 1, edad_primer_hijo, genero_primer_hijo[0]])
            personas = siguienteshijos(hombres, mujeres, edad_primer_hijo, 2, totalniños, totalniñas, id_personas + 2, personas)
            probtrabajo = numaleatorio()
            if probtrabajo >= 0 and probtrabajo < 1.0:
                trabajo = 0
            elif probtrabajo >= 1.0 and probtrabajo <= 100.0:
                trabajo = 1
            if personas[7] > 24 or personas[10] > 24:  # Prueba de que un hijo ya es mayor y ya no es monoparental
                tipofamilia = tipodefamilia(4, trabajo, 1, 0)
            else:
                tipofamilia = tipodefamilia(4, trabajo, 1, 1)
            lista_familias.append(familia(id_familias, personas, casasp, casasm, casasg, tipofamilia))
            id_personas += 4
            id_familias += 1

        elif tipo >= 3.2 and tipo <= 87.8 and totalhombresadultos + totalmujeresadultas > 1 and totalniños + totalniñas > 1:  # Pareja con dos hijos
            genero_hijo = sexadorhijos(totalniños, totalniñas, 1) # Da el genero de los hijos teniendo encuenta la disponibilidad
            if genero_hijo[0] == 0:
                edad_primer_hijo = escogepersonas(hombres, 0, 24, 0)
            elif genero_hijo[0] == 1:
                edad_primer_hijo = escogepersonas(mujeres, 0, 24, 1)
            edad_nacimiento = numaleatorio()  # Primero se saca estadisticamente a que edad tuvo la madre el primer hijo para luego sacar la edad de la madre
            if (edad_nacimiento >= 0 and edad_nacimiento < 1.8):  # La madre dio a luz cuando tenia entre 15-19
                edad_madre = random.randint(15, 19)
                personas = parejador(hombres, mujeres, edad_madre + edad_primer_hijo, personas)
            elif (edad_nacimiento >= 1.8 and edad_nacimiento < 9.3):  # La madre dio a luz cuando tenia entre 20-24
                edad_madre = random.randint(20, 24)
                personas = parejador(hombres, mujeres, edad_madre + edad_primer_hijo, personas)
            elif (edad_nacimiento >= 9.3 and edad_nacimiento < 26.7):  # La madre dio a luz cuando tenia entre 25-29
                edad_madre = random.randint(25, 29)
                personas = parejador(hombres, mujeres, edad_madre + edad_primer_hijo, personas)
            elif (edad_nacimiento >= 26.7 and edad_nacimiento < 59.3):  # La madre dio a luz cuando tenia entre 30-34
                edad_madre = random.randint(30, 34)
                personas = parejador(hombres, mujeres, edad_madre + edad_primer_hijo, personas)
            elif (edad_nacimiento >= 59.3 and edad_nacimiento < 89.6):  # La madre dio a luz cuando tenia entre 35-39
                edad_madre = random.randint(35, 39)
                personas = parejador(hombres, mujeres, edad_madre + edad_primer_hijo, personas)
            elif (edad_nacimiento >= 89.6 and edad_nacimiento < 99.1):  # La madre dio a luz cuando tenia entre 40-44
                edad_madre = random.randint(40, 44)
                personas = parejador(hombres, mujeres, edad_madre + edad_primer_hijo, personas)
            elif (edad_nacimiento >= 99.1 and edad_nacimiento <= 100.0):  # La madre dio a luz cuando tenia mas de 45
                edad_madre = random.randint(45, 49)
                personas = parejador(hombres, mujeres, edad_madre + edad_primer_hijo, personas)
            personas.extend([id_personas + 2, edad_primer_hijo, genero_hijo[0]])  # Sumamos 2 al id porque en el parejador se metieron los padres
            personas = siguienteshijos(hombres, mujeres, edad_primer_hijo, 1, totalniños, totalniñas, id_personas + 3, personas)
            probtrabajo = numaleatorio()
            if probtrabajo >= 0 and probtrabajo < 1.9:
                trabajo = 0
            elif probtrabajo >= 1.9 and probtrabajo <= 100.0:
                trabajo = 1
            tipofamilia = tipodefamilia(4, trabajo, 1, 0)
            lista_familias.append(familia(id_familias, personas, casasp, casasm, casasg, tipofamilia))
            id_personas += 4
            id_familias += 1

        # REVISAR NUMERO DE ADULTOS Y NIÑOS DISPONIBLES DISTINTAS FORMAS DE FAMILIAS
        '''elif tipo >= 87.8 and tipo < 95.8 and totalhombresadultos + totalmujeresadultas > 2 and totalniños + totalniñas > 0:  # Núcleo familiar con otras personas que no forman núcleo familiar (Abuelo)
            id_personas += 3
            id_familias += 1

        elif tipo >= 95.8 and tipo <= 96.7 and totalhombresadultos + totalmujeresadultas > 2:  # Personas que no forman ningún núcleo familiar entre sí
            id_personas += 3
            id_familias += 1

        elif tipo >= 96.7 and tipo <= 100.0 and totalhombresadultos + totalmujeresadultas > 2:  # Dos o más núcleos familiares
            id_personas += 3
            id_familias += 1'''


    elif tamfamilia >= 93.6 and tamfamilia < 97.5: # Familia de 5
        tipo = numaleatorio()
        if tipo >= 0 and tipo < 65.8 and totalhombresadultos + totalmujeresadultas > 1 and totalniños + totalniñas > 2:  # Pareja con tres hijos
            genero_hijo = sexadorhijos(totalniños, totalniñas, 1)
            if genero_hijo[0] == 0:
                edad_primer_hijo = escogepersonas(hombres, 0, 24, 0)
            elif genero_hijo[0] == 1:
                edad_primer_hijo = escogepersonas(mujeres, 0, 24, 1)
            edad_nacimiento = numaleatorio()  # Primero se saca estadisticamente a que edad tuvo la madre el primer hijo para luego sacar la edad de la madre
            if (edad_nacimiento >= 0 and edad_nacimiento < 1.8):  # La madre dio a luz cuando tenia entre 15-19
                edad_madre = random.randint(15, 19)
                personas = parejador(hombres, mujeres, edad_madre + edad_primer_hijo, personas)
            elif (edad_nacimiento >= 1.8 and edad_nacimiento < 9.3):  # La madre dio a luz cuando tenia entre 20-24
                edad_madre = random.randint(20, 24)
                personas = parejador(hombres, mujeres, edad_madre + edad_primer_hijo, personas)
            elif (edad_nacimiento >= 9.3 and edad_nacimiento < 26.7):  # La madre dio a luz cuando tenia entre 25-29
                edad_madre = random.randint(25, 29)
                personas = parejador(hombres, mujeres, edad_madre + edad_primer_hijo, personas)
            elif (edad_nacimiento >= 26.7 and edad_nacimiento < 59.3):  # La madre dio a luz cuando tenia entre 30-34
                edad_madre = random.randint(30, 34)
                personas = parejador(hombres, mujeres, edad_madre + edad_primer_hijo, personas)
            elif (edad_nacimiento >= 59.3 and edad_nacimiento < 89.6):  # La madre dio a luz cuando tenia entre 35-39
                edad_madre = random.randint(35, 39)
                personas = parejador(hombres, mujeres, edad_madre + edad_primer_hijo, personas)
            elif (edad_nacimiento >= 89.6 and edad_nacimiento < 99.1):  # La madre dio a luz cuando tenia entre 40-44
                edad_madre = random.randint(40, 44)
                personas = parejador(hombres, mujeres, edad_madre + edad_primer_hijo, personas)
            elif (edad_nacimiento >= 99.1 and edad_nacimiento <= 100.0):  # La madre dio a luz cuando tenia mas de 45
                edad_madre = random.randint(45, 49)
                personas = parejador(hombres, mujeres, edad_madre + edad_primer_hijo, personas)
            personas.extend([id_personas + 2, edad_primer_hijo, genero_hijo[0]])  # Sumamos 2 al id porque en el parejador se metieron los padres
            personas = siguienteshijos(hombres, mujeres, edad_primer_hijo, 2, totalniños, totalniñas, id_personas + 3, personas)
            probtrabajo = numaleatorio()
            if probtrabajo >= 0 and probtrabajo < 2.7:
                trabajo = 0
            elif probtrabajo >= 2.7 and probtrabajo <= 100.0:
                trabajo = 1
            tipofamilia = tipodefamilia(5, trabajo, 1, 0)
            lista_familias.append(familia(id_familias, personas, casasp, casasm, casasg, tipofamilia))
            id_personas += 5
            id_familias += 1

        # REVISAR NUMERO DE ADULTOS Y NIÑOS DISPONIBLES DISTINTAS FORMAS DE FAMILIAS
        '''elif tipo >= 65.8 and tipo < 85.8 and totalhombresadultos + totalmujeresadultas > 2 and totalniños + totalniñas > 0:  # Núcleo familiar con otras personas que no forman núcleo familiar (Abuelo)
            id_personas += 3
            id_familias += 1


        elif tipo >= 85.8 and tipo <= 100.0 and totalhombresadultos + totalmujeresadultas > 2:  # Dos o más núcleos familiares
            id_personas += 3
            id_familias += 1'''


    elif tamfamilia >= 97.5 and tamfamilia <= 99.0: # Familia de 6
        tipo = numaleatorio()
        # REVISAR NUMERO DE ADULTOS Y NIÑOS DISPONIBLES DISTINTAS FORMAS DE FAMILIAS
        '''if tipo >= 0 and tipo < 27.4 and totalhombresadultos + totalmujeresadultas > 2 and totalniños + totalniñas > 0:  # Pareja con cuatro hijos
            id_personas += 3
            id_familias += 1

        elif tipo >= 27.4 and tipo <= 58.8 and totalhombresadultos + totalmujeresadultas > 2:  # Núcleo familiar con otras personas que no forman núcleo familiar (Abuelo)
            id_personas += 3
            id_familias += 1

        elif tipo >= 58.8 and tipo <= 100.0 and totalhombresadultos + totalmujeresadultas > 2:  # Dos o más núcleos familiares
            id_personas += 3
            id_familias += 1'''

    elif tamfamilia >= 99.0 and tamfamilia <= 100.0: # Familia de 7 o más
        tipo = numaleatorio()
        # REVISAR NUMERO DE ADULTOS Y NIÑOS DISPONIBLES DISTINTAS FORMAS DE FAMILIAS
        '''if tipo >= 0 and tipo < 9.2 and totalhombresadultos + totalmujeresadultas > 2 and totalniños + totalniñas > 0:  # Pareja con cinco hijos
            id_personas += 3
            id_familias += 1

        elif tipo >= 9.2 and tipo <= 25.1 and totalhombresadultos + totalmujeresadultas > 2:  # Núcleo familiar con otras personas que no forman núcleo familiar (Abuelo)
            id_personas += 3
            id_familias += 1

        elif tipo >= 25.1 and tipo <= 100.0 and totalhombresadultos + totalmujeresadultas > 2:  # Dos o más núcleos familiares
            id_personas += 3
            id_familias += 1'''
    else:
        sys.exit('Error al generar el numero de personas por familia')

for i in range(7):
    casasp, casasm, casasg = catastro()
    copiacasasp = copy.deepcopy(casasp)
    copiacasasm = copy.deepcopy(casasm)
    copiacasasg = copy.deepcopy(casasg)
    listaHombres, listaMujeres, totalniñas, totalniños, totalmujeresadultas, totalhombresadultos = censo()

    while totalmujeresadultas + totalhombresadultos > 0:
        if len(casasp) == 0 and len(casasm) == 0 and len(casasg) == 0:
            casasp = copy.deepcopy(copiacasasp)
            casasm = copy.deepcopy(copiacasasm)
            casasg = copy.deepcopy(copiacasasg)
        print("HAY " + str(totalmujeresadultas) + " mujeres, " + str(totalhombresadultos) + " hombres, " + str(totalniñas) + " niñas y " + str(totalniños) + " niños por colocar")
        familiador (listaHombres, listaMujeres)
        print("QUEDAN " + str(totalmujeresadultas) + " mujeres, " + str(totalhombresadultos) + " hombres, " + str(totalniñas) + " niñas y " + str(totalniños) + " niños por colocar")
    print(lista_familias[0].casa)
planear(lista_familias)
