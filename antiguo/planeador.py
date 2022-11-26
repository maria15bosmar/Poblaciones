import math
import random
import copy
from facilities import raster


def planear(lista_familias):
    mapa = raster()
    famtipo1, famtipo2, famtipo3, famtipo4 ,famtipo5, famtipo6, famtipo7, famtipo8 = familiasreales()
    copiafamtipo1, copiafamtipo2, copiafamtipo3, copiafamtipo4 = copy.deepcopy(famtipo1), copy.deepcopy(famtipo2), copy.deepcopy(famtipo3), copy.deepcopy(famtipo4)
    copiafamtipo5, copiafamtipo6, copiafamtipo7, copiafamtipo8 = copy.deepcopy(famtipo5), copy.deepcopy(famtipo6), copy.deepcopy(famtipo7), copy.deepcopy(famtipo8)
    fichero_salida = open('population.xml', 'w')
    fichero_salida.write('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE plans SYSTEM "http://www.matsim.org/files/dtd/plans_v4.dtd">\n\n<population>\n\n')
    for i in range(len(lista_familias)):
        tipo = lista_familias[i].tipofamilia
        if tipo == 1:       # Unipersonal    EnelParo    Sinniños
            vacio = traspaso(famtipo1,lista_familias[i], fichero_salida, mapa, 1)
        elif tipo == 2:     # Unipersonal    Trabajando  Sinniños
            vacio = traspaso(famtipo2,lista_familias[i], fichero_salida, mapa, 2)
        elif tipo == 3:     # Multipersonal  EnelParo    Sinniños
            vacio = traspaso(famtipo3,lista_familias[i], fichero_salida, mapa, 3)
        elif tipo == 4:     # Multipersonal  Trabajando  Sinniños
            vacio = traspaso(famtipo4,lista_familias[i], fichero_salida, mapa, 4)
        elif tipo == 5:     # Multipersonal  EnelParo    Conniños   Monoparental
            vacio = traspaso(famtipo5,lista_familias[i], fichero_salida, mapa, 5)
        elif tipo == 6:     # Multipersonal  EnelParo    Conniños   Nomonoparental
            vacio = traspaso(famtipo6,lista_familias[i], fichero_salida, mapa, 6)
        elif tipo == 7:     # Multipersonal  Trabajando  Conniños   Monoparental
            vacio = traspaso(famtipo7,lista_familias[i], fichero_salida, mapa, 7)
        elif tipo == 8:     # Multipersonal  Trabajando  Conniños   Nomonoparental
            vacio = traspaso(famtipo8,lista_familias[i], fichero_salida, mapa, 8)
        print("Se han completado " + str(i) + " familias")

        if vacio == -1 or vacio == -3:
            if tipo == 1:  # En caso de terminarse los familias reales del consorcio se vuelven a utilizar con la copia original
                if len(famtipo1) >= len(copiafamtipo1)/2:
                    famtipo1 = copy.deepcopy(copiafamtipo1)
                else:
                    famtipo1 = famtipo1 + copy.deepcopy(copiafamtipo1)
            elif tipo == 2:
                if len(famtipo2) >= len(copiafamtipo2) / 2:
                    famtipo2 = copy.deepcopy(copiafamtipo2)
                else:
                    famtipo2 = famtipo2 + copy.deepcopy(copiafamtipo2)
            elif tipo == 3:
                if len(famtipo3) >= len(copiafamtipo3) / 2:
                    famtipo3 = copy.deepcopy(copiafamtipo3)
                else:
                    famtipo3 = famtipo3 + copy.deepcopy(copiafamtipo3)
            elif tipo == 4:
                if len(famtipo4) >= len(copiafamtipo4) / 2:
                    famtipo4 = copy.deepcopy(copiafamtipo4)
                else:
                    famtipo4 = famtipo4 + copy.deepcopy(copiafamtipo4)
            elif tipo == 5:
                if len(famtipo5) >= len(copiafamtipo5) / 2:
                    famtipo5 = copy.deepcopy(copiafamtipo5)
                else:
                    famtipo5 = famtipo5 + copy.deepcopy(copiafamtipo5)
            elif tipo == 6:
                if len(famtipo6) >= len(copiafamtipo6) / 2:
                    famtipo6 = copy.deepcopy(copiafamtipo6)
                else:
                    famtipo6 = famtipo6 + copy.deepcopy(copiafamtipo6)
            elif tipo == 7:
                if len(famtipo7) >= len(copiafamtipo7) / 2:
                    famtipo7 = copy.deepcopy(copiafamtipo7)
                else:
                    famtipo7 = famtipo7 + copy.deepcopy(copiafamtipo7)
            elif tipo == 8:
                if len(famtipo8) >= len(copiafamtipo8) / 2:
                    famtipo8 = copy.deepcopy(copiafamtipo8)
                else:
                    famtipo8 = famtipo8 + copy.deepcopy(copiafamtipo8)
    fichero_salida.write('</population>')
    fichero_salida.close()  # Cerramos el fichero de popablación

def familiasreales(): #Este metodo lee los archivos con las familias reales y las guarda en las 6 listas dependiendo del tipo
    famtipo1, famtipo2, famtipo3, famtipo4, famtipo5, famtipo6, famtipo7, famtipo8 = [], [], [], [], [], [], [], []
    tipologia = 1   #tipo de familia
    aux_id_hog = -1
    aux_id_per = -1
    aux_id_via = -1
    for i in range(8):
        dir = 'Consorcio\ptipologia_.csv'
        index = dir.find('.')
        dir = dir[:index] + str(tipologia) + dir[index:]
        fichero = open(dir, 'r+')   # se lee el fichero con las personas reales
        texto = fichero.readlines()
        numero_lineas = len(texto)
        familia, persona, plan = [], [], []
        for j in range(numero_lineas): # Para cada linea del archivo leido se van guardando en las variables los datos
            id_hog, id_per, id_via, sexo, trabajo, carnet, hora_ini, hora_fin, mot_origen, mot_destino, vehiculo, distancia, edad, num_veh, num_miembros_fam, num_adultos, pueblo_dest, pueblo_orig = texto[j].split(';')
            id_hog = id_hog.replace("ï»¿", "")      #al leer del csv no se porque me añade estos caracteres
            pueblo_orig = pueblo_orig.replace("\n", "")
            if len(persona) == 0:                   # Plan inicial
                plan = [id_hog, id_per, id_via, sexo, trabajo, carnet, hora_ini, hora_fin, mot_origen, mot_destino, vehiculo, distancia, edad, num_veh, num_miembros_fam, num_adultos, pueblo_dest, pueblo_orig]
                persona.append(plan)
            elif id_hog == aux_id_hog and id_per == aux_id_per and int(id_via) == int(aux_id_via) + 1:  #Plan posterior de la misma persona de la familia
                plan = [id_hog, id_per, id_via, sexo, trabajo, carnet, hora_ini, hora_fin, mot_origen, mot_destino, vehiculo, distancia, edad, num_veh, num_miembros_fam, num_adultos, pueblo_dest, pueblo_orig]
                persona.append(plan)
            elif id_hog == aux_id_hog and id_per != aux_id_per: # Nueva persona de la familia
                familia.append(persona)
                plan = [id_hog, id_per, id_via, sexo, trabajo, carnet, hora_ini, hora_fin, mot_origen, mot_destino, vehiculo, distancia, edad, num_veh, num_miembros_fam, num_adultos, pueblo_dest, pueblo_orig]
                persona = []
                persona.append(plan)
            elif id_hog != aux_id_hog:  # Nuevo hogar, guardamos por lo tanto el anterior hogar segun su tipo
                familia.append(persona)
                if tipologia == 1:
                    famtipo1.append(familia)
                elif tipologia == 2:
                    famtipo2.append(familia)
                elif tipologia == 3:
                    famtipo3.append(familia)
                elif tipologia == 4:
                    famtipo4.append(familia)
                elif tipologia == 5:
                    famtipo5.append(familia)
                elif tipologia == 6:
                    famtipo6.append(familia)
                elif tipologia == 7:
                    famtipo7.append(familia)
                elif tipologia == 8:
                    famtipo8.append(familia)
                familia = []    # Se reinician las variables
                persona = []
                plan = [id_hog, id_per, id_via, sexo, trabajo, carnet, hora_ini, hora_fin, mot_origen, mot_destino, vehiculo, distancia, edad, num_veh, num_miembros_fam, num_adultos, pueblo_dest, pueblo_orig]
                persona.append(plan)
            aux_id_hog = id_hog
            aux_id_per = id_per
            aux_id_via = id_via
        tipologia += 1  # Ya se han leido todas las casas de un tipo se pasa a la siguiente tipologia
        fichero.close()
    return famtipo1, famtipo2, famtipo3, famtipo4, famtipo5, famtipo6, famtipo7, famtipo8


def masceros(numero):   # Añade ceros a las horas para que tengan bien el formato
    if (len(str(numero)) == 1):
        numero = "000" + str(numero)
    elif (len(str(numero)) == 2):
        numero = "00" + str(numero)
    elif (len(str(numero)) == 3):
        numero = "0" + str(numero)
    return numero


def trav_time(hora_ini, hora_fin):
    h1 = str(hora_ini)[:2]
    m1 = str(hora_ini)[2:]
    h2 = str(hora_fin)[:2]
    m2 = str(hora_fin)[2:]
    min1 = int(m1) + int(h1) * 60
    min2 = int(m2) + int(h2) * 60
    duracion = min2 - min1
    if duracion >= 60:
        horas = duracion // 60
        minutos = str(duracion - 60 * horas)
        if len(str(minutos)) == 1:
            minutos = "0" + str(minutos)
        duracion = str(horas) + str(minutos)
    duracion = masceros(duracion)
    duracion = duracion[:2] + ":" + duracion[2:]
    return duracion


def modo(consorcio):
    if consorcio == 1 or consorcio == 2 or consorcio == 3 or consorcio == 4 or consorcio == 5 or consorcio == 6 or consorcio == 7 or consorcio == 8 or consorcio == 9:
        modestr = "pt"
    elif consorcio == 10:
        modestr = "taxi"
    elif consorcio == 11 or consorcio == 12 or consorcio == 13 or consorcio == 14 or consorcio == 15 or consorcio == 16 or consorcio == 17 or consorcio == 18 or consorcio == 19 or consorcio == 23: #or consorcio == -1:
        modestr = "car"
    elif consorcio == 20 or consorcio == 21 or consorcio == 22:
        modestr = "bicicle"
    elif consorcio == 24:
        modestr = "walk"
    return modestr


def lugar(consorcio):
    if consorcio == 1:
        origenstr = "home"
    elif consorcio == 2 or consorcio == 3: #or consorcio == -1:
        origenstr = "work"
    elif consorcio == 4:
        origenstr = "education"
    elif consorcio == 5:
        origenstr = "shopping"
    elif consorcio == 6:
        origenstr = "medical"
    elif consorcio == 7:
        origenstr = "work"         ## Cambiado por work por no añadir los coches conjuntos Falta por implementar carry
    elif consorcio == 8 or consorcio == 9 or consorcio == 10 or consorcio == 11 or consorcio == 12:
        origenstr = "leisure"
    return origenstr


def viajefuera(pueblo_dest):
    # Alcalá de Henares, Pinto, Torrejon de Ardoz, Valdemoro
    if pueblo_dest == 5 or pueblo_dest == 113 or pueblo_dest == 148 or pueblo_dest == 161:
        x_nueva = 438447
        y_nueva = 4464616
    # Alcobendas, Madrid
    elif pueblo_dest == 6 or pueblo_dest == 79:
        x_nueva = 437647
        y_nueva = 4468216
    # Alcorcon
    elif pueblo_dest == 7:
        x_nueva = 432447
        y_nueva = 4465716
    # Boadilla del Monte, Colmenar Viejo, Majadahonda, Pozuelo de Alarcon, Las Rozas
    elif pueblo_dest == 22 or pueblo_dest == 45 or pueblo_dest == 80 or pueblo_dest == 115 or pueblo_dest == 127:
        x_nueva = 432847
        y_nueva = 4468216
    # Fuenlabrada, Humanes
    elif pueblo_dest == 58 or pueblo_dest == 73:
        x_nueva = 433600
        y_nueva = 4462216
    # Getafe, Parla
    elif pueblo_dest == 65 or pueblo_dest == 106:
        x_nueva = 436847
        y_nueva = 4463016
    # Mostoles
    elif pueblo_dest == 92:
        x_nueva = 432447
        y_nueva = 4463016
    return x_nueva, y_nueva

def tipodeviaje(destinostr, cuadrante, mapa):
    if destinostr == "work":
        puntos = mapa[cuadrante].work
    elif destinostr == "education":
        puntos = mapa[cuadrante].education
    elif destinostr == "shopping":
        puntos = mapa[cuadrante].shopping
    elif destinostr == "medical":
        puntos = mapa[cuadrante].medical
    elif destinostr == "carry":     ## Falta por implementar carry
        puntos = mapa[cuadrante].work
    elif destinostr == "leisure":
        puntos = mapa[cuadrante].leisure
    return puntos

def pesoscuadrante(listapuntos, destinostr, mapa): # Toma todos los puntos del circulo y saca de los cuadrantes los valores del tipo buscado
    x_inicial = 432447
    x_final = 438447
    y_inicial = 4468216
    y_final = 4462216
    cuadrante_anterior, sumapuntuacion = -1, 0
    listacuadrantes,  listacuadrantes_aux = [], []
    for k in range(len(listapuntos)):
        x_actual = listapuntos[k][0]
        y_actual = listapuntos[k][1]
        if x_inicial <= x_actual < x_final and y_inicial > y_actual >= y_final:
            dist_afinal_X = (x_actual - x_inicial) // 400  # Se calcula el cuadrante en X
            dist_afinal_Y = (y_inicial - y_actual) // 400  # Se calcula el cuadrante en Y
            if dist_afinal_X == 15: # En el caso de que la x sea igual a x_final fallaria por ser division entera
                dist_afinal_X = 14
            if dist_afinal_Y == 15: # En el caso de que la y sea igual a y_final fallaria por ser division entera
                dist_afinal_Y = 14
            cuadrante = dist_afinal_X + dist_afinal_Y * 15  # Se calcula el cuadrante donde se situa el edificio
            if cuadrante != cuadrante_anterior:  # En caso de no haber revisado ya ese cuadrante se inserta
                edificios = tipodeviaje(destinostr, cuadrante, mapa)
                if edificios > 0:
                    sumapuntuacion += edificios
                    listacuadrantes.append([cuadrante, sumapuntuacion, x_actual, y_actual])  # Se guarda la suma de puntuaciones para luego usar el random
                listacuadrantes_aux.append([cuadrante, sumapuntuacion, x_actual,y_actual])
                cuadrante_anterior = cuadrante
    if sumapuntuacion == 0 and len(listacuadrantes_aux) > 0:    # Si no hay puntuacion para el tipo de viaje se escoje aleatoriamente un cuadrante
        aleatorio = random.randint(0, len(listacuadrantes_aux)-1)
        x_nueva = listacuadrantes_aux[aleatorio][2]
        y_nueva = listacuadrantes_aux[aleatorio][3]
    else:
        puntero = random.randint(0, sumapuntuacion)
        for l in range(len(listacuadrantes)):
            if listacuadrantes[l][1] >= puntero:
                x_nueva = listacuadrantes[l][2]
                y_nueva = listacuadrantes[l][3]
                break
    return x_nueva, y_nueva


def coordenadas(x_anterior, y_anterior, distancia, destinostr, pueblo_dest, pueblo_orig, mapa):
    x_nueva, y_nueva = 1, 1
    if pueblo_dest != 74:  # Si la persona se desplaza fuera del municipio se dan las cordenadas de la carretera por donde sale del mapa
        x_nueva, y_nueva = viajefuera(pueblo_dest)
    else:                                       # En caso de quedarse en el municipio se ven los lugares posibles a los que ir
        grados_girados = 0
        listapuntos = []
        if pueblo_dest == pueblo_orig:
            distancia = distancia.replace(",", ".")
            radio = round(float(distancia) * 1000)
            if radio <= 500:
                grados = 20
            elif 500 < radio <= 1000:
                grados = 10
            elif 1000 < radio <= 3000:
                grados = 5
            elif 3000 < radio <= 8400:
                grados = 2.5
            elif radio > 8400:
                radio = 4000
                grados = 2.5
        else:
            radio = 4000
            grados = 2.5
        if x_anterior + radio > 438447 and x_anterior - radio < 432447 and y_anterior + radio > 4468216 and x_anterior - radio < 4462216: #Si se sale por todos los lados del mapa se reduce el radio
            radio = round(radio/2)
        x_nueva = x_anterior + radio    #Primer punto a comprobar [x+radio, y]
        listapuntos.append([x_nueva, y_anterior])
        grados_girados += grados
        while grados_girados <= 90:  # Se hayan los puntos del 1 cuadrante
            alpha = grados_girados * math.pi / 180  # Pasar grados a radianes
            cos_x_nueva = math.cos(alpha)
            sin_y_nueva = math.sin(alpha)
            x_nueva = round(x_anterior + radio * cos_x_nueva)
            y_nueva = round(y_anterior + radio * sin_y_nueva)
            listapuntos.append([x_nueva, y_nueva])
            grados_girados += grados
        puntos_cuadrante_1 = len(listapuntos)
        if grados_girados - grados == 90:  # En caso de tener un punto en 90 grados no hay que aplicarle simetria a ese punto
            puntos_cuadrante_1 -= 1 # Se resta 1 porque en caso de tener un pto en 90 grados, para i = 0 se cogeria este punto al ser el ultimo de la lista y asi se pilla el anterior
        for i in range(puntos_cuadrante_1):  # Se hayan los puntos del 2 cuadrante
            x_nueva = listapuntos[puntos_cuadrante_1 - 1 - i][0]  # Se resta 1 por ser una lista que si no outofindex
            y_nueva = listapuntos[puntos_cuadrante_1 - 1 - i][1]
            dist_en_x = x_nueva - x_anterior
            listapuntos.append([x_nueva - 2 * dist_en_x, y_nueva])  # Simetria del punto respecto al eje de ordenadas
        puntos_cuadrante_1y2 = len(listapuntos) - 2  # A los puntos en x - radio y x + radio no se les aplica simetria
        for j in range(puntos_cuadrante_1y2):  # Se hayan los puntos del 3 y 4 cuadrante
            x_nueva = listapuntos[puntos_cuadrante_1y2 - j][0]
            y_nueva = listapuntos[puntos_cuadrante_1y2 - j][1]
            dist_en_y = y_nueva - y_anterior
            listapuntos.append([x_nueva, y_nueva - 2 * dist_en_y])  # Simetria del punto respecto al eje de abcisas
        x_nueva, y_nueva = pesoscuadrante(listapuntos, destinostr, mapa)
    return x_nueva, y_nueva;

def ordenar(fam_consorcio, fam_sintetica, num_hijos_sinte):
    persona, consorcio, consorcio_copia = [], [], []
    num_per_consorcio = int(fam_consorcio[0][0][0][14])
    num_hijos_consorcio = int(fam_consorcio[0][0][0][14]) - int(fam_consorcio[0][0][0][15])
    direncia_hijos = num_hijos_consorcio - num_hijos_sinte
    if direncia_hijos < 0:   # hay un hijo menos en el consorcio por lo tanto se duplica uno de ellos:
        boolean = False
        aux = num_per_consorcio - 1
        while boolean == False:
            if int(fam_consorcio[0][aux][0][12]) <= 24:
                copia_auxiliar = copy.deepcopy(fam_consorcio[0][aux])
                fam_consorcio[0].append(copia_auxiliar)
                boolean = True
                num_per_consorcio += 1
            aux -= 1
    elif direncia_hijos > 0: # hay un hijo mas por lo tanto se quita uno
        for m in range(direncia_hijos):
            boolean = False
            aux = num_per_consorcio - 1
            while boolean == False:
                if int(fam_consorcio[0][aux][0][12]) <= 24:
                    del fam_consorcio[0][aux]
                    boolean = True
                    num_per_consorcio -= 1
                aux -= 1
    for k in range(num_per_consorcio):
        persona = [int(fam_consorcio[0][k][0][12]), int(fam_consorcio[0][k][0][3])-1, int(fam_consorcio[0][k][0][1])] # Edad, genero e id de la persona le resto uno al genero para que coincida con 0 h 1 m
        consorcio.append(persona)
    consorcio_copia = copy.deepcopy(consorcio)
    for i in range(num_per_consorcio):  #bubble sort consorcio ordenando por edad
        for j in range(0, num_per_consorcio - i - 1):
            if consorcio[j][0] < consorcio[j + 1][0]:
                consorcio[j], consorcio[j + 1] = consorcio[j + 1], consorcio[j]
    if len(consorcio) - num_hijos_sinte == 2:    # buscamos la pareja, los que tengan la edad mas cercana era num_hijos_sinte >= 2 pero se elimino
        pareja_cons = [0,1]
        pareja_sinte = [0,1]
        """if len(consorcio) - num_hijos_sinte > 2: # Como la asignacion de planes se sigue haciendo en orden no funciona si [58,57,26,3] y [75,43,39,11] los planes de la pareja se asignan a 75 y 43
            diferencia_cons = 999
            diferencia_sinte = 999
            for z in range(len(consorcio) - num_hijos_sinte - 1):
                if consorcio[z][0] - consorcio[z+1][0] < diferencia_cons: # Buscando la pareja en el consorcio
                    diferencia_cons = consorcio[z][0] - consorcio[z+1][0]
                    pareja_cons = [z , z+1]
                if fam_sintetica.personas[1 + 3*z] - fam_sintetica.personas[4 + 3*z] < diferencia_sinte: # Buscando la pareja en sintetico
                    diferencia_sinte = fam_sintetica.personas[1 + 3*z] - fam_sintetica.personas[4 + 3*z]
                    pareja_sinte = [z , z+1]"""
        if consorcio[pareja_cons[0]][1] != fam_sintetica.personas[2 + 3*pareja_sinte[0]] and consorcio[pareja_cons[1]][1] != fam_sintetica.personas[2 + 3*pareja_sinte[1]]:   # La pareja del consorcio h y m estan ordenadas distintamente que la sintetica entoces se intercambian
            consorcio[pareja_cons[0]], consorcio[pareja_cons[1]] = consorcio[pareja_cons[1]], consorcio[pareja_cons[0]]
    for l in range(num_per_consorcio):
        if consorcio_copia[l][2] != consorcio[l][2]:    #Si no coinciden estan desordenados
            for x in range(l+1, num_per_consorcio):      # buscamos entonces la posicion en la que estaba la persona originalmente
                if consorcio_copia[x][2] == consorcio[l][2]:  # Una vez encontrada la posicion en la copia modificamos esta y la lista principal
                    fam_consorcio[0][l], fam_consorcio[0][x] = fam_consorcio[0][x], fam_consorcio[0][l]
                    consorcio_copia[l], consorcio_copia[x] = consorcio_copia[x], consorcio_copia[l]
                    break

def traspaso(fam_consorcio, fam_sintetica, fichero_salida, mapa, tipologia):
    terminado = False
    num_personas_sinte = int(len(fam_sintetica.personas) / 3)
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
                if fam_sintetica.personas[1 + 3 * i] > 24:
                    num_adultos_sinte += 1
                    hogar_joven += 1
                if fam_sintetica.personas[1 + 3 * i] <= 24:
                    num_hijos_sinte += 1
            """if hogar_joven == 0 and (tipologia == 3 or tipologia == 4): # para que se acepten hogares jovenes
                for i in range(num_personas_sinte):
                    if fam_sintetica.personas[1 + 3 * i] > 17:
                        num_adultos_sinte += 1
                        num_hijos_sinte -= 1
                    else:
                        familiapta = False
                        break"""
            if hogar_joven == 1 and (tipologia == 6 or tipologia == 8): # Parejas jovenes uno de los dos de entre 18 y 24 con hijos se comprueba que este bien para aceptarla o no
                num_joven, joven = 0, 0
                for i in range(num_personas_sinte):
                    if 17 < fam_sintetica.personas[1 + 3 * i] <= 24:  # Se comprueba si hay un solo un progenitor de entre 18 y 24
                        num_joven += 1
                        joven = i
                if num_joven == 1:
                    pareja = 0
                    for j in range(num_personas_sinte):
                        if joven != j and fam_sintetica.personas[1 + 3 * joven]-fam_sintetica.personas[1 + 3 * j] <= 15: # Busca a alguien que no pueda ser su hijo para luego comprobar que sea su pareja
                            if fam_sintetica.personas[1 + 3 * j] >= 18 and fam_sintetica.personas[1 + 3 * joven]-fam_sintetica.personas[1 + 3 * j] > -15: # Se comprueba que pueda ser su pareja si tiene mas de 18 y se llevan menos de 15
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
            if hogar_joven == 0 and (tipologia == 6 or tipologia == 8):  # Parejas jovenes los dos de entre 18 y 24 con hijos se comprueba que este bien para aceptarla o no
                pareja = []
                for k in range(num_personas_sinte):
                    if 17 < fam_sintetica.personas[1 + 3 * k] <= 24:  # Se comprueba si hay dos progenitores de entre 18 y 24
                        pareja.append(k)
                if len(pareja) == 2: # Si los hay se comprueba que el resto de la familia puedan ser sus hijos es decir los tuvierron como min a los 15
                    posible = True
                    for l in range(num_personas_sinte):
                        if l != pareja[0] and l != pareja[1]:
                            if fam_sintetica.personas[1 + 3 * pareja[0]] - fam_sintetica.personas[1 + 3 * l] < 15 or fam_sintetica.personas[1 + 3 * pareja[1]] - fam_sintetica.personas[1 + 3 * l] < 15:
                                posible = False # Se ha comprobado que uno de los hijos por edad no puede ser hijo de uno de los progenitores luego ya no es una familia valida
                    if posible == True:
                        num_adultos_sinte += 2
                        num_hijos_sinte -= 2
                    else:
                        familiapta = False
                else:
                    familiapta = False
        if familiapta == True:
            while match == False:
                num_adultos_consorcio = int(fam_consorcio[0][0][0][15])
                num_hijos_consorcio = int(fam_consorcio[0][0][0][14]) - num_adultos_consorcio
                if num_adultos_sinte == num_adultos_consorcio and num_hijos_sinte - num_hijos_consorcio <= 1:  # Si coinciden el numero de adulto y como mucho hay un niño sinte mas se asignan los planes
                    match = True
                    if tipologia >= 5:  # tipologias 5 6 7 y 8 que tienen niños
                        for x in range(num_personas_sinte):  # bubble sort familias sinteticas ordenando por edad para que no haya problemas con los niños
                            for y in range(0, num_personas_sinte - x - 1):
                                if fam_sintetica.personas[1 + 3 * y] < fam_sintetica.personas[1 + 3 * (y + 1)]:
                                    fam_sintetica.personas[0 + 3 * y], fam_sintetica.personas[0 + 3 * (y + 1)] = fam_sintetica.personas[0 + 3 * (y + 1)], fam_sintetica.personas[0 + 3 * y]  # cambia id
                                    fam_sintetica.personas[1 + 3 * y], fam_sintetica.personas[1 + 3 * (y + 1)] = fam_sintetica.personas[1 + 3 * (y + 1)], fam_sintetica.personas[1 + 3 * y]  # cambia edad
                                    fam_sintetica.personas[2 + 3 * y], fam_sintetica.personas[2 + 3 * (y + 1)] = fam_sintetica.personas[2 + 3 * (y + 1)], fam_sintetica.personas[2 + 3 * y]  # cambia genero
                else:   # Si no coincide se quita la familia del consorcio de la lista y se pone atras
                    fam_consorcio.append(fam_consorcio.pop(0))
                    parabucle += 1
                    if parabucle == len(fam_consorcio):
                        return -1   ## No quedan familias que se ajusten al tipo que ha salido
        else:
            return -2   ## La familia sintetica no es apta
        ordenar(fam_consorcio, fam_sintetica, num_hijos_sinte)
    for j in range(num_personas_sinte):
        if int(fam_consorcio[0][0][0][2]) == -1:    # Caso de que la persona del consorcio no tenga planes
            fam_consorcio[0].pop(0)  # Se borra a la persona que no tenia planes
            if len(fam_consorcio[0]) == 0:  # Si no quedan mas personas en la familia se borra la familia
                fam_consorcio.pop(0)
        else:                                       # Caso de que la persona del consorcio tenga planes
            genero = fam_sintetica.personas[2 + 3 * j]
            carnet = fam_consorcio[0][0][0][5]
            '''try:     # Fallo en los datos donde una persona no tiene un primer plan
                carnet = fam_consorcio[0][0][0][5]
            except:
                print(o)'''
            if genero == 0:
                generostr = "m"
            elif genero == 1:
                generostr = "f"
            if carnet == 1:
                carnetstr = "no"
                cochestr = "never"
            elif carnet != 1:
                carnetstr = "yes"
                cochestr = "always"
            if tipologia == 1 or tipologia == 3 or tipologia == 5 or tipologia == 6:
                trabajostr = "no"
            elif tipologia == 2 or tipologia == 4 or tipologia == 7 or tipologia == 8:
                trabajostr = "yes"
            fichero_salida.write('\t\t<person id = "' + str(fam_sintetica.personas[0 + 3 * j]) + '" sex = "' + generostr + '" age = "' + str(fam_sintetica.personas[1 + 3 * j]) + '" license = "' + carnetstr + '" car_avail = "' + cochestr + '" employed = "' + trabajostr + '">\n')
            fichero_salida.write('\t\t\t<plan selected = "yes">\n')
            while terminado == False:
            # plan = [id_hog, id_per, id_via, sexo, trabajo, carnet, hora_ini, hora_fin, mot_origen, mot_destino, vehiculo, distancia, edad, num_veh, num_miembros_fam, num_adultos, pueblo_dest, pueblo_orig]
                hora_ini = fam_consorcio[0][0][0][6]
                hora_fin = fam_consorcio[0][0][0][7]
                hora_ini = masceros(hora_ini)
                hora_fin = masceros(hora_fin)
                duracion = trav_time(hora_ini, hora_fin)
                hora_ini = hora_ini[:2] + ":" + hora_ini[2:]
                hora_fin = hora_fin[:2] + ":" + hora_fin[2:]
                modestr = modo(int(fam_consorcio[0][0][0][10]))
                origenstr = lugar(int(fam_consorcio[0][0][0][8]))
                destinostr = lugar(int(fam_consorcio[0][0][0][9]))
                id_viaje = int(fam_consorcio[0][0][0][2]) - 1
                if id_viaje == 0:   # En caso de que sea el primer viaje se pone la estancia en casa hasta la hora de salir
                    fichero_salida.write('\t\t\t\t<act type = "' + origenstr + '" x = "' + str(fam_sintetica.casa[0]) + '" y = "' + str(fam_sintetica.casa[1]) + '" start_time = "00:00" dur = "' + hora_ini + '" end_time = "' + hora_ini + '"/>\n')
                    x_anterior = fam_sintetica.casa[0]
                    y_anterior = fam_sintetica.casa[1]
                if destinostr == "home":  #Si va a casa las nuevas coordenadas son las de casa en otro caso se buscan
                    x_nueva = str(fam_sintetica.casa[0])
                    y_nueva = str(fam_sintetica.casa[1])
                else:                       #En caso contrario se buscan las nuevas coordenadas
                    x_nueva, y_nueva = coordenadas(round(float(x_anterior)), round(float(y_anterior)),fam_consorcio[0][0][0][11], destinostr, int(fam_consorcio[0][0][0][16]), int(fam_consorcio[0][0][0][17]),mapa)
                fichero_salida.write('\t\t\t\t<leg mode = "' + modestr + '" dep_time = "' + hora_ini + '" trav_time = "' + duracion + '" arr_time = "' + hora_fin + '">\n\t\t\t\t</leg>\n')
                if len(fam_consorcio[0][0]) == 1:   # En caso de que solo le queda un plan por hacer a la persona
                    hora_ini_aux = hora_ini.replace(":", "")
                    duracionfinal = trav_time(hora_ini_aux, 2400)
                    fichero_salida.write('\t\t\t\t<act type = "' + destinostr + '" x = "' + str(x_nueva) + '" y = "' + str(y_nueva) + '" start_time = "' + hora_ini + '" dur = "' + duracionfinal + '" end_time = "24:00"/>\n')
                else:                               # En caso de que le queden mas planes a la persona
                    fichero_salida.write('\t\t\t\t<act type = "' + destinostr + '" x = "' + str(x_nueva) + '" y = "' + str(y_nueva) + '" start_time = "' + hora_ini + '" dur = "' + duracion + '" end_time = "' + hora_fin + '"/>\n')
                x_anterior = x_nueva
                y_anterior = y_nueva
                fam_consorcio[0][0].pop(0)          # Se elimina el plan ya asignado
                if len(fam_consorcio[0][0]) == 0:   # Si no le quedan mas planes a la persona se borra esta personas
                    fichero_salida.write('\t\t\t</plan>\n\t\t</person>\n\n')
                    fam_consorcio[0].pop(0)        # Se borra a la persona que no tiene ya planes
                    terminado = True
                if len(fam_consorcio[0]) == 0:   # Si no quedan mas personas en la familia se borra la familia
                    fam_consorcio.pop(0)
            terminado = False

    if len(fam_consorcio) == 0:
        return -3
    else:
        return 0