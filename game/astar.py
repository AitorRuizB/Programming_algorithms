#AITOR RUIZ BAUTISTA 2391025G

import math
class Nodo:
    def __init__(self, pos, g=0, h=0,f=0, padre=None,cal=0):
        self.pos = pos
        self.g = g
        self.h = h
        self.f = f
        self.padre = padre
        self.cal=cal

def coste(p1, p2):
    """Calcula el costo de moverse de p1 a p2."""
    return 1 if (p1[0] == p2[0] or p1[1] == p2[1]) else 1.5

def estimacion(ox, oy, dx, dy,h):

    if (h==0):
        return 0 #Trivial
    if (h==1):#Distancia Euclídea
        return math.sqrt((dx-ox)**2+(dy-oy)**2)
    if (h==2):#Distancia heurística de Manhattan
        return abs(dx - ox) + abs(dy - oy)
    if (h==3): #Distancia Diagonal
        return max(abs(ox-dx), abs(oy-dy))
    
    

def is_on_L(nodo, lista):
    """Verifica si un nodo ha sido explorado por posición."""
    return any(n.pos == nodo.pos for n in lista)

def reconstruir_camino(nodo):
    """Reconstruye el camino desde la meta hasta el inicio."""
    camino = []
    while nodo:
        camino.append(nodo.pos)
        nodo = nodo.padre
    return camino[::-1]  # Se invierte para que el camino vaya desde el inicio hasta la meta

def construir_focal(frontera,epsilon):
    """Construye la sublista para el computo de calorías"""
    focal=[]
    nodo_menor_f=min(frontera, key=lambda n: n.f)
    for nodos in frontera:
        if nodos.f<=((1+ epsilon)*nodo_menor_f.f):
            focal.append(nodos)
    return focal

def calcular_cal(vecino,tab):
    """Cálculo de calorías según la casilla"""
    if tab.mapa[vecino[0]][vecino[1]] == 1:
        return 2
    if tab.mapa[vecino[0]][vecino[1]] == 2:
        return 4
    if tab.mapa[vecino[0]][vecino[1]] == 3:
        return 6







def astar(tab, filO, colO, filD, colD, heuristica, epsilon, verbose, camino):

    nodo_inicio = Nodo((filO, colO), 0, estimacion(filO, colO, filD, colD,heuristica),0)#inicializar el nodo de inicio
    frontera = [nodo_inicio]  # Lista de nodos frontera
    explorados = set()  # Conjunto de nodos explorados
    
    if verbose>0:
        print(f"Nodo inicio: {nodo_inicio.pos}, Destino: ({filD},{colD})")

    while frontera:
        
        if (epsilon>0):
            focal=construir_focal(frontera,epsilon) # Lista que contiene los datos filtrados por epsilon
                        # buscar el nodo con menor coste de calorías y si son iguales con menor f
            nodo_actual=min(focal, key=lambda n:( n.cal,n.f))
    
        if (epsilon==0):
            nodo_actual = min(frontera, key=lambda n: n.f)  # Nodo con menor costo total f
        frontera.remove(nodo_actual)
        if (verbose>0):
            print(f"Nodo que se usa para explorar :({nodo_actual.pos[0]},{nodo_actual.pos[1]})")#Nodos por los que va haciendo el camino

        if nodo_actual.pos == (filD, colD):  # Se encontró el destino
            for x,y in reconstruir_camino(nodo_actual):
                camino[x][y]='X'
            return nodo_actual.g,nodo_actual.cal, len(explorados)

        explorados.add(nodo_actual.pos)

        x, y = nodo_actual.pos
        
        for dx, dy in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]:#Todos los posibles movimientos desde una celda
            vecino_pos = (x + dx, y + dy)
            
            # Verificar si está dentro de los límites
            if not (0 <= vecino_pos[0] < tab.filas and 0 <= vecino_pos[1] < tab.columnas):
                continue
            
            # Verificar si es transitable
            if tab.mapa[vecino_pos[0]][vecino_pos[1]] == 0:
                if (verbose ==2):
                    print(f"El nodo({vecino_pos[0]},{vecino_pos[1]}) es intransitable")
                continue
            
            # Evitar nodos ya explorados
            if vecino_pos in explorados:
                if  verbose ==2:
                    print(f"El nodo ({vecino_pos[0]},{vecino_pos[1]}) ya ha sido explorado")
                continue  

            g_nuevo = coste(nodo_actual.pos,vecino_pos)+nodo_actual.g  # Coste g de movimiento v/d/h
            h_nuevo= estimacion(vecino_pos[0], vecino_pos[1], filD, colD,heuristica)#Calculo optimo
            if epsilon>0:
                cal_nuevo=nodo_actual.cal+calcular_cal(vecino_pos,tab)#Ahora se calculan la calorias
            else:
                cal_nuevo=0
            """Se crea el nodo vecino para almacenar su informacion explorada"""
            nodo_vecino = Nodo(vecino_pos, g_nuevo,h_nuevo,g_nuevo+h_nuevo,nodo_actual,cal_nuevo)
           
            if verbose==2:
                print(f"Explorando nodo vecino: {nodo_vecino.pos}, f:{nodo_vecino.f}.")
            if epsilon == 0:
                # Solo descartar si el nodo en la frontera tiene un mejor f 
                if any(n.pos == nodo_vecino.pos and n.f <= nodo_vecino.f for n in frontera):
                    continue
            elif epsilon > 0:
                # Si el nodo ya está en la frontera, lo descartamos si tiene mejores calorias y f
                if any(n.pos == nodo_vecino.pos and n.cal <= nodo_vecino.cal and n.f <= nodo_vecino.f for n in frontera):
                    continue

            frontera.append(nodo_vecino)
            if (verbose==2):
                print(f"Nodo vecino que entra en frontera :({nodo_vecino.pos[0]},{nodo_vecino.pos[1]}) ")#Nodos explorados y de los que se tiene info

    
    return -1, 0, len(explorados)  # No se puede llegar al destino

