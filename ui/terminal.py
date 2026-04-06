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