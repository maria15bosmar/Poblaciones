import random

class familia:
  def __init__(self, id_familia, personas, casasp, casasm, casasg, tipofamilia):
    self.id_familia = id_familia
    self.personas = personas
    self.casa = self.coordenadas(personas, casasp, casasm, casasg)
    self.tipofamilia = tipofamilia
    print("Se ha creado la familia " + str(self.id_familia) + " que se compone de " + str(self.personas)) # + " y que se ubica en " + str(self.coordenadas[0])

  def coordenadas(self, personas, casasp, casasm, casasg):
    coordenadas = []
    num_per = len(personas)/3
    tam_casa = random.randrange(0, 1001)/10

    if num_per == 1:
      if tam_casa >= 0 and tam_casa < 14.6 and len(casasp) > 0: # Casa pequena
        coordenadas = casasp[0]
        del casasp[0]
      elif tam_casa >= 14.6 and tam_casa < 88.2 and len(casasm) > 0: # Casa mediana
        coordenadas = casasm[0]
        del casasm[0]
      elif tam_casa >= 88.2 and tam_casa <= 100.0 and len(casasg) > 0: # Casa grande
        coordenadas = casasg[0]
        del casasg[0]
    elif num_per == 2:
      if tam_casa >= 0 and tam_casa < 9.0 and len(casasp) > 0: # Casa pequena
        coordenadas = casasp[0]
        del casasp[0]
      elif tam_casa >= 9.0 and tam_casa < 83.3 and len(casasm) > 0: # Casa mediana
        coordenadas = casasm[0]
        del casasm[0]
      elif tam_casa >= 83.3 and tam_casa <= 100.0 and len(casasg) > 0: # Casa grande
        coordenadas = casasg[0]
        del casasg[0]
    elif num_per == 3:
      if tam_casa >= 0 and tam_casa < 5.5 and len(casasp) > 0: # Casa pequena
        coordenadas = casasp[0]
        del casasp[0]
      elif tam_casa >= 5.5 and tam_casa < 80.6 and len(casasm) > 0: # Casa mediana
        coordenadas = casasm[0]
        del casasm[0]
      elif tam_casa >= 80.6 and tam_casa <= 100.0 and len(casasg) > 0: # Casa grande
        coordenadas = casasg[0]
        del casasg[0]
    elif num_per == 4:
      if tam_casa >= 0 and tam_casa < 3.9 and len(casasp) > 0: # Casa pequena
        coordenadas = casasp[0]
        del casasp[0]
      elif tam_casa >= 3.9 and tam_casa < 73.6 and len(casasm) > 0: # Casa mediana
        coordenadas = casasm[0]
        del casasm[0]
      elif tam_casa >= 73.6 and tam_casa <= 100.0 and len(casasg) > 0: # Casa grande
        coordenadas = casasg[0]
        del casasg[0]
    elif num_per == 5:
      if tam_casa >= 0 and tam_casa < 1.2 and len(casasp) > 0: # Casa pequena
        coordenadas = casasp[0]
        del casasp[0]
      elif tam_casa >= 1.2 and tam_casa < 81.4 and len(casasm) > 0: # Casa mediana
        coordenadas = casasm[0]
        del casasm[0]
      elif tam_casa >= 81.4 and tam_casa <= 100.0 and len(casasg) > 0: # Casa grande
        coordenadas = casasg[0]
        del casasg[0]
    elif num_per == 6:
      if tam_casa >= 0 and tam_casa < 3.3 and len(casasp) > 0: # Casa pequena
        coordenadas = casasp[0]
        del casasp[0]
      elif tam_casa >= 3.3 and tam_casa < 80.0 and len(casasm) > 0: # Casa mediana
        coordenadas = casasm[0]
        del casasm[0]
      elif tam_casa >= 80.0 and tam_casa <= 100.0 and len(casasg) > 0: # Casa grande
        coordenadas = casasg[0]
        del casasg[0]
    elif num_per == 7:
      if tam_casa >= 0 and tam_casa < 6.3 and len(casasp) > 0: # Casa pequena
        coordenadas = casasp[0]
        del casasp[0]
      elif tam_casa >= 6.3 and tam_casa < 87.5 and len(casasm) > 0: # Casa mediana
        coordenadas = casasm[0]
        del casasm[0]
      elif tam_casa >= 87.5 and tam_casa <= 100.0 and len(casasg) > 0: # Casa grande
        coordenadas = casasg[0]
        del casasg[0]
    if len(coordenadas) == 0:
      if len(casasp) > 0:
        coordenadas = casasp[0]
        del casasp[0]
      elif len(casasm) > 0:
        coordenadas = casasm[0]
        del casasm[0]
      elif len(casasg) > 0:
        coordenadas = casasg[0]
        del casasg[0]
    return coordenadas




