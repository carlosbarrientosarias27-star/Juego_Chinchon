import pytest
from unittest.mock import MagicMock
from core.validator import Validador

# Helper para crear cartas mockeadas rápidamente
def crear_carta(valor, palo, es_comodin=False):
    carta = MagicMock()
    carta.valor = valor
    carta.palo = palo
    carta.es_comodin = es_comodin
    # El valor para puntos suele ser el valor nominal (1-7) o 10 para sota/caballo/rey
    carta.obtener_puntos.return_value = valor if valor <= 7 else 10
    return carta

class TestValidador:

    ## --- Tests de Escalera ---
    def test_es_escalera_valida(self):
        """Verifica una escalera básica del mismo palo."""
        cartas = [
            crear_carta(1, "Oros"),
            crear_carta(2, "Oros"),
            crear_carta(3, "Oros")
        ]
        assert Validador.es_escalera(cartas) is True

    def test_es_escalera_distinto_palo(self):
        """Una escalera no es válida si los palos son distintos."""
        cartas = [
            crear_carta(1, "Oros"),
            crear_carta(2, "Copas"),
            crear_carta(3, "Oros")
        ]
        assert Validador.es_escalera(cartas) is False

    def test_es_escalera_salto_numerico(self):
        """Una escalera no es válida si los valores no son consecutivos."""
        cartas = [
            crear_carta(1, "Espadas"),
            crear_carta(2, "Espadas"),
            crear_carta(4, "Espadas")
        ]
        assert Validador.es_escalera(cartas) is False

    def test_es_escalera_con_comodin(self):
        """La lógica actual descarta escaleras que contengan comodines."""
        cartas = [
            crear_carta(1, "Oros"),
            crear_carta(2, "Oros", es_comodin=True),
            crear_carta(3, "Oros")
        ]
        assert Validador.es_escalera(cartas) is False

    ## --- Tests de Grupo ---
    def test_es_grupo_valido(self):
        """Verifica un grupo de cartas con el mismo valor."""
        cartas = [
            crear_carta(5, "Oros"),
            crear_carta(5, "Copas"),
            crear_carta(5, "Bastos")
        ]
        assert Validador.es_grupo(cartas) is True

    def test_es_grupo_insuficiente(self):
        """Un grupo debe tener al menos 3 cartas."""
        cartas = [crear_carta(7, "Oros"), crear_carta(7, "Copas")]
        assert Validador.es_grupo(cartas) is False

    ## --- Tests de Puntos y Chinchón ---
    def test_calcular_puntos_sin_combos(self):
        """Si no hay combinaciones, debe sumar el valor de todas las cartas."""
        mano = [
            crear_carta(1, "Oros"), # 1 pto
            crear_carta(10, "Copas") # 10 pts (Sota)
        ]
        puntos, chinchon = Validador.calcular_puntos_optimos(mano)
        assert puntos == 11
        assert chinchon is False

    def test_detectar_chinchon(self):
        """Verifica que una mano de 7 cartas que forman un combo sea Chinchón (-10 pts)."""
        # Creamos una escalera de 7 cartas de Oros
        mano_chinchon = [crear_carta(v, "Oros") for v in [1, 2, 3, 4, 5, 6, 7]]
        
        puntos, chinchon = Validador.calcular_puntos_optimos(mano_chinchon)
        
        assert puntos == -10
        assert chinchon is True

    ## --- Tests de búsqueda de combinaciones ---
    def test_buscar_combos_existentes(self):
        """Verifica que identifique correctamente combinaciones dentro de la mano."""
        mano = [
            crear_carta(1, "Bastos"),
            crear_carta(2, "Bastos"),
            crear_carta(3, "Bastos"),
            crear_carta(7, "Oros")
        ]
        combos = Validador._buscar_combos(mano)
        assert len(combos) > 0
        assert all(c.palo == "Bastos" for c in combos[0])