import numpy as np
# Probability of house size given a number of members.
TIPOS_CASA = [(0.146, 0.736, 0.118), (0.09, 0.743, 0.167), (0.055, 0.751, 0.194),
  (0.039, 0.697, 0.264), (0.012, 0.802, 0.186), (0.033, 0.767, 0.2), (0.063, 0.812, 0.125)]

class Familia:
  def __init__(self, id_familia, personas, tipos_casas, tipofamilia):
    self.id_familia = id_familia
    self.personas = personas
    self.casa = self.coordenadas(personas, tipos_casas)
    self.tipofamilia = tipofamilia
    """
    print("Se ha creado la familia " + str(self.id_familia) + " que se compone de ")
    for i in self.personas:
      print(f"- {i}")
    print("y que se ubica en " + str(self.casa))
    """

  def coordenadas(self, personas, tipos_casas):
    """ Returns some coordinates of a house. """
    coordenadas = []
    num_per = len(personas)
    selected = np.random.choice(range(3), 1, p=TIPOS_CASA[num_per])[0]
    lista = tipos_casas[selected]
    coordenadas = lista.pop(0)
    if len(coordenadas) == 0:
      for i in tipos_casas:
        if len(i)>0:
          coordenadas = i.pop()

    return coordenadas

def sort_personas(self):
  self.personas.sort(reverse=True, key = lambda p: p.edad)

