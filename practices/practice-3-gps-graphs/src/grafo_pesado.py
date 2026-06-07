"""
grafo.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP10A
Integrantes:
    - Miguel Gabaldón Poncela
    - Gonzalo García Martínez-Echevarría

Descripción:
Librería para el análisis de grafos pesados.
"""

from typing import List,Tuple,Dict,Callable,Union
import networkx as nx
import sys

import heapq #Librería para la creación de colas de prioridad

INFTY=sys.float_info.max #Distincia "infinita" entre nodos de un grafo

"""
En las siguientes funciones, las funciones de peso son funciones que reciben un grafo o digrafo y dos vértices y devuelven un real (su peso)
Por ejemplo, si las aristas del grafo contienen en sus datos un campo llamado 'valor', una posible función de peso sería:

def mi_peso(G:nx.Graph,u:object, v:object):
    return G[u][v]['valor']

y, en tal caso, para calcular Dijkstra con dicho parámetro haríamos

camino=dijkstra(G,mi_peso,origen, destino)


"""

def dijkstra(G:Union[nx.Graph, nx.DiGraph], peso:Union[Callable[[nx.Graph,object,object],float], Callable[[nx.DiGraph,object,object],float]], origen:object)-> Dict[object,object]:
    """ Calcula un Árbol de Caminos Mínimos para el grafo pesado partiendo
    del vértice "origen" usando el algoritmo de Dijkstra. Calcula únicamente
    el árbol de la componente conexa que contiene a "origen".
    
    Args:
        origen (object): vértice del grafo de origen
    Returns:
        Dict[object,object]: Devuelve un diccionario que indica, para cada vértice alcanzable
            desde "origen", qué vértice es su padre en el árbol de caminos mínimos.
    Raises:
        TypeError: Si origen no es "hashable".
    Example:
        Si G.dijksra(1)={2:1, 3:2, 4:1} entonces 1 es padre de 2 y de 4 y 2 es padre de 3.
        En particular, un camino mínimo desde 1 hasta 3 sería 1->2->3.
    """

    if not isinstance(origen, (str, int, tuple, frozenset)):
        raise TypeError("El vértice origen debe ser un tipo hashable.")
    
    padres = {}
    distancias = {nodo: float('inf') for nodo in G.nodes}
    distancias[origen] = 0
    heap = [(0, str(origen))]
    while heap:
        distancia_actual, nodo_actual = heapq.heappop(heap)
        nodo_actual = int(nodo_actual) if nodo_actual.isdigit() else nodo_actual
        if distancia_actual > distancias[nodo_actual]:
            continue
        for vecino in G.neighbors(nodo_actual):
            distancia_tentativa = distancia_actual + peso(G, nodo_actual, vecino)
            if distancia_tentativa < distancias[vecino]:
                distancias[vecino] = distancia_tentativa
                padres[vecino] = nodo_actual
                heapq.heappush(heap, (distancia_tentativa, str(vecino)))
    return padres



def camino_minimo(G:Union[nx.Graph, nx.DiGraph], peso:Union[Callable[[nx.Graph,object,object],float], Callable[[nx.DiGraph,object,object],float]] ,origen:object,destino:object)->List[object]:
    """ Calcula el camino mínimo desde el vértice origen hasta el vértice
    destino utilizando el algoritmo de Dijkstra.
    
    Args:
        G (nx.Graph o nx.Digraph): grafo a grado dirigido
        peso (función): función que recibe un grafo o grafo dirigido y dos vértices del mismo y devuelve el peso de la arista que los conecta
        origen (object): vértice del grafo de origen
        destino (object): vértice del grafo de destino
    Returns:
        List[object]: Devuelve una lista con los vértices del grafo por los que pasa
            el camino más corto entre el origen y el destino. El primer elemento de
            la lista es origen y el último destino.
    Example:
        Si dijksra(G,peso,1,4)=[1,5,2,4] entonces el camino más corto en G entre 1 y 4 es 1->5->2->4.
    Raises:
        TypeError: Si origen o destino no son "hashable".
    """
    padres = dijkstra(G, peso, origen)
    camino = []
    nodo = destino
    while nodo is not None:
        camino.append(nodo)
        nodo = padres.get(nodo)

    if camino[-1] != origen:
        raise ValueError("No hay camino entre el origen y el destino en el grafo.")
    
    return camino[::-1]


def prim(G:nx.Graph, peso:Callable[[nx.Graph,object,object],float])-> Dict[object,object]:
    """ Calcula un Árbol Abarcador Mínimo para el grafo pesado
    usando el algoritmo de Prim.
    
    Args: None
    Returns:
        G (nx.Graph): grafo
        peso (función): función que recibe un grafo y dos vértices del grafo y devuelve el peso de la arista que los conecta
        Dict[object,object]: Devuelve un diccionario que indica, para cada vértice del
            grafo, qué vértice es su padre en el árbol abarcador mínimo.
    Raises: None
    Example:
        Si prim(G,peso)={1: None, 2:1, 3:2, 4:1} entonces en un árbol abarcador mínimo tenemos que:
            1 es una raíz (no tiene padre)
            1 es padre de 2 y de 4
            2 es padre de 3
    """
    padre = {v: None for v in G.nodes}
    coste_minimo = {v: float('inf') for v in G.nodes}
    visitados = set()
    Q = []
    raiz = next(iter(G.nodes))
    coste_minimo[raiz] = 0
    heapq.heappush(Q, (0, str(raiz)))  # (peso, nodo)
    while Q:
        _, v = heapq.heappop(Q)
        v = int(v) if v.isdigit() else v
        if v in visitados:
            continue        
        visitados.add(v)
        for vecino in G.neighbors(v):
            peso_actual = float(peso(G, v, vecino))
            if vecino not in visitados and peso(G, v, vecino) < coste_minimo[vecino]:
                coste_minimo[vecino] = peso(G, v, vecino)
                padre[vecino] = v
                heapq.heappush(Q, (peso_actual, str(vecino)))
    return padre



def find(nodo, parent:dict):
    if parent[nodo] != nodo:
        parent[nodo] = find(parent[nodo], parent) 
    return parent[nodo]

def union(nodo1, nodo2, parent:dict, rank:dict):
    raiz1 = find(nodo1, parent)
    raiz2 = find(nodo2, parent)

    if raiz1 != raiz2:
        if rank[raiz1] > rank[raiz2]:
            parent[raiz2] = raiz1
        elif rank[raiz1] < rank[raiz2]:
            parent[raiz1] = raiz2
        else:
            parent[raiz2] = raiz1
            rank[raiz1] += 1
                

def kruskal(G:nx.Graph, peso:Callable[[nx.Graph,object,object],float])-> List[Tuple[object,object]]:
    """ Calcula un Árbol Abarcador Mínimo para el grafo
    usando el algoritmo de Kruskal.
    
    Args:
        G (nx.Graph): grafo
        peso (función): función que recibe un grafo y dos vértices del grafo y devuelve el peso de la arista que los conecta
    Returns:
        List[Tuple[object,object]]: Devuelve una lista [(s1,t1),(s2,t2),...,(sn,tn)]
            de los pares de vértices del grafo que forman las aristas
            del arbol abarcador mínimo.
    Raises: None
    Example:
        En el ejemplo anterior en que prim(G,peso)={1:None, 2:1, 3:2, 4:1} podríamos tener, por ejemplo,
        kruskal(G,peso)=[(1,2),(1,4),(3,2)]
    """
    aristas = [(u, v, peso(G, u, v)) for u, v in G.edges]
    
    aristas.sort(key=lambda x: x[2])
    parent = {}
    rank = {}
    for nodo in G.nodes:
        parent[nodo] = nodo
        rank[nodo] = 0
    mst = []
    for u, v, peso_arista in aristas:
        if find(u, parent) != find(v, parent):  
            mst.append((u, v)) 
            union(u, v, parent, rank)  
    return mst