"""
callejero.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP10A
Integrantes:
    - Miguel Gabaldón Poncela
    - Gonzalo García Martínez-Echevarría

Descripción:
Librería con herramientas y clases auxiliares necesarias para la representación de un callejero en un grafo.

Complétese esta descripción según las funcionalidades agregadas por el grupo.
"""
import os
import osmnx as ox
import networkx as nx
import pandas as pd
import re
from typing import Tuple

import matplotlib.pyplot as plt

STREET_FILE_NAME="direcciones.csv"

PLACE_NAME = "Madrid, Spain"
MAP_FILE_NAME="madrid.graphml"

MAX_SPEEDS={'living_street': '20',
 'residential': '30',
 'primary_link': '40',
 'unclassified': '40',
 'secondary_link': '40',
 'trunk_link': '40',
 'secondary': '50',
 'tertiary': '50',
 'primary': '50',
 'trunk': '50',
 'tertiary_link':'50',
 'busway': '50',
 'motorway_link': '70',
 'motorway': '100'}


class ServiceNotAvailableError(Exception):
    "Excepción que indica que la navegación no está disponible en este momento"
    pass


class AdressNotFoundError(Exception):
    "Excepción que indica que una dirección buscada no existe en la base de datos"
    pass


############## Parte 2 ##############

def conversor_coordenadas(coord:str):
    match = re.match(r"(\d+)[°º]\s*(\d+)'?\s*(\d+(\.\d+)?)(?:''?|\"?)?\s*([NSEW])", coord)
    if match:
        degrees, minutes, seconds, _, direction = match.groups()
        decimal_degrees = float(degrees) + float(minutes) / 60 + float(seconds) / 3600
        if direction in ['S', 'W']:
            decimal_degrees *= -1
        return decimal_degrees
    return None

def carga_callejero() -> pd.DataFrame:
    """ Función que carga el callejero de Madrid, lo procesa y devuelve
    un DataFrame con los datos procesados
    
    Args: None
    Returns:
        Dict[object,object]: Devuelve un diccionario que indica, para cada vértice del
            grafo, qué vértice es su padre en el árbol abarcador mínimo.
    Raises:
        FileNotFoundError si el fichero csv con las direcciones no existe
    """
    callejero = pd.read_csv(STREET_FILE_NAME,delimiter=";",encoding='latin1')
    callejero = callejero[["VIA_CLASE", "VIA_PAR", "VIA_NOMBRE", "NUMERO", "LATITUD", "LONGITUD"]]

    callejero = callejero.dropna(subset=['LATITUD', 'LONGITUD'])


    callejero['LATITUD'] = callejero['LATITUD'].apply(conversor_coordenadas)
    callejero['LONGITUD'] = callejero['LONGITUD'].apply(conversor_coordenadas)


    return callejero

def busca_direccion(direccion:str, callejero:pd.DataFrame) -> Tuple[float,float]:
    """ Función que busca una dirección, dada en el formato
        calle, numero
    en el DataFrame callejero de Madrid y devuelve el par (latitud, longitud) en grados de la
    hubicación geográfica de dicha dirección
    
    Args:
        direccion (str): Nombre completo de la calle con número, en formato "Calle, num"
        callejero (DataFrame): DataFrame con la información de las calles
    Returns:
        Tuple[float,float]: Par de float (latitud,longitud) de la dirección buscada, expresados en grados
    Raises:
        AdressNotFoundError: Si la dirección no existe en la base de datos
    Example:
        busca_direccion("Calle de Alberto Aguilera, 23", data)=(40.42998055555555,3.7112583333333333)
        busca_direccion("Calle de Alberto Aguilera, 25", data)=(40.43013055555555,3.7126916666666667)
    """

    callejero_buscar = callejero[["VIA_NOMBRE","NUMERO","LATITUD","LONGITUD"]]
    partes = direccion.split(',')
    via_nombre = partes[0].strip()
    numero = partes[1].strip()
    via_nombre_limpio = ""
    via_nombre = via_nombre.split(" ")
    via_nombre = via_nombre[::-1]
    for palabra in via_nombre:
        via_nombre_limpio = palabra.lower() + " " + via_nombre_limpio
        via_nombre_limpio.strip()
        resultado = callejero_buscar[
            (callejero_buscar['VIA_NOMBRE'].str.lower() == via_nombre_limpio.strip()) &
            (callejero_buscar['NUMERO'].astype(str) == numero.strip())
        ]
        if not resultado.empty:
            latitud = resultado.iloc[0]['LATITUD']
            longitud = resultado.iloc[0]['LONGITUD']
            return latitud, longitud
    raise ValueError("La dirección no se encontró en el dataset.")


############## Parte 4 ##############

class ServiceNotAvailableError(Exception):
    pass

def mostrar_grafo(G:nx.MultiDiGraph, ruta=None)-> None:
    plt.plot()
    posicion = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}
    nx.draw_networkx_nodes(G, pos=posicion, node_size=0.5, node_color='black')
    nx.draw_networkx_edges(G, pos=posicion, arrowstyle='->', arrowsize=5, edge_color='gray', width=0.2)
    if ruta:
        edges_in_route = list(zip(ruta, ruta[1:]))
        nx.draw_networkx_edges(G, pos=posicion, edgelist=edges_in_route, edge_color='red', width=1.5, alpha=0.8)
        nx.draw_networkx_nodes(G, pos=posicion, nodelist=ruta, node_size=10, node_color='red', alpha=0.8)
    plt.show()
    return None


def procesa_grafo(multidigrafo:nx.MultiDiGraph) -> nx.DiGraph:
    """ Función que recupera el quiver de calles de Madrid de OpenStreetMap.
    Args:
        multidigrafo: multidigrafo de las calles de Madrid obtenido de OpenStreetMap.
    Returns:
        nx.DiGraph: Grafo dirigido y sin bucles asociado al multidigrafo dado.
    Raises: None
    """
    digrafo =  ox.utils_graph.convert.to_digraph(multidigrafo)
    bucles = list(nx.selfloop_edges(digrafo))
    digrafo.remove_edges_from(bucles)    
    return digrafo

def carga_grafo() -> nx.MultiDiGraph:
    """ Función que recupera el quiver de calles de Madrid de OpenStreetMap.
    Args: None
    Returns:
        nx.MultiDiGraph: Quiver de las calles de Madrid.
    Raises:
        ServiceNotAvailableError: Si no es posible recuperar el grafo de OpenStreetMap.
    """
    if os.path.exists(MAP_FILE_NAME):
        G = ox.load_graphml(MAP_FILE_NAME)
    else:
        try:
            G = ox.graph_from_place(PLACE_NAME, network_type="drive")
            ox.save_graphml(G, MAP_FILE_NAME)
        except Exception:
            raise ServiceNotAvailableError("No se puede recuperar el grafo de OpenStreetMap.")
    return G
    
if __name__ == "__main__":
    mostrar_grafo(procesa_grafo(carga_grafo()))
