""" Clase Persona. """

class Persona:
    """ Representa a una persona que forma parte de una familia. """
    id_pers = 0
    def __init__(self, edad, genero):
        self.id = Persona.id_pers
        Persona.id_pers += 1
        self.edad = edad
        self.genero = genero

    def __str__(self) -> str:
        return f"id: {self.id}, edad: {self.edad}, género: {self.genero}"

    def __eq__(self, other) -> bool:
        return self.id == other.id
