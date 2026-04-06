from typing import List, Optional
from models.player import Jugador
from core.cards import Baraja, Carta
from core.validator import Validador
from ui.interface import GameInterface

class JuegoChinchon:
    """
    Motor principal del juego. 
    Controla el flujo de la partida, turnos y reglas de negocio.
    """
    
    def __init__(self, nombres_jugadores: List[str], ui: GameInterface):
        self.ui = ui
        self.jugadores = [Jugador(nombre) for nombre in nombres_jugadores]
        self.baraja = Baraja()
        self.ronda_actual = 1
        self.finalizado = False

    def obtener_jugadores_activos(self) -> List[Jugador]:
        return [j for j in self.jugadores if not j.eliminado]

    def _aplicar_logica_comodin(self, jugador: Jugador, carta: Carta):
        """Implementa las reglas de los comodines de cerveza."""
        num = carta.id_comodin
        efectos = {
            1: ("Estrecha Galicia", lambda j: setattr(j, 'puntos', 80) if j.puntos >= 100 else None),
            2: ("Alhambra Verde", lambda j: setattr(j, 'puntos', 25) if j.puntos >= 50 else None),
            3: ("1906", lambda j: setattr(j, 'puntos', max(0, j.puntos - 25)) if j.puntos >= 25 else None),
            4: ("SIN CERVEZA", lambda j: setattr(j, 'eliminado', True))
        }
        
        nombre_c, accion = efectos.get(num, ("Desconocido", lambda j: None))
        self.ui.notificar_comodin(nombre_c, num)
        accion(jugador)
        jugador.uso_comodin[num] = True

    def preparar_ronda(self):
        """Reinicia la baraja y reparte cartas."""
        self.baraja.reiniciar()
        self.baraja.descartes = [self.baraja.robar()]
        for jugador in self.obtener_jugadores_activos():
            jugador.mano = [self.baraja.robar() for _ in range(7)]

    def ejecutar_turno(self, jugador: Jugador) -> bool:
        """
        Gestiona el turno de un jugador. 
        Retorna True si el jugador decide cerrar la ronda.
        """
        # 1. Fase de Robo
        opcion = self.ui.solicitar_accion_robo(jugador, self.baraja.descartes[-1])
        
        if opcion == "mazo":
            carta = self.baraja.robar()
            if carta.es_comodin:
                self._aplicar_logica_comodin(jugador, carta)
                if jugador.eliminado: return False
                # Si no muere, roba otra carta normal según reglas
                carta = self.baraja.robar()
        else:
            carta = self.baraja.descartes.pop()

        jugador.mano.append(carta)

        # 2. Fase de Descarte/Cierre
        puntos_actuales, _ = Validador.calcular_puntos_optimos(jugador.mano)
        puede_cerrar = puntos_actuales <= 15
        
        idx_descarte, quiere_cerrar = self.ui.solicitar_descarte(jugador, puede_cerrar)
        
        carta_fuera = jugador.mano.pop(idx_descarte)
        self.baraja.descartes.append(carta_fuera)
        
        return quiere_cerrar

    def calcular_fin_ronda(self, cerrador: Jugador):
        """Procesa los puntos de todos al final de una ronda."""
        for j in self.obtener_jugadores_activos():
            puntos, es_chinchon = Validador.calcular_puntos_optimos(j.mano)
            
            if es_chinchon:
                j.puntos -= 10
                self.ui.notificar_evento(f"¡{j.nombre} hizo CHINCHÓN! (-10 pts)")
            else:
                j.puntos += puntos
            
            if j.puntos >= 100:
                j.eliminado = True
                self.ui.notificar_evento(f"{j.nombre} ha sido eliminado por puntos.")

    def jugar(self):
        """Bucle principal de la partida (Main Loop)."""
        while len(self.obtener_jugadores_activos()) > 1:
            self.preparar_ronda()
            ronda_activa = True
            
            while ronda_activa:
                for jugador in self.obtener_jugadores_activos():
                    cerrar = self.ejecutar_turno(jugador)
                    if cerrar:
                        self.calcular_fin_ronda(jugador)
                        ronda_activa = False
                        break
                    
                    if len(self.obtener_jugadores_activos()) <= 1:
                        ronda_activa = False
                        break
            
            self.ui.mostrar_puntuaciones(self.jugadores)
            self.ronda_actual += 1

        ganadores = self.obtener_jugadores_activos()
        self.ui.anunciar_ganador(ganadores[0] if ganadores else None)