# 📄 Reporte de Vulnerabilidad: Bandit B605

Atributo	    Detalle
ID del Error	B605: start_process_with_a_shell
Gravedad	    ALTA (Alta)
Confianza	    ALTA (Alta)
CWE	CWE-78:     Inyección de comandos del sistema operativo
Ubicación	    ui/terminal.py- Línea 5 


# Explicación del Problema

El error ocurre porque estás usando os.system(). Esta función ejecuta comandos directamente en la shell (consola) del sistema operativo.

## ¿Por qué es peligroso?

Si alguna vez permitieras que una entrada de usuario llegara a esa función (por ejemplo, os.system(f"echo {input_usuario}")), un atacante podría escribir algo como ; rm -rf / y tu programa lo ejecutaría con los permisos actuales del sistema. Bandit marca todas las llamadas a os.system() como riesgo alto porque invocan una shell intermedia innecesaria.


# 🛠️ Solución Paso a Paso

Para solucionar esto, debemos evitar os.system() y usar el módulo subprocess, que es más moderno y seguro, ya que permite ejecutar comandos sin invocar la shell directamente.

## Paso 1: Importar el módulo adecuado

Cambiamos import os por el módulo que gestiona procesos de forma segura.Pitón

import subprocess
import os

## Paso 2: Refactorizar el métodolimpiar

En lugar de pasarle un string a la shell, le pasamos una lista de argumentos al sistema operativo. Esto evita que la shell interprete caracteres especiales como ; o &.

## Paso 3: Código corregido

Actualiza tu archivo ui/terminal.py de la siguiente manera:Pitónimport subprocess

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


# ✅ ¿Por qué esto soluciona el error?

- Evita la Shell: Al usar subprocess.run(), el comando se envía directamente al sistema operativo como un binario ejecutable, no como una cadena de texto que la consola deba "interpretar".

- Validación de Bandit: Bandit dejará de marcar la línea porque subprocess es la recomendación estándar para evitar la vulnerabilidad CWE-78.

- Manejo de Errores: Se añade un bloque try-except por si el entorno donde se corre el juego (como algunas consolas de IDEs) no reconoce los comandos de sistema.