import pytest
from unittest.mock import patch, MagicMock
from main import iniciar_partida

class TestMain:

    @patch('main.JuegoChinchon')
    @patch('main.TerminalUI')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_iniciar_partida_flujo_completo(self, mock_print, mock_input, mock_ui_class, mock_juego_class):
        """
        Verifica que iniciar_partida solicite el número de jugadores,
        sus nombres, e instancie el motor del juego correctamente.
        """
        # 1. Configuración de mocks
        # Simulamos: 2 jugadores, nombres 'Ana' y 'Bert'
        mock_input.side_effect = ["2", "Ana", "Bert"]
        
        # Mock de la instancia de UI y de Juego
        mock_ui_instancia = mock_ui_class.return_value
        mock_juego_instancia = mock_juego_class.return_value
        
        # 2. Ejecución
        iniciar_partida()
        
        # 3. Aseveraciones (Assertions)
        # Verificar que se limpió la pantalla al inicio
        mock_ui_instancia.limpiar.assert_called_once()
        
        # Verificar que se solicitaron los nombres la cantidad de veces correcta
        assert mock_input.call_count == 3
        
        # Verificar que se instanció JuegoChinchon con los datos correctos
        mock_juego_class.assert_called_once_with(["Ana", "Bert"], mock_ui_instancia)
        
        # Verificar que se llamó al método principal para empezar a jugar
        mock_juego_instancia.jugar.assert_called_once()

    @patch('main.TerminalUI')
    @patch('builtins.input')
    def test_iniciar_partida_error_input_no_numerico(self, mock_input, mock_ui):
        """Verifica que el programa falle si el número de jugadores no es un entero."""
        mock_input.return_value = "invalid"
        
        with pytest.raises(ValueError):
            iniciar_partida()