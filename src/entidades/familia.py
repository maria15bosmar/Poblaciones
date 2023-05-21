""" Clase Familia. """

import numpy as np
import json
from utils import PATH_JSON_FAMILIADOR

with open(PATH_JSON_FAMILIADOR) as f:
	INPUTS_FAMILIADOR = json.load(f)

class Familia:
	id_fams = 0
	""" Representa una familia con su id, sus personas, las coordenadas de su hogar y su tipo. """
	def __init__(self, personas, tipos_casas, tipofamilia):
		self.id_familia = Familia.id_fams # id numérico.
		Familia.id_fams += 1
		self.personas = personas # Lista de personas.
		self.casa = self.coordenadas(personas, tipos_casas) # Coordenadas de la casa.
		self.tipofamilia = tipofamilia # Tipo de familia.
		self.n_adultos = 0
		self.n_hijos = 0
		
		# Datos numéricos sobre la familia y posición inicial de las personas.
		for pers in self.personas:
			pers.posicion = [self.casa[0], self.casa[1]]
			self.n_adultos += pers.adulto
			self.n_hijos += ((pers.adulto - 1) * -1)
		"""
		print("Se ha creado la familia " + str(self.id_familia) + " que se compone de ")
		for i in self.personas:
			print(f"- {i}")
		print("y que se ubica en " + str(self.casa))
		"""

	def coordenadas(self, personas, tipos_casas):
		""" Devuelve unas coordenadas de una casa. """
		coordenadas = []
		num_per = len(personas)
		# Seleccionar aleatoriamente una casa grande, mediana o pequeña.
		selected = np.random.choice(range(3), p=INPUTS_FAMILIADOR["familiador"]["tipos_casas"][num_per])
		# Si esa lista tiene casas aún, se extrae la primera.
		if len(tipos_casas[selected]) > 0:
			lista = tipos_casas[selected]
		# Si no, se selecciona de cualquiera de las otras listas en las que sea posible.
		else:
			for i in range(3):
				if len(tipos_casas[i]) > 0:
					lista = tipos_casas[i]
					break
		coordenadas = lista.pop(0)
		return coordenadas

	def sort_personas(self):
		""" Ordena las personas de una familia por edad. """
		self.personas.sort(reverse=True, key = lambda p: p.edad)