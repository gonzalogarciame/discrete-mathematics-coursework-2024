import osmnx as ox
import networkx as nx
from callejero import *
from grafo_pesado import camino_minimo
import math

MARGEN = 3

def obtener_limite_velocidad(arista):
    """
    Obtiene el límite de velocidad asociado a una arista.

    Args:
        arista (dict): Datos de la arista, incluyendo posibles atributos
                       como 'maxspeed' o 'highway'.

    Returns:
        float: Límite de velocidad en km/h. Si no se encuentra un límite explícito,
               se asume un valor por defecto de 50 km/h.
    """
    # Verificar si la arista tiene un atributo 'maxspeed'
    if 'maxspeed' in arista:
        maxspeed = arista['maxspeed']  # Obtener el límite de velocidad
        if isinstance(maxspeed, list):  # Si es una lista, tomar el primer elemento
            maxspeed = maxspeed[0]
        try:
            limite_velocidad = float(maxspeed)  # Intentar convertir el límite a número
            return limite_velocidad
        except ValueError:
            # Si la conversión falla, buscar números dentro del texto
            coincidencia = re.search(r'(\d+)', str(maxspeed))
            if coincidencia:
                limite_velocidad = float(coincidencia.group(1))
                return limite_velocidad
    
    # Verificar si la arista tiene un atributo 'highway'
    if 'highway' in arista:
        tipo_carretera = arista['highway']  # Obtener el tipo de carretera
        if isinstance(tipo_carretera, list):  # Si es una lista, tomar el primer elemento
            tipo_carretera = tipo_carretera[0]
        velocidad_cadena = MAX_SPEEDS.get(tipo_carretera, '50')  # Buscar el límite en el diccionario por defecto
        try:
            limite_velocidad = float(velocidad_cadena)  # Intentar convertir el valor a número
            return limite_velocidad
        except ValueError:
            pass
    
    # Si no se encuentra un límite válido, devolver el valor por defecto
    return 50.0


def vertice_mas_cercano(G: nx.DiGraph, lat: float, lon: float):
    """
    Encuentra el nodo del grafo más cercano a unas coordenadas específicas.

    Args:
        G (nx.DiGraph): Grafo dirigido que representa las calles.
        lat (float): Latitud de las coordenadas de interés.
        lon (float): Longitud de las coordenadas de interés.

    Returns:
        object: Nodo del grafo más cercano a las coordenadas dadas.

    Utiliza la función `ox.distance.nearest_nodes` para calcular el nodo
    más cercano en el grafo a las coordenadas proporcionadas.
    """
    return ox.distance.nearest_nodes(G, lon, lat)


def calcular_ruta(G: nx.DiGraph, origen, destino, modo: str):
    """
    Calcula la ruta óptima entre dos nodos en el grafo según el modo seleccionado.

    Args:
        G (nx.DiGraph): Grafo dirigido que representa las calles.
        origen: Nodo de inicio para el cálculo de la ruta.
        destino: Nodo final para el cálculo de la ruta.
        modo (str): Modo de cálculo de la ruta. Puede ser:
                    - "corta" o "1" para la ruta más corta en distancia.
                    - "rapida" o "2" para la ruta más rápida en tiempo.
                    - "optimizada" o "3" para una ruta considerando penalización de semáforos.

    Returns:
        list: Lista de nodos que representan la ruta calculada.

    Raises:
        ValueError: Si el modo no es válido.

    La función selecciona la función de peso adecuada según el modo
    y calcula la ruta utilizando `camino_minimo`.
    """
    if modo == "corta" or modo == "1":
        # Ruta más corta basada en la longitud de las calles.
        peso = lambda G, u, v: G[u][v].get('length', 1)
    elif modo == "rapida" or modo == "2":
        # Ruta más rápida basada en la velocidad máxima de las calles.
        peso = lambda G, u, v: G[u][v].get('length', 1) / int(G[u][v].get('speed_limit', "50"))
    elif modo == "optimizada" or modo == "3":
        # Ruta optimizada considerando penalización de semáforos.
        peso = lambda G, u, v: (G[u][v].get('length', 1) / int(G[u][v].get('speed_limit', "50"))) + 30 * 0.8
    else:
        raise ValueError("Modo de ruta no válido. Debes introducir: corta, rapida u optimizada.")

    return camino_minimo(G, peso, origen, destino)



def generar_instrucciones(G: nx.DiGraph, camino: list) -> list:
    """
    Genera las instrucciones de navegación para una ruta específica.

    Args:
        G (nx.DiGraph): Grafo dirigido que representa las calles.
        camino (list): Lista de nodos que representan la ruta a seguir.

    Returns:
        list: Lista de instrucciones de navegación en formato textual.

    La función genera instrucciones detalladas para cada segmento de la
    ruta, incluyendo:
    - Nombre de las calles.
    - Distancias a recorrer.
    - Giros a izquierda o derecha en intersecciones.
    """
    instrucciones = []
    # Obtener datos de la primera arista.
    arista_inicial = G[camino[0]][camino[1]]
    tupla_vector_inicial = (G.nodes[camino[0]]['y'] - G.nodes[camino[1]]['y'], G.nodes[camino[0]]['x'] - G.nodes[camino[1]]['x'])
    nombre_inicial = arista_inicial['name']
    longitud_total = arista_inicial['length']
    instrucciones.append(f'Dirígete hacia {nombre_inicial}.')

    # Iterar sobre los segmentos de la ruta para calcular instrucciones.
    for i in range(len(camino) - 2):
        # Datos del siguiente segmento.
        arista_siguiente = G[camino[i + 1]][camino[i + 2]]
        tupla_vector_siguiente = (G.nodes[camino[i + 1]]['y'] - G.nodes[camino[i + 2]]['y'], G.nodes[camino[i + 1]]['x'] - G.nodes[camino[i + 2]]['x'])
        nombre_siguiente = arista_siguiente['name']

        # Calcular el ángulo entre los vectores del segmento actual y el siguiente.
        producto_escalar = tupla_vector_inicial[0] * tupla_vector_siguiente[0] + tupla_vector_inicial[1] * tupla_vector_siguiente[1]
        magnitud_inicial = math.sqrt(tupla_vector_inicial[0]**2 + tupla_vector_inicial[1]**2)
        magnitud_siguiente = math.sqrt(tupla_vector_siguiente[0]**2 + tupla_vector_siguiente[1]**2)
        angulo_radianes = math.acos(producto_escalar / (magnitud_inicial * magnitud_siguiente))
        angulo = angulo_radianes * (180 / math.pi)

        # Determinante para calcular la dirección del giro.
        determinante = tupla_vector_inicial[0] * tupla_vector_siguiente[1] - tupla_vector_inicial[1] * tupla_vector_siguiente[0]

        # Decidir si hay un giro o si se continúa en línea recta.
        if angulo < MARGEN:
            giro = None
        elif determinante < 0:
            giro = 'izquierda'
        else:
            giro = 'derecha'

        # Generar instrucciones según el cambio de calle o la continuidad.
        if nombre_inicial != nombre_siguiente:
            if giro:
                instruccion = f'Después de avanzar {round(longitud_total)} metros, gira a la {giro} en {nombre_siguiente}.'
            else:
                instruccion = f'Tras avanzar {round(longitud_total)} metros, sigue por {nombre_siguiente}.'
            instrucciones.append(instruccion)
            longitud_total = arista_siguiente['length']
        else:
            longitud_total += arista_siguiente['length']

        # Actualizar el vector inicial y el nombre de la calle.
        tupla_vector_inicial = tupla_vector_siguiente
        nombre_inicial = nombre_siguiente
    instrucciones.append("Llegaste a tu destino")
    return instrucciones



if __name__ == "__main__":
    df_direcciones = carga_callejero()
    G_sin_procesar = carga_grafo()
    G = procesa_grafo(G_sin_procesar)
    for u, v, arista in G.edges(data=True):
        limite_velocidad = obtener_limite_velocidad(arista)
        arista['speed_limit'] = limite_velocidad
    while True:
        origen = input("Introduce la dirección de origen: ")
        destino = input("Introduce la dirección de destino: ")
        try:
            latitud_origen, longitud_origen = busca_direccion(origen, df_direcciones)
            latitud_destino, longitud_destino = busca_direccion(destino, df_direcciones)
        except ValueError as e:
            print(e)
            continue
        origen = vertice_mas_cercano(G, latitud_origen, longitud_origen)
        destino = vertice_mas_cercano(G, latitud_destino, longitud_destino)
        print("Modos de cálculo de ruta:")
        print("1. Más corta\n2. Más rápida\n3. Optimizada (semaforización) \n[1-(corta)/2-(rapida)/3-(optimizada)]")
        modo = input("Deberás elegir entre: corta, rapida u optimizada. ")
        try:
            camino = calcular_ruta(G, origen, destino, modo)
        except ValueError as e:
            print(e)
            continue
        instrucciones = generar_instrucciones(G, camino)
        for instr in instrucciones:
            print(instr)
        mostrar_grafo(G, camino)
