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

    @patch('builtins.print')
    def test_anunciar_ganador_con_jugador(self, mock_print, ui):
        """Verifica que se imprima el nombre del ganador con el formato decorado."""
        ganador = MagicMock()
        ganador.nombre = "Carlos"
        
        ui.anunciar_ganador(ganador)
        
        # Verificamos que se imprima el anuncio con el nombre del ganador
        mock_print.assert_any_call("\n" + "="*30)
        mock_print.assert_any_call("¡EL GANADOR ES: Carlos!")
        mock_print.assert_any_call("="*30 + "\n")

    @patch('builtins.print')
    def test_anunciar_ganador_empate(self, mock_print, ui):
        """Verifica el mensaje cuando no hay un ganador (None)."""
        ui.anunciar_ganador(None)
        
        # Verificamos el mensaje de empate o sin ganador
        mock_print.assert_called_with("\nLa partida ha terminado en empate o sin ganador claro.")

    @patch('builtins.input', side_effect=['X', 'M'])
    @patch('builtins.print')
    def test_solicitar_accion_robo_reintento(self, mock_print, mock_input, ui):
        """Verifica que el sistema reintente si la entrada es inválida y acepte 'M'."""
        mock_jugador = MagicMock(nombre="Test")
        mock_jugador.mano = []
        mock_carta = MagicMock(es_comodin=False, valor=10, palo="Copas")
        
        resultado = ui.solicitar_accion_robo(mock_jugador, mock_carta)
        
        # Debe retornar 'M' tras el segundo intento
        assert resultado == 'M'
        # Debe haber mostrado el error de opción inválida
        mock_print.assert_any_call("❌ Opción inválida. Usa 'M' para Mazo o 'P' para Pozo.")
    
    @patch('builtins.input', side_effect=['2', 'S'])
    @patch('builtins.print')
    def test_solicitar_descarte_cerrando(self, mock_print, mock_input, ui):
        """Verifica que se pueda seleccionar una carta y elegir cerrar la partida."""
        mock_jugador = MagicMock()
        mock_jugador.mano = [MagicMock(), MagicMock()]
        
        idx, cerrar = ui.solicitar_descarte(mock_jugador, puede_cerrar=True)
        
        assert idx == 1  # El usuario eligió '2'
        assert cerrar is True

    @patch('builtins.input', return_value='S')
    @patch('builtins.print')
    def test_solicitar_accion_robo_salir(self, mock_print, mock_input, ui):
        """Verifica que la opción 'S' devuelva la señal de salida."""
        mock_jugador = MagicMock(nombre="Test")
        mock_jugador.mano = []
        mock_carta = MagicMock(es_comodin=False)
        
        resultado = ui.solicitar_accion_robo(mock_jugador, mock_carta)
        
        assert resultado == "salir"
    
    @patch('builtins.input', side_effect=['2', 'S'])
    @patch('builtins.print')
    def test_solicitar_descarte_cerrando(self, mock_print, mock_input, ui):
        """Verifica que se pueda seleccionar una carta y elegir cerrar la partida."""
        mock_jugador = MagicMock()
        mock_jugador.mano = [MagicMock(), MagicMock()] # Simulamos 2 cartas
        
        idx, cerrar = ui.solicitar_descarte(mock_jugador, puede_cerrar=True)
        
        assert idx == 1  # El usuario eligió '2', que es índice 1
        assert cerrar is True # El usuario eligió 'S'