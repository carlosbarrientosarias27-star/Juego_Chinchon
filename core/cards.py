import random
from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True) # Inmutable para evitar errores de lógica
class Carta:
    palo: Optional[str] = None
    valor: Optional[int] = None
    es_comodin: bool = False
    id_comodin: Optional[int] = None

    def obtener_puntos(self) -> int:
        return 0 if self.es_comodin else (self.valor or 0)

class Baraja:
    PALOS = ['Oros', 'Copas', 'Espadas', 'Bastos']
    VALORES = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]

    def __init__(self):
        self.cartas: List[Carta] = []
        self.descartes: List[Carta] = []
        self._inicializar()

    def _inicializar(self):
        self.cartas = [Carta(p, v) for p in self.PALOS for v in self.VALORES]
        self.cartas += [Carta(es_comodin=True, id_comodin=i) for i in range(1, 5)]
        random.shuffle(self.cartas)

    def robar(self) -> Carta:
        if not self.cartas:
            self._reabastecer_mazo()
        return self.cartas.pop()

    def _reabastecer_mazo(self):
        if len(self.descartes) <= 1: return
        ultima = self.descartes.pop()
        self.cartas = self.descartes[:]
        self.descartes = [ultima]
        random.shuffle(self.cartas)
