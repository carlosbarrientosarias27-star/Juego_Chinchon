import pytest
from unittest.mock import MagicMock
from models.player import Jugador

@pytest.fixture
def jugador_test():
    """Proporciona una instancia limpia de Jugador para cada test."""
    return Jugador(nombre="Cervezero")

class TestJugador:

    def test_inicializacion_por_defecto(self, jugador_test):
        """Verifica que un jugador nuevo tenga los valores iniciales correctos."""
        assert jugador_test.nombre == "Cervezero"
        assert jugador_test.puntos == 0
        assert jugador_test.eliminado is False
        assert len(jugador_test.mano) == 0
        # Verifica que todos los comodines inicien en False
        assert all(usado is False for usado in jugador_test.uso_comodin.values())

    def test_añadir_a_mano(self, jugador_test):
        """Valida que la carta se agregue correctamente a la lista de la mano."""
        mock_carta = MagicMock()
        jugador_test.añadir_a_mano(mock_carta)
        assert jugador_test.cantidad_cartas == 1
        assert jugador_test.mano[0] == mock_carta

    def test_extraer_de_mano_valido(self, jugador_test):
        """Verifica la extracción exitosa de una carta por su índice."""
        mock_carta = MagicMock()
        jugador_test.añadir_a_mano(mock_carta)
        
        carta_extraida = jugador_test.extraer_de_mano(0)
        
        assert carta_extraida == mock_carta
        assert jugador_test.cantidad_cartas == 0

    def test_extraer_de_mano_indice_invalido(self, jugador_test):
        """Asegura que se lance IndexError si el índice no existe."""
        with pytest.raises(IndexError, match="El índice de la carta no existe"):
            jugador_test.extraer_de_mano(99)

    def test_gestion_comodines(self, jugador_test):
        """Prueba el ciclo de vida del uso de comodines (verificar y marcar)."""
        id_comodin = 3 # Ejemplo: 1906
        
        # Estado inicial
        assert jugador_test.tiene_comodin_usado(id_comodin) is False
        
        # Marcar como usado
        jugador_test.marcar_comodin_usado(id_comodin)
        assert jugador_test.tiene_comodin_usado(id_comodin) is True

    def test_propiedad_cantidad_cartas(self, jugador_test):
        """Verifica que el decorador @property funcione dinámicamente."""
        assert jugador_test.cantidad_cartas == 0
        jugador_test.mano = [MagicMock(), MagicMock()]
        assert jugador_test.cantidad_cartas == 2

    def test_representacion_string(self, jugador_test):
        """Valida el método __str__ en estado normal y eliminado."""
        # Estado normal
        res_normal = str(jugador_test)
        assert "Cervezero" in res_normal
        assert "0 pts" in res_normal
        
        # Estado eliminado
        jugador_test.eliminado = True
        res_eliminado = str(jugador_test)
        assert "ELIMINADO" in res_eliminado