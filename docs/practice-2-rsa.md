# Practice 2: RSA, Key Generation, and Attacks

## Original Goal

The second practice extended the modular arithmetic work into cryptography. The assignment focused on implementing RSA key generation, encryption and decryption, user key files, a simple chat-like interface, and attacks against weak RSA configurations.

Original report: `practices/practice-2-rsa/report/P2GP10A.docx`

Source code:

- `practices/practice-2-rsa/src/modular.py`
- `practices/practice-2-rsa/src/rsa.py`
- `practices/practice-2-rsa/src/registrarusuario.py`
- `practices/practice-2-rsa/src/criptochat.py`

## What Was Implemented

### `rsa.py`

This is the main RSA library. It includes:

- `generar_claves(min_primo, max_primo)`: chooses two primes, computes `n`, selects a public exponent `e`, and computes the private exponent `d`.
- `aplicar_padding(m, digitos_padding)`: appends random decimal digits to the message.
- `eliminar_padding(m, digitos_padding)`: removes the padding digits.
- `cifrar_rsa(m, n, e, digitos_padding)`: pads and encrypts an integer message.
- `descifrar_rsa(c, n, d, digitos_padding)`: decrypts and removes padding.
- `codificar_cadena(s)`: converts a string into Unicode code points.
- `decodificar_cadena(m)`: converts Unicode code points back into text.
- `cifrar_cadena_rsa(s, n, e, digitos_padding)`: encrypts a string character by character.
- `descifrar_cadena_rsa(cList, n, d, digitos_padding)`: decrypts a list of encrypted character values.
- `romper_clave(n, e)`: recovers the private exponent when `phi(n)` can be computed.
- `ataque_texto_elegido(cList, n, e)`: performs a dictionary-style chosen-plaintext attack against RSA without padding.

### `registrarusuario.py`

This script creates key files for a user:

- `pub_<usuario>` stores `n`, `e`, and the number of padding digits.
- `priv_<usuario>` stores `d`.

The files are moved into a `Usuarios` directory.

### `criptochat.py`

This script loads one user's private key and another user's public key. It then allows the user to:

- encrypt a message with the recipient's public key;
- decrypt a message with the local private key;
- exit the program.

## Mathematical Ideas

RSA is based on modular exponentiation and the difficulty of factoring a large product of two primes.

The key steps are:

1. Choose two primes `p` and `q`.
2. Compute `n = p * q`.
3. Compute `phi(n) = (p - 1)(q - 1)`.
4. Choose `e` coprime with `phi(n)`.
5. Compute `d`, the modular inverse of `e` modulo `phi(n)`.
6. Encrypt with `c = m^e mod n`.
7. Decrypt with `m = c^d mod n`.

The practice also shows why textbook RSA is fragile:

- Small primes make `n` factorable.
- Without secure padding, repeated plaintexts encrypt predictably.
- A chosen-plaintext dictionary can recover messages when the plaintext alphabet is small.

## Recovered Plaintext

According to the report, the recovered plaintext from the presencial exercise was:

```text
Yo he visto cosas que vosotros no creeriais. Atacar naves en llamas mas alla de Orion. He visto rayos-C brillar en la oscuridad cerca de la Puerta de Tannhauser. Todos esos momentos se perderan en el tiempo, como lagrimas en la lluvia.
```

The original report contains the accented version.

## How To Run

From the practice source folder:

```bash
cd practices/practice-2-rsa/src
python registrarusuario.py
python criptochat.py alice bob
```

You can also call the library directly from Python:

```python
import rsa

n, e, d = rsa.generar_claves(100, 500)
cipher = rsa.cifrar_cadena_rsa("Hola", n, e, 2)
plain = rsa.descifrar_cadena_rsa(cipher, n, d, 2)
```

## Implementation Notes

This implementation is useful for learning RSA, but it is not production cryptography. Real systems require cryptographically secure randomness, large primes, standardized padding such as OAEP, authenticated encryption patterns, and careful side-channel protections.
