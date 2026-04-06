import pytest
from ui.interface import GameInterface

def test_no_se_puede_instanciar_clase_abstracta():
    """
    Verifica que GameInterface no pueda ser instanciada directamente
    debido a que tiene métodos abstractos.
    """
    with pytest.raises(TypeError) as excinfo:
        GameInterface()
    assert "Can't instantiate abstract class GameInterface" in str(excinfo.value)

def test_subclase_incompleta_lanza_error():
    """
    Verifica que una subclase que no implementa todos los métodos 
    abstractos también lance TypeError al intentar instanciarse.
    """
    class InterfazIncompleta(GameInterface):
        def limpiar_pantalla(self):
            pass
        # Faltan el resto de métodos abstractos definidos en interface.py

    with pytest.raises(TypeError):
        InterfazIncompleta()

def test_subclase_valida_instanciacion():
    """
    Verifica que una subclase que implementa todos los métodos 
    definidos en el contrato pueda instanciarse correctamente.
    """
    class InterfazValida(GameInterface):
        def limpiar_pantalla(self): pass
        def mostrar_mensaje(self, mensaje): pass
        def mostrar_estado_juego(self, jugadores, carta_descarte): pass
        def solicitar_accion_robo(self, jugador, carta_descarte): return "mazo"
        def solicitar_descarte(self, jugador, puede_cerrar): return (0, False)
        def notificar_comodin(self, nombre, id_comodin): pass
        def mostrar_resultado_ronda(self, jugadores, cerrador): pass
        def anunciar_ganador(self, ganador): pass

    # No debería lanzar ninguna excepción
    ui = InterfazValida()
    assert isinstance(ui, GameInterface)