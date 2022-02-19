#!/usr/bin/env python3

"""
Quantum algorithm to validate an ISBN / EAN13 checkdigit
using only a single qubit.

Copyright (c) 2022 Charles Horn.

"""

import matplotlib.pyplot as plt
import sys
from math import pi
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister, execute, Aer, IBMQ


SHOTS = 300


def validate(isbn, show_circuit=False):
    orig = isbn
    # strip spaces, dashes, and convert X character into hex A
    isbn = isbn.upper().replace('-', '').replace(' ', '').replace('X', 'A')

    # Set up the circuit:
    input_ = QuantumRegister(1, name='isbn')
    output_c = ClassicalRegister(1, name='validation')
    qc = QuantumCircuit(input_, output_c)

    # Set up the qubit
    qc.x(input_)
    qc.h(input_)

    # Encode the ISBN digits (using repeated phase gates)
    len_ = len(isbn)
    if len_ not in (10, 13):
        qc.p(pi, 0)  # encode invalid format input, always returns 0 -- i.e. not valid.

    for i, c in enumerate(isbn):
        if len_ == 13:    # ISBN-13 / EAN-13 phase encoding
            qc.p(int(c) * pi / 5 * (3 if (i & 1) else 1), 0)
        elif len_ == 10:  # ISBN-10 phase encoding
            qc.p(int(c, 16) * 2 * pi / 11 * (10 - i), 0)

    # Validate:
    qc.h(input_)
    qc.measure(input_, output_c)

    # Run / simulate the circuit SHOTS times:
    backend = Aer.get_backend('aer_simulator')
    job = execute(qc, backend, shots=SHOTS)
    result = job.result()
    counts = result.get_counts(qc)

    valid = counts.get('1') == SHOTS

    # Display results:
    print(f'Shots: {SHOTS}')
    print(f'Counts: {counts}')
    if valid:
        print(f'ISBN {orig} validates!')
    else:
        print(f'{orig} does not validate!')
    if counts.get('0') == SHOTS:
        print(f'Possibly not a valid ISBN format: {orig}. An ISBN must be 10 digits from [0-9Xx] OR 13 digits from [0-9], (optionally separated with dashes or spaces).')

    if show_circuit:
        qc.draw(output='mpl')
        plt.show()

    return valid


if __name__ == '__main__':
    isbn = sys.argv[1]
    print(f'Validating ISBN {isbn}...')
    validate(isbn, show_circuit=True)
