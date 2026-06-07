import rsa
import os
import shutil

if __name__ == "__main__":
    nombre = input("Un nombre: ")
    try:
        valor_minimo = int(input("Introduce el valor mínimo de cada primo usado para generar sus claves de RSA: "))
        valor_maximo = int(input("Introduce el valor máximo de cada primo usado para generar sus claves de RSA: "))
        digitos_padding = int(input("Introduce el número de cifras de padding: "))
    except ValueError:
        print("Debes introducir un número.")
    n,e,d = rsa.generar_claves(valor_minimo, valor_maximo)
    fichero_publica = "pub_" + nombre
    fichero_privada = "priv_" + nombre 
    with open(fichero_publica, "w") as fichero:
        fichero.write(f"{n}\n")
        fichero.write(f"{e}\n")
        fichero.write(f"{digitos_padding}\n")
    with open(fichero_privada, "w") as fichero:
        fichero.write(f"{d}")
    
    carpeta = 'Usuarios'
    directorio = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(directorio, carpeta)
    if not os.path.exists(ruta):
        os.makedirs(ruta)
    shutil.move(os.path.join(directorio, fichero_publica), ruta)
    shutil.move(os.path.join(directorio, fichero_privada), ruta)