class Persona:
    def __init__(self, id, edad, genero):
        self.id = id
        self.edad = edad
        self.genero = genero
    
    def __str__(self) -> str:
        return f"id: {self.id}, edad: {self.edad}, género: {self.genero}"