""" Función main. Contiene las funciones pertenecientes al familiador. """

import json, copy
import numpy as np
from scipy.special import softmax
from familia import Familia
from persona import Persona
from utils import *
from planeador import planear

id_pers = 0
id_fams = 0
lista_familias = []

with open(PATH_JSON_FAMILIADOR) as f:
    INPUTS_FAMILIADOR = json.load(f)

def elegir_personas(edadmin, edadmax, genero):
    """ Devuelve una edad factible para una persona. """
    global num_ciudadanos, poblacion
    # Excepciones a tratar.
    if edadmin == 85:
        edadmax = 95
    # Edad concreta y si no superior (segundo hijo).
    if edadmax == -1:
        edadmax = edadmin + 4
        edad = edadmin
    # Mismo caso que -1 pero para adultos.
    elif edadmax == -3:
        edadmax = edadmin + 4
        edad = edadmin
        if edadmax > 95:
            edadmax = 95
    # Persona con una edad predefinida
    elif edadmax == -2:
        if edadmin >= 27 and edadmin <= 93:
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
        elif edadmin >= 95:
            edad = edadmin
            edadmin = edad - 4
            edadmax = 95
    # Si no, se hace aleatoriamente
    else:
        edad = np.random.randint(edadmin, edadmax+1)
    # Lista de posibles edades que se van a probar en orden.
    rango = list(range(edad, edadmax+1))
    rango.extend(list(range(edadmin, edad)))
    # Se busca a la persona en el rango determinado.
    for i in rango:
        if poblacion[genero][i] > 0:
            poblacion[genero][i] -= 1
            if i <= 24: # Si es un niño.
                num_ciudadanos[2 + genero] -= 1
            else: # Si es un adulto.
                num_ciudadanos[genero] -= 1
            return i
    # No se encuentra a una persona.
    if edadmax < 24:   # No quedan hijos en ese rango. Probar con hijos mayores de hasta 24 años.
        return elegir_personas(edadmax, 24, genero)
    elif edadmax == 24:  # Probamos para cualquier edad de niño.
        return elegir_personas(0, 24, genero)
    # No se encuentran adultos. Hay que probar todos los rangos de edad hasta hallar alguno.
    elif edadmax >= 25:
        if edadmax > 90:
            return elegir_personas(25, 34, genero)
        else:
            return elegir_personas(edadmin + (edadmax-edadmin+1), edadmax + (edadmax-edadmin+1), genero)
    
def sexador_hijos(numero):
    """ Se da un género a un número de hijos dado. """
    global num_ciudadanos
    generos = []
    # Se copia el número de niños y de niñas.
    num_nin = num_ciudadanos[2:].copy()
    for i in range(numero):
        # Se comprueba que queden personas de un género elegido aleatoriamente.
        while True:
            nuevo = np.random.randint(2)
            # Si se encuentran se resta una persona a la copia.
            if num_nin[nuevo] > 0:
                num_nin[nuevo]-=1
                generos.append(nuevo)
                break
    # Se devuelve el género o la lista de géneros.
    if numero == 1:
        return generos[0]
    return generos

def quasiadultos (cantidad):
    """ Comprueba que existan jóvenes de entre 18 y 24 años. """
    global poblacion
    boolean = [0, 0]
    i = 18
    # Se devuelve el número de hombres jóvenes y mujeres jóvenes que quedan.
    while i <= 24 and (boolean[0] < cantidad or boolean[1] < cantidad):
        for gen in range(2):
            if poblacion[gen][i] >= 1:
                boolean[gen] += poblacion[gen][i]
        i += 1
    return boolean

def probabilidad_disminuida(min, max):
    """ Devuelve un número en un rango, mayor probabilidad de que salga más bajo. """
    return round(np.random.beta(2, 5) * (max - min) + min)

def parejador(hay_ninyos):
    """ Devuelve una pareja facible. """
    global poblacion, id_pers
    EDADES = [18, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]
    PORC_EDAD = INPUTS_FAMILIADOR["parejador"]["edad_porcentajes"]
    # Elegir la edad de la primera persona (normalmente la mujer en parejas heterosexuales).
    # Se hace en función de la edad del hijo.
    for ind, ninyos in enumerate(range(25, 75, 5)):
        if hay_ninyos >= ninyos and hay_ninyos <= ninyos+4:
            age_range1 = ind+1
    if hay_ninyos <= 24 and hay_ninyos > 0:
        age_range1 = 0
    # Si no hay niños el range de edad es aleatorio.
    if hay_ninyos == 0:
        age_range1 = np.random.choice(len(PORC_EDAD), p=PORC_EDAD)
    # Se elige la edad de la primera persona.
    # Tener en cuenta la diferencia de edad madre/hijo para madres jóvenes.
    if age_range1 == 0:
        if hay_ninyos != 0:
            if hay_ninyos < 18:
                age1 = 18
            else:
                age1 = hay_ninyos
        # Si no quedan posibles madres jóvenes se pasa a adultas.
        if quasiadultos(2)[1] == 0:
            age1 = 25
        else:
            aux = EDADES[age_range1 + 1]
            age1 = np.random.randint(aux, aux + 5)
    # Si no hay problemas se elige aleatoriamente la primera edad.
    else:
        aux = EDADES[age_range1]
        age1 = np.random.randint(aux, aux + 5)
    # Se elige si es homogamia, hipogamia (alta/baja) o hipergamia (alta/baja) según unas probabilidades.
    tipo_pareja = np.random.choice(5, p=INPUTS_FAMILIADOR["parejador"]["probabilidad_diferencia"][age_range1])
    # La diferencia de edad es fija si no es muy elevada.
    posible_dif = INPUTS_FAMILIADOR["parejador"]["diferencia_edad"][tipo_pareja]
    if type(posible_dif) is int:
        diferencia = posible_dif
    else:
        if tipo_pareja <= 3:
            diferencia = np.random.choice(posible_dif)
        # Si la diferencia es elevada se calcula con una probabilidad disminuída.
        else:
            diferencia_base = np.random.choice(posible_dif)
            diferencia = probabilidad_disminuida(diferencia_base, diferencia_base+5)
            if tipo_pareja == 5:
                diferencia*=-1
    # Se obtiene la segunda edad dada la diferencia.
    age2 = age1 + diferencia
    if age2 > 95:
        age2 = 95
    ages = [age2, age1]
    # Se comprueba que existan dos por genero para parejas homosexuales.
    if age1 <= 24 or age2 <= 24:
        gens = quasiadultos(2)
        for i in range(2):
            if gens[i] < 2 and ages[i] <= 24:
                ages[i] = 25
    # Se elige tipo de pareja.
    # Si solo hay hombres, gay. Si solo hay mujeres, lesbianas. Si hay uno de cada, heteros.
    elecciones = ((0, 0), (1, 1), (1, 0))
    tipo = elecciones[np.random.choice(3, p=INPUTS_FAMILIADOR["parejador"]["tipo_pareja"])]
    if num_ciudadanos[0] < 1:
        tipo = (1, 1)
    elif num_ciudadanos[1] < 1:
        tipo = (0, 0)
    elif num_ciudadanos[0] == 1 and num_ciudadanos[1] == 1:
        tipo = (1, 0)
    # Obtener las personas y devolverlas.
    age1 = elegir_personas(age1, -2, tipo[0])
    age2 = elegir_personas(age2, -2, tipo[1])
    per1 = Persona(id_pers, age1, tipo[0])
    per2 = Persona(id_pers+1, age2, tipo[1])
    id_pers += 2
    return per1, per2

def tipodefamilia(tamfamilia, empleo, niños, monopar):
    """ Devuelve el tipo de familia de entre 8 dada una serie de características. """
    # Unipersonal    En el paro    Sin niños
    if tamfamilia == 1 and empleo == 0 and niños == 0:
        tipo = 1
    # Unipersonal    Trabajando  Sin niños
    elif tamfamilia == 1 and empleo == 1 and niños == 0:
        tipo = 2
    # Multipersonal  En el paro    Sin niños
    elif tamfamilia >= 2 and empleo == 0 and niños == 0:
        tipo = 3
    # Multipersonal  Trabajando  Sin niños
    elif tamfamilia >= 2 and empleo == 1 and niños == 0:
        tipo = 4
    # Multipersonal  En el paro    Con niños    Monoparental
    elif tamfamilia >= 2 and empleo == 0 and niños == 1 and monopar == 1:
        tipo = 5
    # Multipersonal  En el paro    Con niños    No Monoparental
    elif tamfamilia >= 2 and empleo == 0 and niños == 1 and monopar == 0:
        tipo = 6
    # Multipersonal  Trabajando  Con niños    Monoparental
    elif tamfamilia >= 2 and empleo == 1 and niños == 1 and monopar == 1:
        tipo = 7
    # Multipersonal  Trabajando  Con niños    No Monoparental
    elif tamfamilia >= 2 and empleo == 1 and niños == 1 and monopar == 0:
        tipo = 8
    return tipo

def simplificador(generos, edadmin, edadmax):
    """ Calcular edad de los hermanos. """
    global poblacion
    edades = []
    # Encontrar una edad factible para el primer hermano.
    edades.append(elegir_personas(edadmin, edadmax, generos[0]))
    # Calcular la diferencia de edad según una probabilidad.
    elecciones = INPUTS_FAMILIADOR["simplificador"]["diferencia_edad"]
    asumar = np.random.choice(len(elecciones), p=INPUTS_FAMILIADOR["simplificador"]["probabilidad_diferencia"])
    asumar = np.random.randint(elecciones[asumar][0], elecciones[asumar][1] + 1)
    # Aleatoriamente se elige si el hermano 1 es el mayor o el menor (multiplicar asumar por -1).
    if np.random.randint(2):
        asumar*=-1
    # Corregir irregularidades.
    edadprimero = edades[0]
    if edadprimero + asumar > 91: # Para que no se busquen personas de mas de 95
        asumar = 0
    if edadprimero > 91:
        edadprimero = 91
    if edadprimero + asumar <= 24: # Para que no se busquen niños
        asumar = 0
    # Encontrar una edad factible para el segundo hermano.
    print(edadprimero, asumar)
    edades.append(elegir_personas(edadprimero+asumar, -3, generos[1]))
    return edades

def siguientes_hijos(edad1, n_ninyos):
    """ Calcular edades coherentes en caso de que haya más de un hijo en una familia."""
    global num_ciudadanos, id_pers
    if n_ninyos == 1:
        genero_demas = []
        genero_demas.append(sexador_hijos(n_ninyos))
    else:
        genero_demas = sexador_hijos(n_ninyos)
    edades, hijos = [edad1], []
    elecciones = INPUTS_FAMILIADOR["siguientes_hijos"]["diferencia_edad"]
    diferencias = np.random.choice(len(elecciones), n_ninyos, p=INPUTS_FAMILIADOR["siguientes_hijos"]["probabilidad_diferencia"])
    for i in range(n_ninyos):
        if diferencias[i] < 3:
            edades.append(edades[-1] + elecciones[diferencias[i]])
        else:
            edades.append(edades[-1] + probabilidad_disminuida(elecciones[diferencias[i]][0], elecciones[diferencias[i]][1]))
        if edades[-1] + 4 > 24 and num_ciudadanos[genero_demas[i]] == 0:
            nuevo_hijo = elegir_personas(20, -1, genero_demas[i])
        else:
            nuevo_hijo = elegir_personas(edades[i], -1, genero_demas[i])
        id_pers += 1
        hijos.append(Persona(id_pers, nuevo_hijo, genero_demas[i]))
    return hijos

def familiador():
    global num_ciudadanos, id_pers, id_fams, lista_familias
    personas = []
    n_pers = np.random.choice(range(1, 8), p=INPUTS_FAMILIADOR["familiador"]["tipo"])
    subtipo = monopar = subsubtipo = -1
    ninyos = 0
    RANGOS_EDAD = INPUTS_FAMILIADOR["familiador"]["rangos_edad"]
    # UNIDAD UNIPERSONAL
    if n_pers == 1 and num_ciudadanos[0] + num_ciudadanos[1] > 0:
        # listas de probabilidad para numpy.
        PORC_EDAD = INPUTS_FAMILIADOR["familiador"]["1"]["edad"]
        PORC_GENERO = INPUTS_FAMILIADOR["familiador"]["1"]["genero"]
        # seleccionamos edad y género.
        edad = np.random.choice(len(PORC_EDAD), p=PORC_EDAD)
        genre_prob = PORC_GENERO[edad]
        if edad == 0:
            h, m = quasiadultos(1)
            # Si no quedan personas de un determinado género, se fija al que haya.
            if h == 0 and m == 0:
                edad = 1
                genero = np.random.choice(2, p=[1-genre_prob, genre_prob])
                if num_ciudadanos[0] < 1:
                    genero = 1
                elif num_ciudadanos[1] < 1:
                    genero = 0
            elif h <= 0:
                genero = 1
            elif m <= 0:
                genero = 0
            else:
                genero = np.random.choice(2, p=[1-genre_prob, genre_prob])
        else:
            genero = np.random.choice(2, p=[1-genre_prob, genre_prob])
            if num_ciudadanos[0] < 1:
                genero = 1
            elif num_ciudadanos[1] < 1:
                genero = 0
        unipersonal = elegir_personas(RANGOS_EDAD[edad], RANGOS_EDAD[edad+1]-1, genero)
        personas.append(Persona(id_pers, unipersonal, genero))
        id_pers+=1

    # FAMILIA DE DOS PERSONAS
    elif n_pers == 2:
        # Se elige un tipo de familia.
        DATOS_TIPO2 = INPUTS_FAMILIADOR["familiador"]["2"]
        subtipo = np.random.choice(4, p=DATOS_TIPO2["subtipo"])
        if (subtipo == 1 or subtipo == 0) and num_ciudadanos[subtipo] > 0 and num_ciudadanos[2] + num_ciudadanos[3] > 0: # PADRE/MADRE CON UN NIÑX
            monopar = ninyos = 1
            PORC_EDADES = DATOS_TIPO2["monopar"]["edad"]
            edad = np.random.choice(range(1, 6), p=PORC_EDADES)
            if edad <5:
                padre = elegir_personas(RANGOS_EDAD[edad], RANGOS_EDAD[edad+1]-1, subtipo)
            else:
                padre = elegir_personas(RANGOS_EDAD[edad], 95, subtipo)
            personas.append(Persona(id_pers, padre, subtipo))
            sexo_hijo = sexador_hijos(1)
            if padre <= 38:
                hijo = elegir_personas(0, padre-15, sexo_hijo)
            else:
                hijo = elegir_personas(0, 24, sexo_hijo)
            personas.append(Persona(id_pers, hijo, sexo_hijo))
        if subtipo == 2 and num_ciudadanos[0] + num_ciudadanos[1] > 1: # PAREJA SIN HIJOS
            pers1, pers2 = parejador(0)
            personas += [pers1, pers2]
        if subtipo == 3 and num_ciudadanos[0] + num_ciudadanos[1] > 1: # OTRO
            PORC_SUBTIPO = DATOS_TIPO2["subsubtipo"]
            subsubtipo = np.random.choice(4, p=PORC_SUBTIPO)
            if subsubtipo == 0: # HERMANOS
                PORC_EDAD = DATOS_TIPO2["hermanos"]["edad"] # Edad del primero.
                edad = np.random.choice(len(PORC_EDAD), p=PORC_EDAD)
                PORC_GENERO = DATOS_TIPO2["hermanos"]["generos"] # Generos de ambos hermnaos.
                elecciones = ((0, 0), (1, 1), (0, 1))
                if num_ciudadanos[0] < 2:
                    generos = [1, 1]
                elif num_ciudadanos[0] > 2:
                    generos = [0, 0]
                elif num_ciudadanos[0] == 1 and num_ciudadanos[1] == 1:
                    generos = [0, 1]
                else:
                    generos = elecciones[np.random.choice(3, p=PORC_GENERO)]
                if edad == 0:
                    if num_ciudadanos[0] > 1 and num_ciudadanos[1] > 1:
                        h, m = quasiadultos(2)
                        # Si no quedan personas de un determinado género, se fija al que haya o se cambia la edad.
                        if h == 0 and m == 0:
                            edad = 1
                        elif h == 1 and m == 1:
                            generos[0] = 0
                            generos[1] = 1
                        elif m == 0 and h >= 2:
                            generos[0] = 0
                            generos[1] = 0
                        elif h == 0 and m >= 2:
                            generos[0] = 1
                            generos[1] = 1
                    else:
                        edad = 1
                edades = simplificador(generos, RANGOS_EDAD[edad], RANGOS_EDAD[edad+1]-1)
                for per in range(2):
                    personas.append(Persona(id_pers, edades[per], generos[per]))
                    id_pers+=1
                # AGREGAR A FAMILIA Y CONTAR PERSONA ETC
            if subsubtipo == 5 and num_ciudadanos[2] + num_ciudadanos[3] > 0: # ABUELX Y NIETX
                ninyos = monopar = 1
                PORC_GENERO = DATOS_TIPO2["abuelo_nieto"]["genero"]
                generos = []
                for i in range(2):
                    generos.append(np.random.choice(2, p=[1 - PORC_GENERO[i], PORC_GENERO[i]]))
                # Si no quedan ciudadanos adultos de algún tipo, se usa el otro género.
                if num_ciudadanos[0] < 1:
                    generos[1] = 1
                elif num_ciudadanos[1] < 1:
                    generos[1] = 0
                PORC_EDAD_NIETO = DATOS_TIPO2["abuelo_nieto"]["edad_nieto"]
                # Si no quedan adultos, se escoge un niño y viceversa.
                if (num_ciudadanos[generos[0]] < 2 and num_ciudadanos[generos[0] + 2] < 1
                    or num_ciudadanos[generos[0]] < 2):
                    generos[0] = int(not generos[0])
                elif num_ciudadanos[generos[0] + 2] < 1:
                    seleccion = np.random.choice(range(3, 7), p=softmax(PORC_EDAD_NIETO[3:]))
                else:
                    seleccion = np.random.choice(7, p=PORC_EDAD_NIETO)
                seleccion = np.random.choice(7, p=PORC_EDAD_NIETO)
                rangos = ((0, 9), (10, 19), (20, 24), (25, 29), (30, 34), (35, 39),
                    (40, 50))
                nieto = elegir_personas(rangos[seleccion][0], rangos[seleccion][1], generos[0])
                personas.append(Persona(id_pers, nieto, generos[0]))
                id_pers += 1
                edades = np.random.choice(range(34, 86, 10), p=DATOS_TIPO2["abuelo_nieto"]["edad_abuelo"])
                abuelo = elegir_personas(edades, edades + 9, generos[1])
                personas.append(Persona(id_pers, abuelo, generos[1]))
                id_pers += 1
    elif n_pers == 3:
        # Se elige un tipo de familia.
        DATOS_TIPO3 = INPUTS_FAMILIADOR["familiador"]["3"]
        subtipo = np.random.choice(4, p=DATOS_TIPO3["subtipo"])
        if (subtipo == 1 or subtipo == 0) and num_ciudadanos[subtipo] > 0 and num_ciudadanos[2] + num_ciudadanos[3] > 1: # PADRE/MADRE CON DOS NIÑX
            ninyos, monopar = 1, 1
            PORC_EDADES = DATOS_TIPO3["monopar"]["edad"]
            edad = np.random.choice(range(1,6), 1, p=PORC_EDADES)[0]
            if edad <5:
                padre = elegir_personas(RANGOS_EDAD[edad], RANGOS_EDAD[edad+1]-1, subtipo)
            else:
                padre = elegir_personas(RANGOS_EDAD[edad], 95, subtipo)
            personas.append(Persona(id_pers, padre, subtipo))
            id_pers += 1
            sexo_hijo = sexador_hijos(1)
            if padre <= 38:
                hijo = elegir_personas(0, padre-15, sexo_hijo)
            else:
                hijo = elegir_personas(0, 24, sexo_hijo)
            personas.append(Persona(id_pers, hijo, sexo_hijo))
            id_pers += 1
            personas.extend(siguientes_hijos( hijo, 1))
        elif subtipo == 2 and num_ciudadanos[0] + num_ciudadanos[1] > 1 and num_ciudadanos[2] + num_ciudadanos[3] > 0: # PAREJA CON UN HIJX
            ninyos, monopar = 1, 0
            sexo_hijo = sexador_hijos(1)
            edad_hijo = elegir_personas( 0, 24, sexo_hijo)
            personas.append(Persona(id_pers, edad_hijo, sexo_hijo))
            id_pers += 1
            PORC_EDAD_MADRE = DATOS_TIPO3["pareja"]["edad_madre"]
            seleccion = np.random.choice(range(15, 46, 5), 1, p=PORC_EDAD_MADRE)[0]
            edad_madre = np.random.randint(seleccion, seleccion+5)
            personas.extend(parejador( edad_madre+edad_hijo))
    
    elif n_pers == 4:
        # Se elige un tipo de familia.
        DATOS_TIPO4 = INPUTS_FAMILIADOR["familiador"]["3"]
        subtipo = np.random.choice(4, p=DATOS_TIPO4["subtipo"])
        # PADRE/MADRE CON DOS NIÑXS
        if (subtipo == 1 or subtipo == 0) and num_ciudadanos[subtipo] > 0 and num_ciudadanos[2] + num_ciudadanos[3] > 2:
            ninyos, monopar = 1, 1
            PORC_EDADES = DATOS_TIPO4["monopar"]["edad"]
            edad = np.random.choice(range(1, 6), p=PORC_EDADES)
            if edad < 5:
                padre = elegir_personas(RANGOS_EDAD[edad], RANGOS_EDAD[edad+1]-1, subtipo)
            else:
                padre = elegir_personas(RANGOS_EDAD[edad], 95, subtipo)
            personas.append(Persona(id_pers, padre, subtipo))
            id_pers += 1
            sexo_hijo = sexador_hijos(1)
            if padre <= 38:
                hijo = elegir_personas(0, padre - 15, sexo_hijo)
            else:
                hijo = elegir_personas(0, 24, sexo_hijo)
            personas.extend(siguientes_hijos(hijo, 2))
            # AGREGAR A FAMILIA Y CONTAR PERSONA ETC
        elif subtipo == 2 and num_ciudadanos[0] + num_ciudadanos[1] > 1 and num_ciudadanos[2] + num_ciudadanos[3] > 1: # PAREJA CON DOS HIJOS.
            ninyos, monopar = 1, 0
            sexo_hijo = sexador_hijos(1)
            edad_hijo = elegir_personas(0, 24, sexo_hijo)
            personas.append(Persona(id_pers, edad_hijo, sexo_hijo))
            id_pers += 1
            PORC_EDAD_MADRE = DATOS_TIPO4["pareja"]["edad_madre"]
            seleccion = np.random.choice(range(15, 46, 5), 1, p=PORC_EDAD_MADRE)[0]
            edad_madre = np.random.randint(seleccion, seleccion+5)
            personas.extend(parejador(edad_madre+edad_hijo))
            personas.extend(siguientes_hijos(edad_hijo, 1))
            # AGREGAR A FAMILIA Y CONTAR PERSONA ETC

    elif n_pers == 5:
        DATOS_TIPO5 = INPUTS_FAMILIADOR["familiador"]["5"]
        prob = DATOS_TIPO5["subtipo"]
        subtipo = np.random.choice(2, p=[prob, 1-prob])
        # Pareja con tres hijos.
        if subtipo == 0 and num_ciudadanos[0] + num_ciudadanos[1] > 1 and num_ciudadanos[2] + num_ciudadanos[3] > 2:
            ninyos, monopar = 1, 0
            sexo_hijo = sexador_hijos(1)
            edad_hijo = elegir_personas(0, 24, sexo_hijo)
            personas.append(Persona(id_pers, edad_hijo, sexo_hijo))
            id_pers += 1
            PORC_EDAD_MADRE = DATOS_TIPO5["edad"]
            seleccion = np.random.choice(range(15, 46, 5), 1, p=PORC_EDAD_MADRE)[0]
            edad_madre = np.random.randint(seleccion, seleccion+5)
            personas.extend(parejador(edad_madre+edad_hijo))
            personas.extend(siguientes_hijos(edad_hijo, 1))
            # AGREGAR A FAMILIA Y CONTAR PERSONA ETC
    else:
        return
    if len(personas) == 0:
        return -1
    # Se crea la familia.
    PROB_TRABAJO = INPUTS_FAMILIADOR["familiador"]["trabajo"]
    #print(n_pers, subtipo, subsubtipo)
    if subtipo == -1:
        p = (PROB_TRABAJO[n_pers-1], 1-PROB_TRABAJO[n_pers-1])
    elif subsubtipo == -1:
        p = (PROB_TRABAJO[n_pers-1][subtipo], 1-PROB_TRABAJO[n_pers-1][subtipo])
    else:
        p = (PROB_TRABAJO[n_pers-1][subtipo][subsubtipo], 1-PROB_TRABAJO[n_pers-1][subtipo][subsubtipo])
    trabajo = np.random.choice(2, p=p)
    tipo = tipodefamilia(n_pers, trabajo, ninyos, monopar)
    lista_familias.append(Familia(id_fams, personas, casas, tipo))
    id_fams += 1

# GUARDAR POBLACIÓN

for distrito in range(INPUT_DATA["num_distritos"]):
    num_ciudadanos = []
    censo = leer_censo(distrito + 1)
    for value in censo[2:]:
        num_ciudadanos.append(value)
    poblacion = np.array([censo[0], censo[1]])
    casas = leer_catastro(distrito + 1)
    casascopia = copy.deepcopy(casas)

    print("DISTRITO", distrito)
    while num_ciudadanos[0] + num_ciudadanos[1] > 0:
        if len(casas[0]) == 0 and len(casas[1]) == 0 and len(casas[2]) == 0:
            casas = copy.deepcopy(casascopia)
        if num_ciudadanos[0] == 0 and num_ciudadanos[1] < 15:
            pass
        familiador()
        #print(poblacion)
        print(num_ciudadanos[0], num_ciudadanos[1], len(lista_familias))
planear(lista_familias)
