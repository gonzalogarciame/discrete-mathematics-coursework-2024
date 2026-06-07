"""
modular.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP10A
Integrantes:
    - Gonzalo García Martínez-Echevarría
    - Miguel Gabaldón Poncela

Descripción:
Librería para la realización de cálculos y resolución de problemas de aritmética modular.
"""

from typing import Tuple, List, Dict

class IncompatibleEquationError(Exception):
    pass


""" Reciba un entero n y devuelva verdadero si es un número primo y falso en caso contrario

    Args:
        n (int): Entero
    
    Returns:
        true si el entero es un número primo.
        false en caso contrario.

    Raises: None
    
    Examples:
        es_primo(5)=true
        es_primo(4)=false
"""
import numpy as np
def es_primo(n:int)->bool:
    if n <= 1:
        return False   # 0 y 1 no son primos
    elif n <= 3:
        return True    # 2 y 3 son primos
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    limite = np.sqrt(n)   #Comprobamos todos los primos hasta raiz de n ya que solo puede haber un primo mayor que divida a 
    while i * i <= limite:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

""" Recibe dos enteros a y b y devuelva la lista de números primos en el intervalo [a, b)

    Args:
        a (int): Elemento inicial del intervalo (incluido)
        b (int): Elemento final del intervalo (no incluido)
    
    Returns:
        List[int]: lista ordenada de primos mayores o iguales que a y menores que b.

    Raises: None
    
    Examples:
        lista_primos(1,11)=[2,3,5,7]
"""

def lista_primos(a:int, b:int)->List[int]:
    if a <= 2:
        lista = [2]  #Comprobamos el 2 y luego empezamos por el 3
        a = 3  
    else:
        lista = []
        if a % 2 == 0:
            a += 1 
    for num in range(a, b, 2):  # Solo verificamos números impares ya que hemos comprobado el 2
        if es_primo(num):
            lista.append(num)
    return lista

""" Recibe  un entero n y devuelve un diccionario cuyas claves son los primos que dividen a n y sus valores los
correspondientes exponentes en la descomposición en producto de factores primos de n.
    Args:
        n (int): Entero que se desea factorizar.
    
    Returns:
        Dict[int,int]: Diccionario en el que las claves son primos positivos p_i que dividen a n y, para cada p_i,
            su valor asociado es el máximo exponente e_i tal que p_i^(e_i) divide a n. Si n=0, devuelve un diccionario vacío.

    Raises: None

    Examples
        factorizar(12)={2: 2, 3: 1}
        factorizar(0)={}
"""
import math

def factorizar(n: int) -> dict[int, int]:
    diccionario = {}
    # Miramos primero el número 2 para evitar comprobar todos los números pares
    if n<0:
        n = -n
    while n % 2 == 0:
        if 2 in diccionario:
            diccionario[2] += 1
        else:
            diccionario[2] = 1
        n //= 2
    # Buscamos los divisores impares desde 3 hasta raiz de n
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        while n % i == 0:
            if i in diccionario:
                diccionario[i] += 1
            else:
                diccionario[i] = 1
            n //= i
        if n == 1:
            return diccionario
    # n solo puede tener un divisor primo mayor que raiz de n
    if n > 1:
        diccionario[n] = 1
    return diccionario


""" Calcula el máximo común divisor de dos enteros a y b.
    Args:
        a (int): Primer entero.
        b (int): Segundo entero.
    
    Returns:
        int: devuelve el máximo común divisor de a y b

    Raises: None

    Examples
        mcd(10,15)=5
"""
def mcd(a:int,b:int)->int:
    while b != 0:
        a, b = b, a%b
    return a

""" Calcula el máximo común divisor d de dos enteros a y b junto con dos enteros x e y tales que
        d=ax+by

    Args:
        a (int): Primer entero.
        b (int): Segundo entero.
    
    Returns: (d,x,y)
        d (int): Máximo común divisor.
        x (int): Coeficiente de a.
        y (int): Coeficiente de b.

    Raises: None

    Examples
        bezout(6,10)=(2,2,-1)
"""
def bezout(n:int, m:int) -> Tuple[int,int,int]:
    if m == 0:
        return n, 1, 0
    mcd, x1, y1 = bezout(m, n % m)
    x = y1
    y = x1 - (n // m) * y1
    return mcd, x, y

""" Dada una lista de enteros, devuelve el máximo divisor común a todos ellos.
    Args:
        nList (List[int]): Lista de enteros.        
    
    Returns:
        int: devuelve el máximo entero que divide a todos los enteros de la lista.

    Raises: None

    Examples
        mcd([4,10,14])=2
"""
def mcd_n(nlist:List[int])->int:
    mcd_temp=mcd(nlist[0],nlist[1])
    for i in range(2,len(nlist)):
        mcd_temp=mcd(mcd_temp,nlist[i])
        print(mcd_temp)
    return mcd_temp

""" Dada una lista de enteros [a_1,...,a_n], devuelve el máximo divisor común d a todos ellos y una
lista de coeficientes [x_1,...,x_n] tal que
    d=a_1*x_1+...a_n*x_n

    Args:
        nList (List[int]): Lista de enteros.        
    
    Returns: (d,X)
        d (int): Máximo entero que divide a todos los enteros de la lista.
        X (List[int]): Lista de coeficientes [x_1,...,x_n].

    Raises: None

    Examples
        bezout_n([4,10,14])=(2,[-2,1,0])
"""
def bezout_n(nlist:List[int])->Tuple[int,List[int]]:
    #Opcional
    pass

""" Determina si dos enteros son coprimos.
    Args:
        a (int): Primer entero.
        b (int): Segundo entero.
    
    Returns:
        bool: Verdadero si son coprimos y falso si no.

    Raises: None

    Examples
        coprimos(14,20)=false
        coprimos(14,15)=true
"""
def coprimos(n:int,m:int)->bool:
    return mcd(n,m) == 1



""" Calcula la inversa de un número n módulo p.

    Args:
        n (int): Número que se desea invertir
        p (int): Módulo.
    
    Returns:
        int: Entero x entre 0 y p-1 tal que n*x es congruente con 1 módulo p.

    Raises:
        ZeroDivisionError: Si el módulo es 0 o si n no es invertible módulo p.
"""


def inversa_mod_p(n:int,p:int)->int:
    if not coprimos(n,p) or p == 0:
        raise ZeroDivisionError("NE")
    if n<0:
        n %= p
    coef_1 = 1
    coef_2 = -(p // n)  
    t1 = 0
    t2 = 1  
    resto = p % n  
    x = n
    y = resto
    cociente = 0  
    while resto != 0:
        cociente = x // y  
        resto = x % y  
        coef_1=coef_1*(-cociente) + t1
        coef_2=coef_2*(-cociente) + t2
        t1 = -(coef_1 - t1) // cociente
        t2 = -(coef_2 - t2) // cociente
        x = y
        y = resto
    if x == 1:  
        return t2 % p
    else:
        raise ZeroDivisionError("NE")

""" Calcula potencias módulo p.

    Args:
        base (int): Base de la potencia.
        exp (int): Exponente al que se eleva la base.
        p (int): Módulo.
    
    Returns:
        int: Resto de dividir base^exp módulo p.

    Raises:
        ZeroDivisionError: Si el módulo es 0.
"""

def potencia_mod_p(base:int, exp:int, p:int) -> int:
    if p == 0:
        raise ZeroDivisionError("NE")
    elif exp < 0:
        return potencia_mod_p(inversa_mod_p(base,p),-exp,p)
    resultado = 1   #Por defecto le damos el valor 1
    base %= p
    while exp > 0:
        if exp % 2 == 1:  # Si e es impar
            resultado = (resultado * base) % p
        exp //= 2  # Dividir e por 2
        base = base**2 % p  # Elevar base al cuadrado
    if exp < 0:  #Preguntar
        resultado = 0
    return resultado


""" Calcula la función phi de Euler de un entero positivo n, es decir, cuenta cúantos enteros positivos
menores que n son coprimos con n.

    Args:
        n (int): Número entero positivo.
    
    Returns:
        int: Función phi de Euler de n.

    Raises: None
"""

def euler(n: int) -> int:
    resultado = n
    if n % 2 == 0:  #  Primero comprobamos el 2 para quitar todos los pares
        resultado -= resultado // 2
        while n % 2 == 0:
            n //= 2
    for i in range(3, int(math.isqrt(n)) + 1, 2):   #Iteramos los números impares
        if n % i == 0:
            resultado -= resultado // i
            while n % i == 0:
                n //= i
    if n > 1:   #   El siguiente número mayor que 1 es un número primo divisor de n
        resultado -= resultado // n
    return resultado

""" Dado un entero n y un número primo p, calcula el símbolo de Legendre de n módulo p.

    Args:
        n (int): Número entero.
        p (int): Número primo.
    
    Returns:
        int: Símbolo de Legendre de Euler de n módulo p:
            0 si es múltiplo de p
            1 si es un cuadrado perfecto (distinto de 0), módulo p
            -1 en caso contrario.

    Raises:
        ZeroDivisionError: Si el módulo p es 0.
"""
def legendre(n: int, p: int) -> int:
    if p == 0:
        raise ZeroDivisionError("NE")
    if n % p == 0:
        return 0
    resultado = (potencia_mod_p(n, (p-1)//2, p))
    if resultado == (p-1):
        return -1
    else:
        return 1

""" Dadas tres listas de números enteros [a_1,...,a_n], [b_1,...,b_n] y [p_1,...,p_n], resuelve el sistema de congruencias
    
    a_i * x = b_i (mod p_i)   i=1,...,n
    
    devolviendo un entero r y un módulo m tales que las soluciones del sistema corresponden a todos los enteros
    x congruentes con r módulo m.

    Args:
        alist (List[int]): Lista de coeficientes de la variable x, [a_1,...,a_n].
        blist (List[int]): Lista de términos independientes [b_1,...,b_n].
        plist (List[int]): Lista de módulos [p_1,...,p_n]
    
    Returns: (r,m)
        r (int): Entero entre 0 y m-1.
        m (int): Entero positivo, módulo de la solución.

    Raises:
        IncompatibleEquationError: Si no es posible resolver el sistema.
"""
def resolver_sistema_congruencias(alist:List[int],blist:List[int],plist:List[int])->Tuple[int,int]:
    r, mod = 0, 1   # Inicializar resultado y módulo
    for a, b, p in zip(alist, blist, plist):   # Iterar sobre cada congruencia
        m_inverso = inversa_mod_p(mod, p)   # Calcular el inverso de m módulo p
        r = (r + (b - a * r) * m_inverso * mod) % (mod * p)   # Actualizar r usando el Teorema Chino del Resto
        mod *= p   # Actualizar el módulo
    return r, mod

""" Encuentra, si existe, una raíz cuadrada para un entero n módulo un número primo p.

    Args:
        n (int): Entero del que se desea hallar la raíz.
        p (int): Módulo. Se asume que es un número primo.
    
    Returns:
        int: Entero x entre 0 y p-1 tal que x^2 = n (mod p).

    Raises:
        IncompatibleEquationError: Si no es posible hallar dicha raíz.
"""
def raiz_mod_p(n:int,p:int)->int:
    #Opcional
    pass

""" Halla, si es posible, las dos posibles soluciones de la ecuación cuadrática ax^2+bx+c=0 (mod p).
Devuelve una tupla con las dos raíces (distintas o una misma raíz repetida en caso de ser doble).

    Args:
        a (int): Coeficiente de x^2.
        b (int): Coeficiente de x.
        c (int): Término independiente.
        p (int): Módulo. Se asume que es un número primo.
    
    Returns: (x1,x2)
        x1 (int): Primera solución. Entero entre 0 y p-1.
        x2 (int): Segunda solución. Entero entre 0 y p-1.

    Raises:
        IncompatibleEquationError: Si no es posible resolver la ecuación.
"""
def ecuacion_cuadratica(a:int,b:int,c:int,p:int)->Tuple[int,int]:
    #Opcional
    pass



