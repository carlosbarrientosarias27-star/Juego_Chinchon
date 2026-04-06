import pytest
from unittest.mock import MagicMock, patch
from ui.terminal import TerminalUI

@pytest.fixture
def ui():
    return TerminalUI()

class TestTerminalUI:

    # Cambiamos os.system por subprocess.run
    @patch('ui.terminal.subprocess.run') 
    def test_limpiar_windows(self, mock_run, ui):
        """Verifica que se llame a 'cls' si el sistema es Windows (nt)."""
        with patch('os.name', 'nt'):
            ui.limpiar()
            # Validamos que se llamó a subprocess con la lista ['cls']
            mock_run.assert_called_with(['cls'], check=True)

    @patch('ui.terminal.subprocess.run')
    def test_limpiar_unix(self, mock_run, ui):
        """Verifica que se llame a 'clear' en sistemas Linux/Mac."""
        with patch('os.name', 'posix'):
            ui.limpiar()
            # Validamos que se llamó a subprocess con la lista ['clear']
            mock_run.assert_called_with(['clear'], check=True)

    def test_render_carta_normal(self, ui):
        """Valida el formato de texto para una carta común."""
        mock_carta = MagicMock()
        mock_carta.es_comodin = False
        mock_carta.valor = 7
        mock_carta.palo = "Oros"
        
        resultado = ui.render_carta(mock_carta)
        assert resultado == "[7 de Oros]"

    def test_render_carta_comodin(self, ui):
        """Valida el formato de texto con el icono de cerveza para comodines."""
        mock_carta = MagicMock()
        mock_carta.es_comodin = True
        mock_carta.id_comodin = 3
        
        resultado = ui.render_carta(mock_carta)
        assert "[🍺 Comodín 3]" in resultado

    @patch('builtins.print')
    def test_mostrar_mano(self, mock_print, ui):
        """Verifica que se imprima la mano del jugador con el índice correcto."""
        # Configuración del jugador mock
        jugador = MagicMock()
        jugador.nombre = "Alice"
        
        # Carta mock
        carta = MagicMock(es_comodin=False, valor=1, palo="Bastos")
        jugador.mano = [carta]
        
        ui.mostrar_mano(jugador)
        
        # Verificamos que se llame a print con el nombre y la carta renderizada
        mock_print.assert_any_call("\n👉 Mano de Alice:")
        mock_print.assert_any_call("  1. [1 de Bastos]")