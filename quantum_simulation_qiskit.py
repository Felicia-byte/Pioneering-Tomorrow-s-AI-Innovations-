"""
Simple QAOA example for MaxCut on a 3-node graph using Qiskit.
This script builds a QAOA circuit and runs a local simulator. It includes notes on running on IBM Quantum Experience.

How it relates to AI optimization: QAOA provides a quantum-enhanced heuristic for combinatorial optimization problems (e.g., molecular candidate selection, feature subset selection). In practice, a hybrid workflow would offload a hard combinatorial subproblem to the quantum optimizer while classical ML handles feature extraction and evaluation.
"""

import importlib
try:
    qiskit = importlib.import_module('qiskit')
    Aer = getattr(qiskit, 'Aer')
    execute = getattr(qiskit, 'execute')
    QuantumInstance = getattr(importlib.import_module('qiskit.utils'), 'QuantumInstance')
    PauliSumOp = getattr(importlib.import_module('qiskit.opflow'), 'PauliSumOp')
    QuadraticProgram = getattr(importlib.import_module('qiskit_optimization'), 'QuadraticProgram')
    QuadraticProgramToQubo = getattr(importlib.import_module('qiskit_optimization.converters'), 'QuadraticProgramToQubo')
    QAOA = getattr(importlib.import_module('qiskit.algorithms'), 'QAOA')
    COBYLA = getattr(importlib.import_module('qiskit.algorithms.optimizers'), 'COBYLA')
except Exception as e:
    raise ImportError(
        "qiskit and qiskit-optimization are required to run this script; install them with:\n"
        "    pip install qiskit qiskit-optimization\n"
        "If you already installed them, ensure your interpreter/environment is configured correctly."
    ) from e
# Build a MaxCut QUBO for a triangle graph (3 nodes fully connected)
# MaxCut: maximize edges across the cut -> convert to minimization QUBO

# Graph edges
edges = [(0,1),(1,2),(0,2)]

# Create QuadraticProgram
qp = QuadraticProgram()
for i in range(3):
    qp.binary_var(name=f'x{i}')

# Objective: minimize -sum_{(i,j) in E} x_i (1 - x_j) + x_j (1 - x_i)
# Equivalent QUBO representation: we can encode a standard MaxCut objective
linear = {f'x{i}': 0 for i in range(3)}
quadratic = {}
for (i,j) in edges:
    quadratic[(f'x{i}', f'x{j}')] = 1

qp.minimize(linear=linear, quadratic=quadratic)

# Convert to QUBO
conv = QuadraticProgramToQubo()
qubo = conv.convert(qp)

# Convert to operator
op = qubo.to_ising()[0]
pauli_op = PauliSumOp.from_operator(op)

# Set up QAOA
backend = Aer.get_backend('aer_simulator_statevector')
quantum_instance = QuantumInstance(backend)
optimizer = COBYLA(maxiter=100)
qaoa = QAOA(optimizer=optimizer, reps=1, quantum_instance=quantum_instance)

result = qaoa.compute_minimum_eigenvalue(pauli_op)
print('QAOA result:', result)

# Notes for IBM Quantum Experience
# - To run on IBM real hardware, set up an IBMQ account and use IBMQ.load_account() and a provider backend.
# - QAOA on real devices requires transpilation, noise-aware compilation, and short depth (reps) due to noise.

# How this optimizes an AI task (example):
# - Consider a drug-discovery pipeline where a large set of candidate molecules must be selected under budget constraints
#   and pairwise incompatibilities. This can be framed as a combinatorial optimization problem (MaxCut-like or knapsack-QUBO).
# - A hybrid workflow: classical model scores molecules (predict activity, ADMET), then a QAOA solver finds an optimal subset maximizing diversity and predicted efficacy under constraints.
# - Current limitations: NISQ devices are small and noisy; simulation or quantum annealers may be used until hardware scales.
