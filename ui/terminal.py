import subprocess
import os

class TerminalUI:
    def limpiar(self):
        """
        Limpia la terminal de forma segura evitando inyección de comandos.
        """
        comando = 'cls' if os.name == 'nt' else 'clear'
        # Usamos subprocess.run con shell=False (por defecto) para mayor seguridad
        try:
            subprocess.run([comando], check=True)
        except Exception:
            # Fallback en caso de que el comando no exista en el entorno
            pass

    def render_carta(self, carta):
        if carta.es_comodin:
            return f"[🍺 Comodín {carta.id_comodin}]"
        return f"[{carta.valor} de {carta.palo}]"

    def mostrar_mano(self, jugador):
        print(f"\n👉 Mano de {jugador.nombre}:")
        for i, c in enumerate(jugador.mano):
            print(f"  {i+1}. {self.render_carta(c)}")
    
    def anunciar_ganador(self, ganador):
        if ganador:
            print("\n" + "="*30)
            print(f"¡EL GANADOR ES: {ganador.nombre}!")
            print("="*30 + "\n")
        else:
            print("\nLa partida ha terminado en empate o sin ganador claro.")

    def solicitar_accion_robo(self, jugador, carta_descarte):
        """Pregunta al jugador de dónde robar o si desea salir."""
        self.mostrar_mano(jugador)
        print(f"\nCarta en el pozo: {self.render_carta(carta_descarte)}")
        
        while True:
            opcion = input("¿Robar de (M)azo, (P)ozo o (S)alir?: ").upper()
            if opcion == 'S':
                return "salir"
            if opcion == 'M':
                return "mazo"
            if opcion == 'P':
                return "pozo"
            print("❌ Opción inválida. Usa 'M', 'P' o 'S'.")
    
    def solicitar_descarte(self, jugador, puede_cerrar):
        """Pide al jugador que elija una carta para descartar y si desea cerrar."""
        self.mostrar_mano(jugador)
        
        while True:
            try:
                entrada = input(f"\nElige el número de carta para descartar (1-{len(jugador.mano)}): ")
                idx = int(entrada) - 1
                
                if 0 <= idx < len(jugador.mano):
                    quiere_cerrar = False
                    if puede_cerrar:
                        confirmacion = input("¿Quieres cerrar la partida con esta carta? (S/N): ").upper()
                        quiere_cerrar = (confirmacion == 'S')
                    
                    return idx, quiere_cerrar
                
                print(f"❌ Selección fuera de rango. Elige entre 1 y {len(jugador.mano)}.")
            except ValueError:
                print("❌ Por favor, introduce un número válido.")