import os

class TerminalUI:
    def limpiar(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def render_carta(self, carta):
        if carta.es_comodin:
            return f"[🍺 Comodín {carta.id_comodin}]"
        return f"[{carta.valor} de {carta.palo}]"

    def mostrar_mano(self, jugador):
        print(f"\n👉 Mano de {jugador.nombre}:")
        for i, c in enumerate(jugador.mano):
            print(f"  {i+1}. {self.render_carta(c)}")