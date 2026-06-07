# Discrete Mathematics Coursework

Structured repository for three Discrete Mathematics practices completed on **1 December 2024** by group **GP10A**:

- Gonzalo Garcia Martinez-Echevarria
- Miguel Gabaldon Poncela

The repository keeps the original submitted reports and source code, while adding clear documentation about what each task asked for, what was implemented, and how the mathematical ideas connect to the programs.

## Repository Structure

```text
.
|-- docs/
|   |-- practice-1-modular-arithmetic.md
|   |-- practice-2-rsa.md
|   `-- practice-3-gps-graphs.md
|-- practices/
|   |-- practice-1-modular-arithmetic/
|   |   |-- report/
|   |   `-- src/
|   |-- practice-2-rsa/
|   |   |-- report/
|   |   `-- src/
|   `-- practice-3-gps-graphs/
|       |-- report/
|       `-- src/
|-- requirements.txt
`-- README.md
```

## Practices

### Practice 1: Modular Arithmetic and IMAT-LAB

Implements a modular arithmetic library and a small command interface. It covers primality, factorization, gcd, Bezout coefficients, modular inverses, modular exponentiation, Euler phi, Legendre symbol, and systems of congruences.

Read more: [docs/practice-1-modular-arithmetic.md](docs/practice-1-modular-arithmetic.md)

### Practice 2: RSA, Key Generation, and Attacks

Builds on the modular arithmetic library to implement RSA key generation, padding, encryption/decryption for integers and strings, key recovery for weak keys, and a chosen-plaintext attack against RSA without padding.

Read more: [docs/practice-2-rsa.md](docs/practice-2-rsa.md)

### Practice 3: Graph Algorithms and GPS Routing

Implements weighted graph algorithms and applies them to a Madrid street-routing prototype using NetworkX, OSMnx, and address data. It includes Dijkstra, Prim, Kruskal, street graph processing, route calculation, and navigation instructions.

Read more: [docs/practice-3-gps-graphs.md](docs/practice-3-gps-graphs.md)

## Setup

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
python -m pip install -r requirements.txt
```

Some scripts depend on external files that were not present in the original folder, such as benchmark input files for Practice 1 or `direcciones.csv` for Practice 3.

## Notes

The source code is preserved as academic coursework. The documentation explains both the intended mathematical method and practical details noticed in the submitted implementation.
