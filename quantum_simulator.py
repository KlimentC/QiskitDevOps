from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_state_city
import matplotlib.pyplot as plt
import numpy as np

def create_quantum_circuit(theta: float = np.pi/4, with_measure: bool = True) -> QuantumCircuit:
    qc = QuantumCircuit(2, 2) if with_measure else QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.ry(theta, 0)
    if with_measure:
        qc.measure([0, 1], [0, 1])
    return qc

def run_quantum_simulation(theta: float = np.pi/4, shots: int = 1024):
    qc_counts = create_quantum_circuit(theta, with_measure=True)
    simulator_counts = AerSimulator()
    counts_result = simulator_counts.run(qc_counts, shots=shots).result()
    counts = counts_result.get_counts(qc_counts)

    qc_state = create_quantum_circuit(theta, with_measure=False)
    simulator_state = AerSimulator()
    qc_state.save_statevector()
    state_result = simulator_state.run(qc_state).result()
    statevector = state_result.get_statevector(qc_state)

    return counts, statevector

if __name__ == "__main__":
    counts, statevector = run_quantum_simulation()
    print("Measurement results:", counts)
    print("Statevector:", statevector)
    plot_histogram(counts)
    plt.show()
    plot_state_city(statevector)
    plt.show()