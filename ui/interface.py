from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from models.player import Jugador
from core.cards import Carta

class GameInterface(ABC):
    """
    Clase base abstracta que define el contrato para cualquier Interfaz de Usuario.
    Ninguno de estos métodos tiene implementación aquí; se definen en ui/terminal.py.
    """

    @abstractmethod
    def limpiar_pantalla(self) -> None:
        """Limpia el buffer de la interfaz actual."""
        pass

    @abstractmethod
    def mostrar_mensaje(self, mensaje: str) -> None:
        """Muestra un mensaje informativo al usuario."""
        pass

    @abstractmethod
    def mostrar_estado_juego(self, jugadores: List[Jugador], carta_descarte: Optional[Carta]) -> None:
        """Muestra la situación general de la mesa y las puntuaciones."""
        pass

    @abstractmethod
    def solicitar_accion_robo(self, jugador: Jugador, carta_descarte: Carta) -> str:
        """
        Pregunta al jugador si quiere robar del mazo ('mazo') o del descarte ('descarte').
        Retorna un string con la elección.
        """
        pass

    @abstractmethod
    def solicitar_descarte(self, jugador: Jugador, puede_cerrar: bool) -> Tuple[int, bool]:
        """
        Solicita al jugador qué carta tirar.
        Retorna una tupla (indice_carta, quiere_cerrar).
        """
        pass

    @abstractmethod
    def notificar_comodin(self, nombre: str, id_comodin: int) -> None:
        """Muestra una alerta visual cuando alguien roba una cerveza/comodín."""
        pass

    @abstractmethod
    def mostrar_resultado_ronda(self, jugadores: List[Jugador], cerrador: Jugador) -> None:
        """Muestra el desglose de puntos al finalizar una ronda."""
        pass

    @abstractmethod
    def anunciar_ganador(self, ganador: Optional[Jugador]) -> None:
        """Muestra el mensaje final de fin de partida."""
        pass