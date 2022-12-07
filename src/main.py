from utils import *
import pandas as pd
import numpy as np
from familia import Familia
from persona import Persona

id_pers = 0
id_fams = 0
lista_familias = []
personas = []

# GUARDAR POBLACIÓN
censo = leer_censo(1)
poblacion = np.array([censo[0], censo[1]])
ciudadanos = []
for i in censo[2:]:
    ciudadanos.append(i)
casas = leer_catastro(1)


def elegir_personas(lista, edadmin, edadmax, genero):
    """ Devuelve una edad factible para una persona. """
    global ciudadanos
    if edadmax == -1:
        edadmax = edadmin + 4
        edad = edadmin
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
        edad = np.random.randint(edadmin, edadmax+1)
    found = False
    # Lista de posibles edades que se van a probar en orden.
    rango = list(range(edad,edadmax+1))
    rango.extend(list(range(edadmin, edad)))
    # Se busca a la persona en el rango determinado.
    print("genero", genero)
    for i in rango:
        if lista[genero][i]>0:
            lista[genero][i]-=1
            found = True
            break
    # Se encuentra una persona
    if found == True:
        # Si es un niño.
        if edad <= 24:
            ciudadanos[2+genero]-=1
        # Si es un adulto.
        else:
            ciudadanos[genero]=1
        return edad
    # No se encuentra a una persona.
    else:
        if edadmax < 24:   # No quedan hijos en ese rango probar con hijos mayores de hasta 24 años
            return elegir_personas(lista, edadmax, 24, genero)
        elif edadmax == 24:  # Probamos para cualquier edad de niño
                return elegir_personas(lista, 0, 24, genero)
        elif edadmax >= 25:
            if edadmax > 90:
                return elegir_personas(lista, 25, 34, genero)
            else:
                return elegir_personas(lista, edadmin + (edadmax-edadmin+1), edadmax + (edadmax-edadmin+1), genero)
    
def sexador_hijos(numero):
    """ Se da un género a un número de hijos dado. """
    global ciudadanos
    generos = []
    for i in range(numero):
        # Se comprueba que queden personas de ese género.
        while True:
            nuevo = np.random.randint(2)
            if ciudadanos[2+nuevo]>0:
                generos.append(nuevo)
                break
    if numero == 1:
        return generos[0]
    return generos

def quasiadultos (poblacion, cantidad):
    boolean = [0, 0]
    i = 18
    # Arriba se comprobó si hay adultos pero no si hay personas de 18 a 24 aquí se hace la comprobación.
    while i <= 24 and (boolean[0] < cantidad or boolean[1] < cantidad): 
        for gen in range(2):
            if poblacion[gen][i] > 1:
                boolean[gen] += poblacion[gen][i]
        i += 1
    return boolean

def probabilidad_disminuida(min, max):
    return round(np.random.beta(2,5)*(max-min)+min)

def parejador(poblacion, hay_ninyos, personas):
    PORC_EDAD = [0.011, 0.037, 0.083, 0.129, 0.129, 0.128, 0.113, 0.095, 0.077, 0.068, 0.053, 0.043, 0.022, 0.01, 0.002]
    # Elegir la edad de la primera persona (normalmente la mujer en parejas heterosexuales).
    # Se hace en función de la edad del hijo.
    for ind, ninyos in enumerate(range(25, 75, 5)):
        if hay_ninyos >= ninyos and hay_ninyos <= ninyos+4:
            age_range1 = ind+1
    if hay_ninyos <= 24 and hay_ninyos >0:
        age_range1 = 0
    # Si no hay niños el range de edad es aleatorio.
    if hay_ninyos == 0:
        age_range1 = np.random.choice(len(PORC_EDAD), 1, p=PORC_EDAD)[0]
    # Se elige la edad de la primera persona aleatoriamente según su rango de edad.
    # Tener en cuenta la diferencia de edad madre/hijo para madres jóvenes.
    if age_range1 == 0:
        if hay_ninyos!=0:
            if hay_ninyos < 18:
                age1 = 18
            else:
                age1 = hay_ninyos
        if quasiadultos(poblacion, 2)[1] == 0:
            age1=25
        
    else:
        aux = RANGOS_EDAD[age_range1]
        age1 = np.random.randint(aux, aux+5)
    # Se elige si es homogamia, hipogamia (alta/baja) o hipergamia (alta/baja) según unas probabilidades.
    tipo_pareja = np.random.choice(5, 1, p=DIFERENCIAS_EDAD[age_range1])[0]
    # La diferencia de edad es fija si no es muy elevada.
    posible_dif = CANTIDAD_DIFERENCIA[tipo_pareja]
    print(posible_dif)
    if type(posible_dif) is int:
        diferencia = posible_dif
    else:
        if tipo_pareja <= 3:
            diferencia = np.random.choice(posible_dif, 1)[0]
        # Si la diferencia es elevada se calcula con una probabilidad disminuída.
        else:
            diferencia_base = np.random.choice(posible_dif, 1)[0]
            diferencia = probabilidad_disminuida(diferencia_base, diferencia_base+5)
            if tipo_pareja == 5:
                diferencia*=-1
    age2 = age1 + diferencia
    ages = [age2, age1]
    # Se comprueba que existan dos por genero para parejas homosexuales.
    if age1 <= 24 or age2 <= 24:
        gens = quasiadultos(poblacion, 2)
        for i in range(2):
            if gens[i] < 2 and ages[i] <= 24:
                ages[i] = 25
    # Se elige tipo de pareja.
    # --- Si solo hay hombres, gay. Si solo hay mujeres, lesbianas. Si hay uno de cada, heteros.
    PROC_TIPO_PAREJA = [0.009, 0.004, 0.987]
    elecciones = ((0, 0), (1, 1), (0, 1))
    tipo = elecciones[np.random.choice(3, 1, p=PROC_TIPO_PAREJA)[0]]
    age1 = elegir_personas(poblacion, age1, -2, tipo[0])
    age2 = elegir_personas(poblacion, age2, -2, tipo[1])
    # ---- AGREGAR A PERSONAS
    return age1, age2

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

def simplificador(generos, edadmin, edadmax, poblacion):
    """ Calcular edad de los hermanos. """
    edades = []
    # Encontrar una edad factible para el primer hermano.
    edades.append(elegir_personas(poblacion, edadmin, edadmax, generos[0]))
    # Calcular la diferencia de edad según una probabilidad.
    elecciones = [(1, 2), (4, 5), (7, 10), (12, 20)]
    asumar = np.random.choice(len(elecciones), 1, p=[0.26, 0.349, 0.272, 0.119])[0]
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
    edades.append(elegir_personas(poblacion, edadprimero+asumar, -3, generos[1]))
    return edades

def siguientes_hijos(poblacion, edad1, n_ninyos, id_pers, personas=None):
    global ciudadanos
    genero_demas = sexador_hijos(n_ninyos)
    edades, hijos = [edad1], []
    PROP_DIFERENCIA = [0.015, 0.175, 0.172, 0.588, 0.05]
    elecciones = (0, 1, 2, (3,9), (10, 20))
    diferencias = np.random.choice(len(elecciones), n_ninyos, p=PROP_DIFERENCIA)
    for i in range(n_ninyos):
        if diferencias[i] < 3:
            edades.append(edades[-1]+elecciones[diferencias[i]])
        else:
            edades.append(edades[-1]+probabilidad_disminuida(elecciones[diferencias[i]][0], elecciones[diferencias[i]][1]))
        if edades[-1]+4 > 24 and ciudadanos[genero_demas[i]] == 0:
            nuevo_hijo = elegir_personas(poblacion, 20, -1, genero_demas[i])
        else:
            nuevo_hijo = elegir_personas(poblacion, edades[i], -1, genero_demas[i])
        hijos.append(Persona(id_pers+i+1, nuevo_hijo, genero_demas[i]))
    return hijos

def familiador(poblacion):
    global ciudadanos, id_pers, id_fams, lista_familias
    personas = []
    PORC_FAMILIAS = [0.257, 0.302, 0.201, 0.176, 0.039, 0.015, 0.01]
    n_pers = np.random.choice(range(1,8), 1, p=PORC_FAMILIAS)[0]

    # UNIDAD UNIPERSONAL
    if n_pers == 1 and ciudadanos[0] + ciudadanos[1] >0:
        # listas de probabilidad para numpy.
        PORC_EDAD = [0.017, 0.124, 0.149, 0.151, 0.148, 0.143, 0.149, 0.119]
        PORC_GENERO = [0.451, 0.487, 0.536, 0.534, 0.436, 0.294, 0.203, 0.182]
        # seleccionamos edad y género.
        edad = np.random.choice(len(PORC_EDAD), 1, p=PORC_EDAD)[0]
        genre_prob = PORC_GENERO[edad]
        if edad == 0:
            h, m = quasiadultos(poblacion, 1)
            # Si no quedan personas de un determinado género, se fija al que haya.
            if h == 0 and m == 0:
                edad = 1
            if h <= 0:
                genero = 1
            if m <= 0:
                genero = 0
            else:
                genero = np.random.choice(2, 1, p=[1-genre_prob, genre_prob])[0]
        unipersonal = elegir_personas(poblacion, RANGOS_EDAD[edad], RANGOS_EDAD[edad+1]-1, genero)
        pers = Persona(id_pers, unipersonal, genero)
        trabajo = np.random.choice(2, p=PROB_TRABAJO[0])
        tipo_fam = tipodefamilia(n_pers, trabajo, 0, -1)
        lista_familias.append(Familia(id_fams, [pers], casas, tipo_fam))
        id_pers += 1
        id_fams += 1
        # AGREGAR A FAMILIA Y CONTAR PERSONA ETC

    # FAMILIA DE DOS PERSONAS
    if n_pers == 2:
        # Se elige un tipo de familia.
        PORC_TIPO_FAMILIA = [0.039, 0.181, 0.674, 0.106]
        tipo_fam = np.random.choice(4, 1, p=PORC_TIPO_FAMILIA)[0]
        # PADRE/MADRE CON UN NIÑX
        if tipo_fam == 1 or tipo_fam == 0:
            PORC_EDADES = [0.02, 0.15, 0.268, 0.207, 0.355]
            edad = np.random.choice(range(1,6), 1, p=PORC_EDADES)[0]
            if edad <5:
                padre = elegir_personas(poblacion, RANGOS_EDAD[edad], RANGOS_EDAD[edad+1]-1, tipo_fam)
            else:
                padre = elegir_personas(poblacion, RANGOS_EDAD[edad], 95, tipo_fam)
            sexo_hijo = sexador_hijos(1)
            if padre <= 38:
                hijo = elegir_personas(poblacion, 0, padre-15, sexo_hijo)
            else:
                hijo = elegir_personas(poblacion, 0, 24, sexo_hijo)
            # AGREGAR A FAMILIA Y CONTAR PERSONA ETC
        if tipo_fam == 3:
            personas = parejador(poblacion, 0, personas)
        if tipo_fam == 4:
            PORC_SUBTIPO = [0.402, 0.082, 0.107, 0.409]
            subtipo = np.random.choice(4, 1, p=PORC_SUBTIPO)[0]
            if subtipo == 1:
                PORC_EDAD = [0.043, 0.097, 0.107, 0.165, 0.232, 0.191, 0.097, 0.068]
                edad = np.random.choice(len(PORC_EDAD), 1, p=PORC_EDAD)[0]
                PORC_GENERO = [.303, 0.277, 0.42]
                elecciones = ((0, 0), (1, 1), (0, 1))
                generos = np.random.choice(3, 1, p=PORC_GENERO)[0]
                #quasi
                if edad == 0:
                    if censo[0] > 1 and censo[1] > 1:
                        h, m = quasiadultos(poblacion, 2)
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
                #quasi
                edades = simplificador(elecciones[generos], RANGOS_EDAD[edad], RANGOS_EDAD[edad+1]-1, poblacion)
                # AGREGAR A FAMILIA Y CONTAR PERSONA ETC
            if subtipo == 2:
                PORC_GENERO = [0.617, 0.148]
                generos = []
                for i in range(2):
                    generos.append(np.random.choice(2, 1, p=[1-PORC_GENERO[i], PORC_GENERO[i]])[0])
                edades = []
                PORC_EDAD_NIETO = [0.032, 0.192, 0.159, 0.322, 0.186, 0.065, 0.044]
                edades[0] = np.random.choice(range(10,41,5), 1, p=PORC_EDAD_NIETO)[0]
                nieto = elegir_personas(poblacion, edades[0], edades[0]+4, genero[0])
                PORC_EDAD_ABUELO = [0.006, 0.011, 0.049, 0.227, 0.376, 0.331]
                edades[1] = np.random.choice(range(34,96,10), 1, p=PORC_EDAD_ABUELO)[0]
                abuelo = elegir_personas(poblacion, edades[1], edades[1]+9, genero[1])
                # AGREGAR A FAMILIA Y CONTAR PERSONA ETC
    if n_pers == 3:
        # Se elige un tipo de familia.
        PORC_TIPO_FAMILIA = [0.115, 0.022, 0.74, 0.123]
        tipo_fam = np.random.choice(4, 1, p=PORC_TIPO_FAMILIA)[0]
        # PADRE/MADRE CON DOS NIÑX
        if tipo_fam == 1 or tipo_fam == 0:
            PORC_EDADES = [0.02, 0.15, 0.268, 0.207, 0.355]
            edad = np.random.choice(range(1,6), 1, p=PORC_EDADES)[0]
            if edad <5:
                padre = elegir_personas(poblacion, RANGOS_EDAD[edad], RANGOS_EDAD[edad+1]-1, tipo_fam)
            else:
                padre = elegir_personas(poblacion, RANGOS_EDAD[edad], 95, tipo_fam)
            sexo_hijo = sexador_hijos(1)
            if padre <= 38:
                hijo = elegir_personas(poblacion, 0, padre-15, sexo_hijo)
            else:
                hijo = elegir_personas(poblacion, 0, 24, sexo_hijo)
            personas = siguientes_hijos(poblacion[0], poblacion[1], hijo, 1, ciudadanos[2], ciudadanos[3], 0, personas)
            # AGREGAR A FAMILIA Y CONTAR PERSONA ETC
        elif tipo_fam == 3:
            sexo_hijo = sexador_hijos(1)
            edad_hijo = elegir_personas(poblacion, 0, 24, sexo_hijo)
            PORC_EDAD_MADRE = [0.018, 0.075, 0.174, 0.326, 0.303, 0.095, 0.009]
            seleccion = np.random.choice(range(15, 46, 5), 1, p=PORC_EDAD_MADRE)[0]
            edad_madre = np.random.randint(seleccion, seleccion+5)
            personas = parejador(poblacion, edad_madre+edad_hijo, personas)
            # AGREGAR A FAMILIA Y CONTAR PERSONA ETC
    
    if n_pers == 4:
        # Se elige un tipo de familia.
        PORC_TIPO_FAMILIA = [0.029, 0.003, 0.846, 0.122]
        tipo_fam = np.random.choice(4, 1, p=PORC_TIPO_FAMILIA)[0]
        # PADRE/MADRE CON DOS NIÑX
        if tipo_fam == 1 or tipo_fam == 0:
            PORC_EDADES = [0.02, 0.15, 0.268, 0.207, 0.355]
            edad = np.random.choice(range(1,6), 1, p=PORC_EDADES)[0]
            if edad <5:
                padre = elegir_personas(poblacion, RANGOS_EDAD[edad], RANGOS_EDAD[edad+1]-1, tipo_fam)
            else:
                padre = elegir_personas(poblacion, RANGOS_EDAD[edad], 95, tipo_fam)
            sexo_hijo = sexador_hijos(1)
            if padre <= 38:
                hijo = elegir_personas(poblacion, 0, padre-15, sexo_hijo)
            else:
                hijo = elegir_personas(poblacion, 0, 24, sexo_hijo)
            personas = siguientes_hijos(poblacion[0], poblacion[1], hijo, 2, ciudadanos[2], ciudadanos[3], 0, personas)
            # AGREGAR A FAMILIA Y CONTAR PERSONA ETC
        elif tipo_fam == 3:
            sexo_hijo = sexador_hijos(1)
            edad_hijo = elegir_personas(poblacion, 0, 24, sexo_hijo)
            PORC_EDAD_MADRE = [0.018, 0.075, 0.174, 0.326, 0.303, 0.095, 0.009]
            seleccion = np.random.choice(range(15, 46, 5), 1, p=PORC_EDAD_MADRE)[0]
            edad_madre = np.random.randint(seleccion, seleccion+5)
            personas = parejador(poblacion, edad_madre+edad_hijo, personas)
            personas = siguientes_hijos(poblacion[0], poblacion[1], edad_hijo, 1, ciudadanos[2], ciudadanos[3], 0, personas)
            # AGREGAR A FAMILIA Y CONTAR PERSONA ETC

    if n_pers == 5:
        prob = 0.658
        tipo_fam = np.random.choice(2, 1, p=[prob, 1-prob])
        if tipo_fam == 0:
            sexo_hijo = sexador_hijos(1)
            edad_hijo = elegir_personas(poblacion, 0, 24, sexo_hijo)
            PORC_EDAD_MADRE = [0.018, 0.075, 0.174, 0.326, 0.303, 0.095, 0.009]
            seleccion = np.random.choice(range(15, 46, 5), 1, p=PORC_EDAD_MADRE)[0]
            edad_madre = np.random.randint(seleccion, seleccion+5)
            personas = parejador(poblacion, edad_madre+edad_hijo, personas)
            personas = siguientes_hijos(poblacion[0], poblacion[1], edad_hijo, 2, ciudadanos[2], ciudadanos[3], 0, personas)
            # AGREGAR A FAMILIA Y CONTAR PERSONA ETC
        
