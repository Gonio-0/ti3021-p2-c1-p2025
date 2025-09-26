class Mascota:
    def __init__(self, nombre: str, edad: int, especie: str):
        self._nombre: str = nombre
        self._edad: int = edad
        self._especie: str = especie

class Perro:
    def __init__(self, vacunas: str):
        self.__vacunas: str = vacunas

class Gato:
    def __init__(self, registro_esterilizacion: str):
        self.__registro_esterilizacion: str = registro_esterilizacion

class Ave:
    def __init__(self, control_vuelo: str, jaula: str):
        self.__control_vuelo: str = control_vuelo
        self.__jaula: str = jaula