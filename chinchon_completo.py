"""
Juego del Chinchón - Proyecto Completo (Versión Unificada)
Incluye lógica de baraja, validación, comodines de cerveza y UI en terminal.
"""

import random
import os
import time

# ==========================================
# 1. CONSTANTES Y CONFIGURACIÓN UI
# ==========================================

class ANSI:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

PALOS = ['Oros', 'Copas', 'Espadas', 'Bastos']
VALORES = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]

# Configuración de los comodines (ID: (Nombre, Color))
COMODINES_INFO = {
    1: ("Estrella Galicia", ANSI.CYAN),
    2: ("Alhambra Verde", ANSI.GREEN),
    3: ("1906", ANSI.RED),
    4: ("SIN CERVEZA", ANSI.WHITE)
}

# ==========================================
# 2. CLASES BÁSICAS (Carta, Baraja, Jugador)
# ==========================================

class Carta:
    """Representa una carta de la baraja española o un comodín."""
    def __init__(self, palo=None, valor=None, es_comodin=False, id_comodin=None):
        self.palo = palo
        self.valor = valor
        self.es_comodin = es_comodin
        self.id_comodin = id_comodin

    def obtener_puntos(self):
        if self.es_comodin:
            return 0
        return self.valor

    def __str__(self):
        if self.es_comodin:
            nombre, color = COMODINES_INFO[self.id_comodin]
            return f"{color}[🍺 {nombre}]{ANSI.RESET}"
        
        simbolos = {'Oros': '🪙', 'Copas': '🍷', 'Espadas': '🗡️', 'Bastos': '🪵'}
        colores = {'Oros': ANSI.YELLOW, 'Copas': ANSI.RED, 'Espadas': ANSI.BLUE, 'Bastos': ANSI.GREEN}
        
        val_str = str(self.valor)
        if self.valor == 10: val_str = "Sota"
        elif self.valor == 11: val_str = "Caballo"
        elif self.valor == 12: val_str = "Rey"
            
        return f"{colores[self.palo]}[{val_str} {simbolos[self.palo]}]{ANSI.RESET}"

class Baraja:
    """Gestiona el mazo de cartas y los descartes."""
    def __init__(self):
        self.cartas = []
        self.descartes = []
        self.construir()

    def construir(self):
        self.cartas = [Carta(palo=p, valor=v) for p in PALOS for v in VALORES]
        for i in range(1, 5):
            self.cartas.append(Carta(es_comodin=True, id_comodin=i))
        self.barajar()

    def barajar(self):
        random.shuffle(self.cartas)

    def robar(self):
        if not self.cartas:
            # Si se acaba el mazo, reusar descartes excepto el último
            if len(self.descartes) > 1:
                self.cartas = self.descartes[:-1]
                self.descartes = [self.descartes[-1]]
                self.barajar()
            else:
                return None
        return self.cartas.pop()

class Jugador:
    """Mantiene el estado, la mano y los puntos de un jugador."""
    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []
        self.puntos = 0
        self.eliminado = False
        self.uso_comodin = {1: False, 2: False, 3: False, 4: False}

    def robar_carta(self, carta):
        self.mano.append(carta)

    def descartar(self, indice):
        if 0 <= indice < len(self.mano):
            return self.mano.pop(indice)
        return None

# ==========================================
# 3. LÓGICA DE VALIDACIÓN (Chinchón y Grupos)
# ==========================================

class Validador:
    """Contiene la lógica para calcular combinaciones y puntos de la mano."""
    
    @staticmethod
    def son_consecutivos(cartas):
        """Verifica si una lista de cartas forma una escalera válida."""
        if len(cartas) < 3: return False
        palo = cartas[0].palo
        if any(c.palo != palo for c in cartas): return False
        
        # Mapeo de valores para saltar del 7 al 10 en la escalera
        orden_valores = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 10:8, 11:9, 12:10}
        ordenados = sorted(cartas, key=lambda c: orden_valores[c.valor])
        
        for i in range(len(ordenados) - 1):
            if orden_valores[ordenados[i+1].valor] - orden_valores[ordenados[i].valor] != 1:
                return False
        return True

    @staticmethod
    def son_grupo(cartas):
        """Verifica si una lista de cartas forma un grupo del mismo valor."""
        if len(cartas) < 3: return False
        valor = cartas[0].valor
        return all(c.valor == valor for c in cartas)

    @classmethod
    def obtener_combinaciones_validas(cls, mano):
        """Encuentra todas las combinaciones posibles (grupos o escaleras) en la mano."""
        import itertools
        combinaciones = []
        # Solo buscamos combinaciones de 3 a 7 cartas
        for r in range(3, 8):
            for combo in itertools.combinations(mano, r):
                if cls.son_grupo(combo) or cls.son_consecutivos(combo):
                    combinaciones.append(list(combo))
        return combinaciones

    @classmethod
    def calcular_puntos_optimos(cls, mano):
        """Encuentra la cantidad mínima de puntos que quedan sin combinar.
        Retorna (puntos_minimos, es_chinchon)"""
        if not mano:
            return 0, False

        combinaciones = cls.obtener_combinaciones_validas(mano)
        
        # Caso base: si no hay combinaciones, sumamos todo
        mejor_puntuacion = sum(c.obtener_puntos() for c in mano)
        es_chinchon = False

        # Si hay una combinación de 7 cartas, es Chinchón directo
        if any(len(c) == 7 for c in combinaciones):
            return -10, True

        # Búsqueda recursiva o iterativa simple para la mejor combinación
        for combo in combinaciones:
            mano_restante = mano.copy()
            # Retirar cartas del combo de la mano restante
            try:
                for carta in combo:
                    mano_restante.remove(carta)
                
                # Buscar subcombinaciones en lo que queda
                puntos_restantes = sum(c.obtener_puntos() for c in mano_restante)
                sub_combos = cls.obtener_combinaciones_validas(mano_restante)
                if sub_combos:
                    for sub in sub_combos:
                        sub_restante = mano_restante.copy()
                        for c in sub: sub_restante.remove(c)
                        p = sum(c.obtener_puntos() for c in sub_restante)
                        if p < puntos_restantes:
                            puntos_restantes = p
                
                if puntos_restantes < mejor_puntuacion:
                    mejor_puntuacion = puntos_restantes
            except ValueError:
                continue

        return mejor_puntuacion, False


# ==========================================
# 4. MOTOR DEL JUEGO Y LÓGICA DE COMODINES
# ==========================================

class JuegoChinchon:
    def __init__(self, nombres_jugadores):
        self.jugadores = [Jugador(nombre) for nombre in nombres_jugadores]
        self.baraja = Baraja()
        self.ronda_actual = 1

    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def activar_comodin(self, jugador, carta_comodin):
        """Aplica los efectos de los comodines según el pseudocódigo del PDF."""
        num = carta_comodin.id_comodin
        nombre_c, color = COMODINES_INFO[num]
        
        print(f"\n{color}┌─────────────────────────────────────────┐")
        print(f"│ ¡{jugador.nombre.upper()} HA ROBADO EL COMODÍN {num}! │")
        print(f"│ {nombre_c.center(39)} │")
        print(f"└─────────────────────────────────────────┘{ANSI.RESET}\n")
        time.sleep(1.5)

        if num == 1: # Estrella Galicia
            if jugador.puntos >= 100 and not jugador.uso_comodin[1]: # Adaptado para asegurar la salvación
                jugador.puntos = 80
                jugador.uso_comodin[1] = True
                print(f"{ANSI.CYAN}¡Estrella Galicia pagada! Te salvas de la eliminación. Bajas a 80 puntos.{ANSI.RESET}")
            else:
                print("Comodín 1 no aplicable (necesitas estar en riesgo de eliminación). Se descarta.")
                
        elif num == 2: # Alhambra Verde
            if jugador.puntos >= 50 and not jugador.uso_comodin[2]:
                jugador.puntos = 25
                jugador.uso_comodin[2] = True
                print(f"{ANSI.GREEN}¡Alhambra Verde activada! Puntos reducidos de golpe a 25.{ANSI.RESET}")
            else:
                print("Comodín 2 no aplicable (necesitas 50 puntos o más). Se descarta.")

        elif num == 3: # Estrella 1906
            if jugador.puntos >= 25 and not jugador.uso_comodin[3]:
                jugador.puntos = max(0, jugador.puntos - 25)
                jugador.uso_comodin[3] = True
                print(f"{ANSI.RED}¡1906 activada! -25 puntos. Ahora tienes {jugador.puntos} puntos.{ANSI.RESET}")
            else:
                print("Comodín 3 no aplicable (necesitas 25 puntos o más). Se descarta.")

        elif num == 4: # SIN CERVEZA
            print(f"{ANSI.BOLD}{ANSI.RED}¡CRÍTICO! {jugador.nombre} robó el comodín SIN CERVEZA.{ANSI.RESET}")
            print("Efecto: Eliminación inmediata de la partida.")
            jugador.eliminado = True
            jugador.uso_comodin[4] = True
            
        time.sleep(2.5)

    def iniciar_ronda(self):
        self.baraja.construir()
        self.baraja.descartes = [self.baraja.robar()]
        
        # Repartir 7 cartas a los jugadores activos
        for jugador in self.jugadores:
            if not jugador.eliminado:
                jugador.mano = [self.baraja.robar() for _ in range(7)]

    def turno_jugador(self, jugador):
        self.limpiar_pantalla()
        print(f"{ANSI.BOLD}═══ RONDA {self.ronda_actual} | TURNO DE {jugador.nombre.upper()} ═══{ANSI.RESET}")
        
        # Mostrar descartes
        carta_tope = self.baraja.descartes[-1] if self.baraja.descartes else "Vacío"
        print(f"\n📥 Pila de descarte: {carta_tope}")
        
        # Mostrar mano
        print(f"🃏 Tu mano: ")
        for i, c in enumerate(jugador.mano):
            print(f"  [{i+1}] {c}")

        # Fase 1: Robar
        print("\n¿Qué deseas hacer?")
        print("  1. Robar del mazo oculto")
        print(f"  2. Robar el descarte ({carta_tope})")
        
        opcion = ""
        while opcion not in ["1", "2"]:
            opcion = input("Elige una opción (1/2): ")

        carta_robada = None
        if opcion == "1":
            carta_robada = self.baraja.robar()
            print(f"\nHas robado: {carta_robada}")
        else:
            carta_robada = self.baraja.descartes.pop()
            print(f"\nHas recogido: {carta_robada}")

        time.sleep(1)

        # Detectar comodín inmediatamente
        if carta_robada.es_comodin:
            self.activar_comodin(jugador, carta_robada)
            # El comodín se descarta/desaparece automáticamente
            if not jugador.eliminado:
                print("Debes robar una carta normal para completar tu turno.")
                time.sleep(2)
                return self.turno_jugador(jugador) # Reiniciar turno sin el comodín
            return False # Jugador fue eliminado por el comodín 4

        jugador.mano.append(carta_robada)

        # Fase 2: Descartar / Cerrar
        self.limpiar_pantalla()
        print(f"{ANSI.BOLD}═══ FASE DE DESCARTE | {jugador.nombre.upper()} ═══{ANSI.RESET}\n")
        for i, c in enumerate(jugador.mano):
            print(f"  [{i+1}] {c}")

        puntos_actuales, es_chinchon = Validador.calcular_puntos_optimos(jugador.mano)
        
        print("\nOpciones:")
        print("  [Número] Descartar esa carta y pasar turno.")
        if puntos_actuales <= 15: # Permite cerrar si tiene buena mano combinada
            print(f"  {ANSI.GREEN}[C] Descartar una carta y CERRAR LA RONDA{ANSI.RESET}")

        eleccion = ""
        cerrar = False
        indice_descarte = -1

        while True:
            eleccion = input("Elige qué carta descartar (1-8) o 'C' para cerrar: ").upper()
            if eleccion == 'C' and puntos_actuales <= 15:
                # Si cierra, debe elegir con qué carta cerrar
                idx = input("¿Qué carta descartas boca abajo para cerrar? (1-8): ")
                if idx.isdigit() and 1 <= int(idx) <= len(jugador.mano):
                    indice_descarte = int(idx) - 1
                    cerrar = True
                    break
            elif eleccion.isdigit() and 1 <= int(eleccion) <= len(jugador.mano):
                indice_descarte = int(eleccion) - 1
                break

        carta_descartada = jugador.descartar(indice_descarte)
        self.baraja.descartes.append(carta_descartada)
        print(f"\nHas descartado {carta_descartada}.")
        time.sleep(1)

        return cerrar

    def mostrar_puntuaciones(self):
        print(f"\n{ANSI.BOLD}📊 PUNTUACIONES ACUMULADAS 📊{ANSI.RESET}")
        print("=" * 40)
        for j in self.jugadores:
            estado = f"{ANSI.RED}ELIMINADO{ANSI.RESET}" if j.eliminado else f"{j.puntos} pts"
            comodines = []
            if j.uso_comodin[1]: comodines.append("Estrella")
            if j.uso_comodin[2]: comodines.append("Alhambra")
            if j.uso_comodin[3]: comodines.append("1906")
            if j.uso_comodin[4]: comodines.append("Muerte")
            str_com = f" [{', '.join(comodines)}]" if comodines else ""
            print(f"{j.nombre.ljust(15)} : {estado}{str_com}")
        print("=" * 40)
        input("\nPresiona ENTER para continuar...")

    def calcular_final_ronda(self, cerrador):
        self.limpiar_pantalla()
        print(f"{ANSI.BOLD}{ANSI.YELLOW}¡{cerrador.nombre.upper()} HA CERRADO LA RONDA!{ANSI.RESET}\n")
        
        for jugador in self.jugadores:
            if not jugador.eliminado:
                puntos_mano, chinchon = Validador.calcular_puntos_optimos(jugador.mano)
                if chinchon:
                    print(f"🎉 ¡{jugador.nombre} ha hecho CHINCHÓN! (-10 puntos)")
                    jugador.puntos -= 10
                else:
                    print(f"🃏 {jugador.nombre} suma {puntos_mano} puntos por cartas no combinadas.")
                    jugador.puntos += puntos_mano

                # Comprobar eliminación normal
                if jugador.puntos >= 100:
                    print(f"{ANSI.RED}💀 {jugador.nombre} ha alcanzado/superado los 100 puntos y queda ELIMINADO.{ANSI.RESET}")
                    jugador.eliminado = True
        
        time.sleep(3)

    def jugar(self):
        self.limpiar_pantalla()
        print(f"{ANSI.BOLD}{ANSI.YELLOW}=========================================={ANSI.RESET}")
        print(f"{ANSI.BOLD}{ANSI.YELLOW}🍺   BIENVENIDO AL JUEGO DEL CHINCHÓN   🍺{ANSI.RESET}")
        print(f"{ANSI.BOLD}{ANSI.YELLOW}=========================================={ANSI.RESET}\n")
        time.sleep(2)

        jugadores_activos = [j for j in self.jugadores if not j.eliminado]

        while len(jugadores_activos) > 1:
            self.iniciar_ronda()
            ronda_terminada = False
            
            # Bucle de turnos de la ronda
            while not ronda_terminada:
                for jugador in self.jugadores:
                    if jugador.eliminado: continue
                    
                    cerrar = self.turno_jugador(jugador)
                    if cerrar:
                        self.calcular_final_ronda(jugador)
                        ronda_terminada = True
                        break
                    
                    # Chequeo por si fue eliminado por el comodín 4 durante su turno
                    jugadores_activos = [j for j in self.jugadores if not j.eliminado]
                    if len(jugadores_activos) <= 1:
                        ronda_terminada = True
                        break

            self.ronda_actual += 1
            self.mostrar_puntuaciones()
            jugadores_activos = [j for j in self.jugadores if not j.eliminado]

        # Fin de partida
        self.limpiar_pantalla()
        print(f"{ANSI.BOLD}{ANSI.GREEN}🏆 ¡FIN DE LA PARTIDA! 🏆{ANSI.RESET}")
        
        if len(jugadores_activos) == 1:
            ganador = jugadores_activos[0]
            print(f"\n¡El ganador es {ANSI.BOLD}{ganador.nombre.upper()}{ANSI.RESET} con {ganador.puntos} puntos!")
            
            # Penalización por comodines no usados
            comodines_restantes = sum(1 for c in self.baraja.cartas + self.baraja.descartes if c.es_comodin)
            if comodines_restantes > 0:
                print(f"\nQuedaron {comodines_restantes} comodín(es) sin usar en la baraja.")
                penalizacion = comodines_restantes * 5
                ganador.puntos -= penalizacion
                print(f"Se descuentan {penalizacion} puntos al ganador. Puntuación final: {ganador.puntos} puntos.")
        else:
            print("\nTodos los jugadores han sido eliminados. ¡Empate catastrófico!")

# ==========================================
# 5. EJECUCIÓN DEL SCRIPT
# ==========================================

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Preparando mesa...")
    
    while True:
        try:
            num_jugadores = int(input("¿Cuántos jugadores van a jugar? (2-4): "))
            if 2 <= num_jugadores <= 4:
                break
            print("Por favor, introduce un número entre 2 y 4.")
        except ValueError:
            print("Entrada inválida. Usa números.")

    nombres = []
    for i in range(num_jugadores):
        nombres.append(input(f"Nombre del jugador {i+1}: "))

    juego = JuegoChinchon(nombres)
    juego.jugar()