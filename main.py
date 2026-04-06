from core.engine import JuegoChinchon
from ui.terminal import TerminalUI

def iniciar_partida():
    ui = TerminalUI()
    ui.limpiar()
    
    print("--- CHINCHÓN PROFESIONAL ---")
    nombres = []
    num = int(input("Número de jugadores (2-4): "))
    for i in range(num):
        nombres.append(input(f"Nombre J{i+1}: "))

    # Iniciar motor
    juego = JuegoChinchon(nombres, ui)
    juego.jugar()

if __name__ == "__main__":
    iniciar_partida()