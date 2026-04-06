import pytest
from unittest.mock import MagicMock, patch
from core.engine import JuegoChinchon

@pytest.fixture
def mock_ui():
    """Simula la interfaz de usuario para evitar bloqueos por input."""
    return MagicMock()

@pytest.fixture
def juego(mock_ui):
    """Instancia base del juego con dos jugadores."""
    nombres = ["Jugador1", "Jugador2"]
    return JuegoChinchon(nombres, mock_ui)

class TestJuegoChinchon:

    def test_inicializacion(self, juego):
        """Verifica que el estado inicial sea correcto."""
        assert len(juego.jugadores) == 2
        assert juego.ronda_actual == 1
        assert not juego.finalizado

    def test_obtener_jugadores_activos(self, juego):
        """Verifica que no se incluyan jugadores eliminados."""
        juego.jugadores[0].eliminado = True
        activos = juego.obtener_jugadores_activos()
        assert len(activos) == 1
        assert activos[0].nombre == "Jugador2"

    def test_aplicar_logica_comodin_muerte(self, juego, mock_ui):
        """Verifica que el comodín ID 4 elimina al jugador."""
        jugador = juego.jugadores[0]
        carta_comodin = MagicMock(id_comodin=4)
        
        juego._aplicar_logica_comodin(jugador, carta_comodin)
        
        assert jugador.eliminado is True
        mock_ui.notificar_comodin.assert_called_with("SIN CERVEZA", 4)

    def test_aplicar_logica_comodin_descuento_1906(self, juego):
        """Verifica que el comodín ID 3 resta 25 puntos (mínimo 0)."""
        jugador = juego.jugadores[0]
        jugador.puntos = 50
        carta_comodin = MagicMock(id_comodin=3)
        
        juego._aplicar_logica_comodin(jugador, carta_comodin)
        
        assert jugador.puntos == 25

    @patch('core.engine.Validador.calcular_puntos_optimos')
    def test_ejecutar_turno_robo_mazo_normal(self, mock_validador, juego, mock_ui):
        """Verifica el flujo de robo del mazo y descarte sin cerrar."""
        jugador = juego.jugadores[0]
        # Empezamos con la mano estándar de 7 cartas
        jugador.mano = [MagicMock(es_comodin=False) for _ in range(7)]
    
        # Configuramos la carta que se va a robar
        carta_robada = MagicMock(es_comodin=False)
        juego.baraja.robar = MagicMock(return_value=carta_robada)
    
        # Configuramos las respuestas de la UI
        mock_ui.solicitar_accion_robo.return_value = "mazo"
        # El jugador descarta la primera carta (índice 0) y decide NO cerrar
        mock_ui.solicitar_descarte.return_value = (0, False)
        
        # El validador dice que tiene 20 puntos (no puede cerrar, pero el test lo fuerza a False)
        mock_validador.return_value = (20, False)
    
        # EJECUCIÓN
        quiere_cerrar = juego.ejecutar_turno(jugador)
    
        # VERIFICACIÓN
        assert quiere_cerrar is False
        # Debe seguir teniendo 7 cartas (7 iniciales + 1 robada - 1 descartada)
        assert len(jugador.mano) == 7
        # Verificamos que se llamó al robo del mazo
        juego.baraja.robar.assert_called()

    @patch('core.engine.Validador.calcular_puntos_optimos')
    def test_calcular_fin_ronda_chinchon(self, mock_validador, juego, mock_ui):
        """Verifica la bonificación de -10 puntos por Chinchón."""
        jugador = juego.jugadores[0]
        jugador.puntos = 15
        # Simulamos que el validador detecta Chinchón
        mock_validador.return_value = (0, True)
        
        juego.calcular_fin_ronda(jugador)
        
        # 15 puntos iniciales - 10 de bono = 5
        assert jugador.puntos == 5
        mock_ui.notificar_evento.assert_any_call(f"¡{jugador.nombre} hizo CHINCHÓN! (-10 pts)")