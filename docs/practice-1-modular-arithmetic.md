# Practice 1: Modular Arithmetic and IMAT-LAB

## Original Goal

The first practice asked for a modular arithmetic toolkit and a command-driven interface named IMAT-LAB. The work combines number theory algorithms with a small parser capable of receiving commands from standard input, command-line arguments, or batch files.

Original report: `practices/practice-1-modular-arithmetic/report/P1GP10A.pdf`

Source code:

- `practices/practice-1-modular-arithmetic/src/modular.py`
- `practices/practice-1-modular-arithmetic/src/imatlab.py`
- `practices/practice-1-modular-arithmetic/src/imatlab_benchmark.py`

## What Was Implemented

### `modular.py`

This file contains the main mathematical library:

- `es_primo(n)`: checks whether an integer is prime.
- `lista_primos(a, b)`: returns primes in the interval `[a, b)`.
- `factorizar(n)`: decomposes an integer into prime factors and exponents.
- `mcd(a, b)`: computes the greatest common divisor with Euclid's algorithm.
- `bezout(n, m)`: computes the gcd and Bezout coefficients using the extended Euclidean algorithm.
- `mcd_n(nlist)`: computes the gcd of a list of integers.
- `coprimos(n, m)`: checks whether two integers are coprime.
- `inversa_mod_p(n, p)`: computes the modular inverse when it exists.
- `potencia_mod_p(base, exp, p)`: computes modular powers using binary exponentiation.
- `euler(n)`: computes Euler's totient function.
- `legendre(n, p)`: computes the Legendre symbol modulo a prime.
- `resolver_sistema_congruencias(alist, blist, plist)`: solves systems of linear congruences using a Chinese Remainder Theorem style construction.

Some optional functions were left as placeholders:

- `bezout_n`
- `raiz_mod_p`
- `ecuacion_cuadratica`

### `imatlab.py`

This file provides an interface over `modular.py`.

It supports commands such as:

```text
primo(17)
factorizar(84)
coprimos(14,15)
mcd(48,18)
pow(2,10,7)
inv(3,11)
euler(36)
resolverSistema([1;2;5],[1;3;7])
```

The implementation uses regular expressions to recognize valid commands. Unknown or malformed commands are answered with `NOP`.

It also supports direct command-line execution, for example:

```bash
python imatlab.py primo 17
python imatlab.py mcd 48 18
python imatlab.py pow 2 10 7
python imatlab.py input.txt output.txt
```

### `imatlab_benchmark.py`

This script measures execution time and optionally profiles IMAT-LAB over predefined input files. The benchmark input files referenced in the script were not included in the original folder.

## Mathematical Ideas

The practice is centered on core tools from elementary number theory:

- Prime checking only needs to test possible divisors up to the square root of the number.
- Prime factorization relies on the Fundamental Theorem of Arithmetic.
- Euclid's algorithm repeatedly replaces `(a, b)` with `(b, a mod b)` until the remainder is zero.
- Bezout's identity states that the gcd of two integers can be written as an integer linear combination of them.
- A modular inverse exists exactly when the number and the modulus are coprime.
- Binary exponentiation reduces the cost of computing large powers modulo `p`.
- Euler's phi function counts positive integers smaller than `n` that are coprime to `n`.
- The Legendre symbol identifies whether a number is a quadratic residue modulo an odd prime.
- Systems of congruences are combined using the Chinese Remainder Theorem when the necessary compatibility conditions hold.

## How To Run

From the practice source folder:

```bash
cd practices/practice-1-modular-arithmetic/src
python imatlab.py primo 17
python imatlab.py factorizar 360
python imatlab.py inv 3 11
```

For batch mode:

```bash
python imatlab.py input.txt output.txt
```

## Implementation Notes

The report explains the intended algorithms and their mathematical justification. The submitted code preserves the original coursework style, including Spanish comments and some optional unfinished functions.
