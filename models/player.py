from dataclasses import dataclass, field
from typing import List, Dict
from core.cards import Carta

@dataclass
class Jugador:
    """
    Representa a un participante en la partida.
    Mantiene el estado de su mano, puntuación y uso de beneficios (comodines).
    """
    nombre: str
    puntos: int = 0
    eliminado: bool = False
    # La mano se inicializa como una lista vacía por defecto
    mano: List[Carta] = field(default_factory=list)
    # Registro de qué comodines de cerveza ha consumido ya (para evitar duplicados)
    uso_comodin: Dict[int, bool] = field(default_factory=lambda: {
        1: False, # Estrella Galicia
        2: False, # Alhambra Verde
        3: False, # 1906
        4: False  # SIN CERVEZA
    })

    def añadir_a_mano(self, carta: Carta) -> None:
        """Agrega una carta a la mano del jugador."""
        self.mano.append(carta)

    def extraer_de_mano(self, indice: int) -> Carta:
        """
        Elimina y retorna una carta de la mano según su posición.
        Levanta IndexError si el índice no es válido.
        """
        if 0 <= indice < len(self.mano):
            return self.mano.pop(indice)
        raise IndexError("El índice de la carta no existe en la mano.")

    def tiene_comodin_usado(self, id_comodin: int) -> bool:
        """Verifica si el jugador ya ha activado un efecto de cerveza específico."""
        return self.uso_comodin.get(id_comodin, False)

    def marcar_comodin_usado(self, id_comodin: int) -> None:
        """Registra que un comodín ha sido procesado."""
        if id_comodin in self.uso_comodin:
            self.uso_comodin[id_comodin] = True

    @property
    def cantidad_cartas(self) -> int:
        """Retorna el número actual de cartas en mano."""
        return len(self.mano)

    def __str__(self) -> str:
        estado = "ELIMINADO" if self.eliminado else f"{self.puntos} pts"
        return f"Jugador: {self.nombre} | Estado: {estado} | Cartas: {self.cantidad_cartas}"