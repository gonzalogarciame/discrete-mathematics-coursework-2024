"""
imatlab.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP10A
Integrantes:
    - Gonzalo García Martínez-Echevarría
    - Miguel Gabaldón Poncela

Descripción:
Sistema interactivo IMAT-LAB de resolución de ecuaciones en aritmética modular.

Interfaz de acceso interactivo o por lotes a la librería modular.py. Si este script se ejecuta sin par´ametros,
lanzar´a la interfaz de usuario para el modo interactivo.
"""

from typing import TextIO
from modular import *
import re

""" Recibe un manejador fin de un fichero de texto ya abierto para lectura y otro de un fichero de salida
ya abierto para escritura y ejecuta línea por línea los comandos proporcionados por fin, escribiendo los resultados en fout. Si
fin y fout no corresponden con la entrada y salida esáandar, esta función ejecuta el modo de procesamiento
por lotes de IMAT-LAB para la entrada fin, guardando el resultado en el fichero fout.

    Args:
        fin (TextIO): Fichero de entrada. Manejador de un fichero de texto ya abierto para lectura.
        fout (TextIO): Fichero de salida. Manejador de un fichero de texto ya abierto para escritura.
    
    Returns: None
    
    Raises: None
    
    Examples:
        run_commands(sys.stdin,sys.stdout) lanza el modo interactivo y ejecuta línea por línea los comandos que
            el usuario lanza desde la entrada estándar.
"""
def run_commands(fin:TextIO,fout:TextIO):
    for linea in fin:
        match = re.match(r'(primo)\((-?\d+)\)|(factorizar)\((-?\d+)\)|(coprimos)\((-?\d+),(-?\d+)\)|(mcd)\((-?\d+),(-?\d+)\)|(pow)\((-?\d+),(-?\d+),(-?\d+)\)|(inv)\((-?\d+),(-?\d+)\)|(euler)\((\d+)\)|(resolverSistema)\((\[-?\d+;-?\d+;-?\d+\](,\[-?\d+;-?\d+;-?\d+\])*)\)', linea.strip())
        if match:
            if match.group(1) == "primo":
                resultado = es_primo(int(match.group(2)))
            elif match.group(3) == "factorizar":
                resultado = factorizar(int(match.group(4)))
            elif match.group(5) == "coprimos":
                resultado = coprimos(int(match.group(6)), int(match.group(7)))
            elif match.group(8) == "mcd":
                resultado = mcd(int(match.group(9)), int(match.group(10)))
            elif match.group(11) == "pow":
                try:
                    resultado = potencia_mod_p(int(match.group(12)), int(match.group(13)), int(match.group(14)))
                except ZeroDivisionError as error:
                    resultado = error
            elif match.group(15) == "inv":
                try:
                    resultado = inversa_mod_p(int(match.group(16)), int(match.group(17)))
                except ZeroDivisionError as error:
                    resultado = error
            elif match.group(18) == "euler":
                resultado = euler(int(match.group(19)))
            elif match.group(20) == "resolverSistema":
                argumentos = match.group(21)
                lista_argumentos = []
                alist = []
                blist = []
                plist = []
                for arg in argumentos.split(","):
                    arg=arg.strip("[]")
                    elementos = arg.split(";")
                    alist.append(int(elementos[0]))
                    blist.append(int(elementos[1]))
                    plist.append(int(elementos[2]))
                    lista_argumentos.append(alist)
                    lista_argumentos.append(blist)
                    lista_argumentos.append(plist)
                try:
                    resultado = resolver_sistema_congruencias(alist, blist, plist)
                except Exception as error:
                    resultado = error
            fout.write(f"{resultado}\n")
        else:
            fout.write(f"NOP\n")

import sys
if __name__ == "__main__":
    lista = sys.argv
    try:

        funcion = lista[1]
        lista_funciones_1 = ["primo", "primos",  "factorizar", "euler"]
        lista_funciones_2 = ["coprimos", "mcd", "inv", "legendre"]
        lista_funciones_3 = ["pow"]
        numero1 = int(lista[2])
        if funcion.lower() in lista_funciones_1 and len(lista) == 3:
            if funcion.lower() == "primo":
                resultado = es_primo(numero1)
            elif funcion.lower() == "factorizar":
                resultado = factorizar(numero1)
            else:
                resultado = euler(numero1)
        elif len(sys.argv) == 3:   #Ejecución por lotes por máquina
            input_file = lista[1]
            output_file = lista[2]
            with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
                run_commands(fin, fout)
        elif funcion.lower() in lista_funciones_2 and len(lista) == 4:
            numero2 = int(lista[3])
            if funcion.lower() == "coprimos":
                resultado = coprimos(numero1,numero2)
            elif funcion.lower() == "mcd":
                resultado = mcd(numero1, numero2)
            elif funcion.lower() == "primos":
                resultado = lista_primos(numero1, numero2)
            elif funcion.lower() == "legendre":
                try:
                    resultado = legendre(numero1, numero2)
                except ZeroDivisionError as error:
                    resultado = error
            else:
                try:
                    resultado = inversa_mod_p(numero1, numero2)
                except ZeroDivisionError as error:
                    resultado = error
        elif funcion.lower() in lista_funciones_3 and len(lista) == 5:
            numero2 = int(lista[3])
            numero3 = int(lista[4])
            try:
                resultado = potencia_mod_p(numero1, numero2, numero3)
            except ZeroDivisionError as error:
                resultado = error
        print(resultado)
    except Exception:
        print("NOP")
