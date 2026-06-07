import sys
import os
from rsa import *

def comprobar_existencia_fichero(fichero:str):
    if os.path.exists(fichero):
        pass
    else:
        raise Exception(f"El fichero del usuario {fichero[6:]} no existe")

def leer_claves_publicas(fichero_publico:str)->tuple[int,int,int]:
    try:
        with open(fichero_publico, "r") as fichero:
            n = int(fichero.readline())
            e = int(fichero.readline())
            digitos_padding = int(fichero.readline())
    except ValueError:
        raise Exception(f"Los valores del fichero {fichero_publico} deben ser enteros.")    
    return n, e, digitos_padding

if __name__ == "__main__":
    try:
        usuario_1 = sys.argv[1]
        usuario_2 = sys.argv[2]
    except IndexError:
        print("El formato por máquina debe ser: <usuario1> <usuario2>")
    nombre_archivo_privado_usuario_1 = f"priv_{usuario_1}"
    nombre_archivo_publico_usuario_1 = f"pub_{usuario_1}"
    nombre_archivo_publico_usuario_2 = f"pub_{usuario_2}" 
    try:
        comprobar_existencia_fichero(nombre_archivo_privado_usuario_1)
        comprobar_existencia_fichero(nombre_archivo_publico_usuario_1)
        comprobar_existencia_fichero(nombre_archivo_publico_usuario_2)
    except Exception as error:
        print(error)

    n_1, e_1, digitos_padding_1 = leer_claves_publicas(nombre_archivo_publico_usuario_1)
    n_2, e_2, digitos_padding_2 = leer_claves_publicas(nombre_archivo_publico_usuario_2)

    with open(nombre_archivo_privado_usuario_1, "r") as fichero:
        d_1 = int(fichero.readline())
    opcion = ""
    while opcion.upper() != "S":
        opcion = input("Elige entre: cifrar(C), descifrar(D) o salir(S). ")
        if opcion.upper() == "C":
            texto = input("Introduzca el texto a cifrar: ")
            mensaje_cifrado = cifrar_cadena_rsa(texto,n_2,e_2,digitos_padding_2)
            print(mensaje_cifrado)
        elif opcion.upper() == "D":
            texto_cifrado = input("Introduzca el texto a descifrar: ")
            texto_cifrado = texto_cifrado.split(" ")
            numeros_cifrado_limpio=[]
            for num in texto_cifrado:
                numeros_cifrado_limpio.append(int(num))
            print(numeros_cifrado_limpio)
            mensaje_descifrado = descifrar_cadena_rsa(numeros_cifrado_limpio, n_1, d_1, digitos_padding_1)
            print(mensaje_descifrado)
        else:
            print("Debes elegir entre C (cifrar), D (descifrar) o S (salir).")

    print("Se ha terminado el programa.")