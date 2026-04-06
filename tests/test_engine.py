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
        """Simula un turno normal robando del mazo sin cerrar."""
        jugador = juego.jugadores[0]
        jugador.mano = [MagicMock() for _ in range(7)]
        
        # Configuración de mocks
        mock_ui.solicitar_accion_robo.return_value = "mazo"
        mock_ui.solicitar_descarte.return_value = (0, False)  # (índice, quiere_cerrar)
        mock_validador.return_value = (20, False)  # 20 puntos, no chinchón
        
        cerro = juego.ejecutar_turno(jugador)
        
        assert cerro is False
        assert len(jugador.mano) == 7
        mock_ui.solicitar_accion_robo.assert_called()

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
        mock_ui.notificar_evento.assert_any_call(f"¡{jugador.nombre} hizo CHINCHÓN! (-10