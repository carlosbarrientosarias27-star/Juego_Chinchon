import pytest
from core.cards import Baraja, Carta

def test_baraja_inicializacion():
    # Check if the deck has 44 cards (40 standard + 4 jokers)
    mazo = Baraja()
    assert len(mazo.cartas) == 44

def test_robar_carta():
    mazo = Baraja()
    carta = mazo.robar()
    assert isinstance(carta, Carta)
    assert len(mazo.cartas) == 43

def test_puntos_comodin():
    comodin = Carta(es_comodin=True)
    assert comodin.obtener_puntos() == 0

def test_puntos_normales():
    carta = Carta(palo='Oros', valor=7)
    assert carta.obtener_puntos() == 7

def test_reabastecer_mazo():
    mazo = Baraja()
    mazo.cartas = []
    # 3 cartas en descartes
    mazo.descartes = [Carta('Copas', 1), Carta('Copas', 2), Carta('Copas', 3)]
    
    # Esta llamada ejecuta la lógica de reabastecimiento
    carta = mazo.robar()
    
    # AJUSTE: Ahora el mazo tiene 1 carta (2 que pasaron menos 1 que se robó)
    assert len(mazo.cartas) == 1  
    assert len(mazo.descartes) == 1