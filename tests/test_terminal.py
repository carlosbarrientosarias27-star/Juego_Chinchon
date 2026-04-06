import pytest
from unittest.mock import MagicMock, patch
from ui.terminal import TerminalUI

@pytest.fixture
def ui():
    return TerminalUI()

class TestTerminalUI:

    @patch('ui.terminal.subprocess.run') 
    def test_limpiar_windows(self, mock_run, ui):
        """Verifica que se llame a 'cls' si el sistema es Windows (nt)."""
        with patch('os.name', 'nt'):
            ui.limpiar()
            mock_run.assert_called_with(['cls'], check=True)

    @patch('ui.terminal.subprocess.run')
    def test_limpiar_unix(self, mock_run, ui):
        """Verifica que se llame a 'clear' en sistemas Linux/Mac."""
        with patch('os.name', 'posix'):
            ui.limpiar()
            mock_run.assert_called_with(['clear'], check=True)

    def test_render_carta_normal(self, ui):
        """Valida el formato de texto para una carta común."""
        mock_carta = MagicMock(es_comodin=False, valor=7, palo="Oros")
        resultado = ui.render_carta(mock_carta)
        assert resultado == "[7 de Oros]"

    def test_render_carta_comodin(self, ui):
        """Valida el formato de texto para comodines."""
        mock_carta = MagicMock(es_comodin=True, id_comodin=3)
        resultado = ui.render_carta(mock_carta)
        assert "[🍺 Comodín 3]" in resultado

    @patch('builtins.print')
    def test_mostrar_mano(self, mock_print, ui):
        """Verifica que se imprima la mano del jugador."""
        jugador = MagicMock(nombre="Alice")
        carta = MagicMock(es_comodin=False, valor=1, palo="Bastos")
        jugador.mano = [carta]
        ui.mostrar_mano(jugador)
        mock_print.assert_any_call("\n👉 Mano de Alice:")

    @patch('builtins.print')
    def test_anunciar_ganador(self, mock_print, ui):
        """Verifica el anuncio del ganador."""
        ganador = MagicMock(nombre="Carlos")
        ui.anunciar_ganador(ganador)
        mock_print.assert_any_call("¡EL GANADOR ES: Carlos!")

    @patch('builtins.input', side_effect=['X', 'M'])
    @patch('builtins.print')
    def test_solicitar_accion_robo_reintento(self, mock_print, mock_input, ui):
        """Verifica reintento por entrada inválida."""
        mock_jugador = MagicMock(nombre="Test", mano=[])
        mock_carta = MagicMock(es_comodin=False)
        resultado = ui.solicitar_accion_robo(mock_jugador, mock_carta)
        assert resultado == 'mazo'

    @patch('builtins.input', side_effect=['2', 'S'])
    @patch('builtins.print')
    def test_solicitar_descarte_cerrando(self, mock_print, mock_input, ui):
        """Verifica selección de carta y cierre."""
        mock_jugador = MagicMock(mano=[MagicMock(), MagicMock()])
        idx, cerrar = ui.solicitar_descarte(mock_jugador, puede_cerrar=True)
        assert idx == 1
        assert cerrar is True

    @patch('builtins.input', return_value='S')
    @patch('builtins.print')
    def test_solicitar_accion_robo_salir(self, mock_print, mock_input, ui):
        """Verifica que 'S' devuelva 'salir'."""
        mock_jugador = MagicMock(nombre="Test", mano=[])
        mock_carta = MagicMock(es_comodin=False)
        resultado = ui.solicitar_accion_robo(mock_jugador, mock_carta)
        assert resultado == "salir"