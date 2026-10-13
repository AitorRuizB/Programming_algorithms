import sys, pygame
from astar import *
from pygame.locals import *
from time import process_time

MARGEN = 3
MARGEN_INFERIOR = 66
CELDA = 30
AMARILLO = (255, 255, 0)

IMPAS = (0,0,0)          # En el archivo se corresponde con '#', en memoria con 0, color negro.
LLANO = (250, 180, 160)  # '.', 1, beige
HUMEDO = (173, 216, 230) # '~', 2, azul claro
ROCOSO = (110, 75, 48)   # '*', 3, marrón oscuro
ALTO_BOTON = 32
ANCHO_BOTON = 64

class Mapa():

    def __init__(self, archivo):
        self.mapa = []
        self.filas = 0
        self.columnas = 0
        fich = open(archivo, "r")
        for cadena in fich:
            self.mapa.append([])
            for i in range(len(cadena)):
                if cadena[i] == ".":
                    self.mapa[self.filas].append(1)
                elif cadena[i] == "~":
                    self.mapa[self.filas].append(2)
                elif cadena[i] == "*":
                    self.mapa[self.filas].append(3)
                elif cadena[i] == "#":
                    self.mapa[self.filas].append(0)
            self.filas += 1
        self.columnas = len(self.mapa[0])
        self.ancho = self.columnas*(CELDA + MARGEN) + MARGEN
        self.alto = self.filas*(CELDA + MARGEN) + MARGEN + MARGEN_INFERIOR
        fich.close()

    def __str__(self):
        salida = ""
        for f in range(self.filas):
            for c in range(self.columnas):
                if self.mapa[f][c] == 1: # pradera
                    salida += ". "
                elif self.mapa[f][c] == 2: # pantano
                    salida += "~ "
                elif self.mapa[f][c] == 3: # montaña
                    salida += "* "
                elif self.mapa[f][c] == 0: # impenetrable
                    salida += "# "
                else:
                    print(f"Error imprimiendo mapa, {f}{c} = {self.mapa[f][c]}")
            salida += "\n"
        return salida

#Devuelve si se ha pulsado algún botón
def pulsaBotonesA(tab, pos):
    res = 0
    if pos[1] > tab.alto - MARGEN_INFERIOR + 6 and pos[1] < tab.alto - MARGEN_INFERIOR + 6 + ALTO_BOTON:
        if   pos[0] > tab.ancho - (ANCHO_BOTON+6)*3 and pos[0] < tab.ancho - (ANCHO_BOTON+6)*2 - 6:
            res = 1
        elif pos[0] > tab.ancho - (ANCHO_BOTON+6)*2 and pos[0] < tab.ancho - (ANCHO_BOTON+6)*1 - 6:
            res = 2
    return res

# Construye la matriz para guardar el camino
def inic(tab):
    cam = []
    for i in range(tab.filas):
        cam.append([])
        for j in range(tab.columnas):
            cam[i].append('.')
    return cam

def main():
    pygame.init()
    reloj = pygame.time.Clock()

    if len(sys.argv) == 1: #si no hay parámetros coge mapa por defecto
        file = 'mapa_12x12_variado.txt'
    else:
        file = sys.argv[1]

    tab = Mapa(file)
    camino = inic(tab)

    screen = pygame.display.set_mode([tab.ancho,tab.alto])
    pygame.display.set_caption("Practica 1 SI")

    boton1 = pygame.image.load("img_boton1.png").convert()
    boton2 = pygame.image.load("img_boton2.png").convert()
    boton3 = pygame.image.load("img_boton3.png").convert()

    personaje = pygame.image.load("img_conejo.png").convert()
    personaje = pygame.transform.scale(personaje, [CELDA, CELDA])
    objetivo = pygame.image.load("img_zanahoria.png").convert()
    objetivo = pygame.transform.scale(objetivo, [CELDA, CELDA])

    N_HEUR = 4
    HEUR = ["Trivial","Euclídea","Manhattan","Dist Diagonal"]

    heur = 0
    f = -1
    cal = 0
    running = True

    filO = colO = filD = colD = -1
    epsilon = 0.07
    if len(sys.argv) > 5:
        try:
            filO = int(sys.argv[2])
            colO = int(sys.argv[3])
            filD = int(sys.argv[4])
            colD = int(sys.argv[5])
        except ValueError:
            print("Los parámetros segundo al quinto han de ser enteros (fila y columna del conejo y la zanahoria)")
            exit()
        if filO<0 or filO>=tab.alto or colO<0 or colO>=tab.ancho or filD<0 or filD>=tab.alto or colD<0 or colD>=tab.ancho:
            print("Los parámetros segundo al quinto han de ser enteros dentro del rango del tamaño del mapa (fila y columna del conejo y la zanahoria)")
            exit()
        if len(sys.argv) > 6:
            try:
                heur = int(sys.argv[6])
            except ValueError:
                print(f"El sexto parámetros debe ser un entero del 0 al {N_HEUR} (número de la heurística)")
                exit()
            if len(sys.argv) > 7:
                try:
                    epsilon = float(sys.argv[6])
                except ValueError:
                    print("El séptimo parámetro debe ser un float mayor que cero (epsilon)")
                    exit()

    while running:
        #procesamiento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                algoritmo = pulsaBotonesA(tab, pos)
                if algoritmo:
                    if filO == -1 or filD == -1:
                        print('Error: primero coloca en el tablero el conejo (origen) y la zanahoria (destino)')
                    else:
                        NADA = 0
                        INFO = 1
                        TRAZ = 2
                        camino = inic(tab)
                        start = process_time()
                        f, cal, explorados = astar(tab, filO, colO, filD, colD, heur, epsilon*(algoritmo-1), NADA, camino)
                        elapsed = process_time() - start
                        print(f'{HEUR[heur]}, {file}, <{filO}, {colO}>, <{filD}, {colD}>, {epsilon*(algoritmo-1)}:  f {f:5.1f}, cal {cal:3d}, nodos {explorados:3d}, t: {elapsed:.6f}')
                        
                # Click en botón de cambiar heurística
                elif pos[1] > tab.alto - MARGEN_INFERIOR + 6 and pos[1] < tab.alto - MARGEN_INFERIOR + 6 + altoBoton \
                and pos[0] > tab.ancho - (anchoBoton+6)   and pos[0] < tab.ancho - 6:
                    heur += 1
                    if heur == N_HEUR:
                        heur = 0

                # Click en el tablero
                elif pos[0] > MARGEN and pos[0] < tab.ancho - MARGEN \
                and pos[1] > MARGEN and pos[1] < tab.alto - MARGEN - MARGEN_INFERIOR:
                
                    if event.button == 1:   #botón izquierdo
                        filO = pos[1]//(CELDA+MARGEN)
                        colO = pos[0]//(CELDA+MARGEN)
                        if tab.mapa[filO][colO] <= 0:
                            filO = -1
                            colO = -1
                            print('Esa casilla no es un origen válido')
                    elif event.button == 3: #botón derecho
                        colD = pos[0]//(CELDA+MARGEN)
                        filD = pos[1]//(CELDA+MARGEN)
                        if tab.mapa[filD][colD] <= 0:
                            filD = -1
                            colD = -1
                            print('Esa casilla no es un destino válido')

        #limpiar pantalla y pintar mapa
        screen.fill(IMPAS)
        for fil in range(tab.filas):
            for col in range(tab.columnas):
                if camino[fil][col] != '.':
                    pygame.draw.rect(screen, AMARILLO, [(CELDA+MARGEN)*col+MARGEN, (CELDA+MARGEN)*fil+MARGEN, CELDA, CELDA], 0)
                elif tab.mapa[fil][col] == 1:
                    pygame.draw.rect(screen, LLANO, [(CELDA+MARGEN)*col+MARGEN, (CELDA+MARGEN)*fil+MARGEN, CELDA, CELDA], 0)
                elif tab.mapa[fil][col] == 2:
                    pygame.draw.rect(screen, HUMEDO, [(CELDA+MARGEN)*col+MARGEN, (CELDA+MARGEN)*fil+MARGEN, CELDA, CELDA], 0)
                elif tab.mapa[fil][col] == 3:
                    pygame.draw.rect(screen, ROCOSO, [(CELDA+MARGEN)*col+MARGEN, (CELDA+MARGEN)*fil+MARGEN, CELDA, CELDA], 0)
                elif tab.mapa[fil][col] == 0:
                    pygame.draw.rect(screen, IMPAS, [(CELDA+MARGEN)*col+MARGEN, (CELDA+MARGEN)*fil+MARGEN, CELDA, CELDA], 0)

        # Pinta conejo, zanahoria y botones
        anchoBoton = 64
        altoBoton = 32
        screen.blit(personaje, [(CELDA+MARGEN)*colO+MARGEN, (CELDA+MARGEN)*filO+MARGEN])
        screen.blit(objetivo, [(CELDA+MARGEN)*colD+MARGEN, (CELDA+MARGEN)*filD+MARGEN])
        screen.blit(boton1, [tab.ancho - (anchoBoton+6)*3 - 6, tab.alto - MARGEN_INFERIOR + 6])
        screen.blit(boton2, [tab.ancho - (anchoBoton+6)*2 - 6, tab.alto - MARGEN_INFERIOR + 6])
        screen.blit(boton3, [tab.ancho - (anchoBoton+6)*1 - 0, tab.alto - MARGEN_INFERIOR + 6])

        #pinta f, cal y heurística seleccionada
        fuente = pygame.font.Font(None, 25)
        if f != -1:
            textoF = fuente.render("f: " + str(f), True, AMARILLO)
            screen.blit(textoF, [5, tab.alto - 60])
            textoCal = fuente.render("Cal: " + str(cal), True, AMARILLO)
            screen.blit(textoCal, [5, tab.alto - 40])
        texto_heuristica = fuente.render("Heurística: " + HEUR[heur], True, AMARILLO)
        screen.blit(texto_heuristica, [5, tab.alto - 20])

        #actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)

    pygame.quit()

#---------------------------------------------------------------------
if __name__ == "__main__":
    main()
