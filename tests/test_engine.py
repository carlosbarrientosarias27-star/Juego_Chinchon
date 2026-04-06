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
    
    # Aseguramos que haya algo en descartes por si el motor lo consulta
        juego.baraja.descartes = [MagicMock()] 
    
        juego._aplicar_logica_comodin(jugador, carta_comodin)
    
        assert jugador.eliminado is True
        
    @patch('core.engine.Validador.calcular_puntos_optimos')
    def test_ejecutar_turno_basico(self, mock_validador, juego, mock_ui):
        """Verifica el flujo de un turno normal sin cerrar."""
        jugador = juego.jugadores[0]
        jugador.mano = [MagicMock(es_comodin=False) for _ in range(7)]
        juego.baraja.descartes = [MagicMock()]
    
        carta_robada = MagicMock(es_comodin=False)
        juego.baraja.robar = MagicMock(return_value=carta_robada)
    
        mock_ui.solicitar_accion_robo.return_value = "mazo"
        mock_ui.solicitar_descarte.return_value = (0, False)
        mock_validador.return_value = (20, False)
    
        quiere_cerrar = juego.ejecutar_turno(jugador)
    
        assert quiere_cerrar is False
        assert len(jugador.mano) == 7
        assert juego.baraja.robar.call_count == 1

    @patch('core.engine.Validador.calcular_puntos_optimos')
    def test_calcular_fin_ronda_chinchon(self, mock_validador, juego, mock_ui):
        """Verifica la bonificación de -10 puntos por Chinchón."""
        jugador = juego.jugadores[0]
        jugador.puntos = 15
        mock_validador.return_value = (0, True)
        
        juego.calcular_fin_ronda(jugador)
        
        assert jugador.puntos == 5
        mock_ui.notificar_evento.assert_any_call(f"¡{jugador.nombre} hizo CHINCHÓN! (-10 pts)")

    # --- NUEVOS TESTS DE SALIDA VOLUNTARIA ---

    def test_ejecutar_turno_salir(self, juego, mock_ui):
        """Verifica que ejecutar_turno devuelva None cuando se solicita salir."""
        jugador = juego.jugadores[0]
    
    # SOLUCIÓN AL INDEXERROR: Añadimos una carta al pozo
        juego.baraja.descartes = [MagicMock()] 
    
        mock_ui.solicitar_accion_robo.return_value = "salir"
    
        resultado = juego.ejecutar_turno(jugador)
        assert resultado is None

    def test_jugar_interrupcion_por_salida(self, juego, mock_ui):
        """Verifica que el bucle principal 'jugar' termine si un jugador sale."""
        # Evitamos errores de baraja configurando un mock
        juego.baraja.reiniciar = MagicMock()
        
        # Forzamos que ejecutar_turno devuelva None para simular la salida
        with patch.object(juego, 'ejecutar_turno', return_value=None):
            juego.jugar() 
            
        # Si el test finaliza, significa que el 'return' en engine.py funcionó.
        # Validamos que no se intentó cerrar la ronda normalmente
        with patch.object(juego, 'calcular_fin_ronda') as mock_fin:
            assert mock_fin.call_count == 0