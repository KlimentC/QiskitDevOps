import pytest
import numpy as np
from quantum_simulator import run_quantum_simulation, create_quantum_circuit


def test_simulation_output():
    counts, statevector = run_quantum_simulation(theta=np.pi / 4, shots=1024)
    valid_keys = {"00", "01", "10", "11"}
    for key in counts.keys():
        assert key in valid_keys
    assert sum(counts.values()) == 1024
    probabilities = np.abs(statevector) ** 2
    total_prob = np.sum(probabilities)
    assert np.isclose(total_prob, 1.0, atol=1e-10)
    prob_00 = probabilities[0]
    prob_11 = probabilities[3]
    assert prob_00 + prob_11 > 0.5


def test_bell_state():
    counts, _ = run_quantum_simulation(theta=0, shots=1024)
    assert "00" in counts and "11" in counts
    assert "01" not in counts and "10" not in counts
    assert sum(counts.values()) == 1024


def test_circuit_structure_with_measure():
    qc = create_quantum_circuit(theta=np.pi / 4, with_measure=True)
    assert len(qc.data) == 5
    assert qc.num_qubits == 2
    assert qc.num_clbits == 2


def test_circuit_structure_no_measure():
    qc = create_quantum_circuit(theta=np.pi / 4, with_measure=False)
    assert len(qc.data) == 3
    assert qc.num_qubits == 2
    assert qc.num_clbits == 0


def test_statevector_bell():
    _, statevector = run_quantum_simulation(theta=0, shots=1024)
    probabilities = np.abs(statevector) ** 2
    assert np.isclose(probabilities[0], 0.5, atol=1e-2)
    assert np.isclose(probabilities[3], 0.5, atol=1e-2)
    assert np.isclose(probabilities[1], 0.0, atol=1e-2)
    assert np.isclose(probabilities[2], 0.0, atol=1e-2)


def test_different_shots():
    counts, _ = run_quantum_simulation(theta=np.pi / 4, shots=2048)
    assert sum(counts.values()) == 2048
    valid_keys = {"00", "01", "10", "11"}
    for key in counts.keys():
        assert key in valid_keys


def test_negative_theta():
    counts, statevector = run_quantum_simulation(theta=-np.pi / 4, shots=1024)
    assert sum(counts.values()) == 1024
    probabilities = np.abs(statevector) ** 2
    assert np.isclose(np.sum(probabilities), 1.0, atol=1e-10)


def test_zero_shots():
    with pytest.raises(Exception):
        counts, _ = run_quantum_simulation(theta=np.pi / 4, shots=0)


def test_circuit_depth():
    qc = create_quantum_circuit(theta=np.pi / 4, with_measure=True)
    assert qc.depth() == 4


def test_statevector_norm():
    _, statevector = run_quantum_simulation(theta=np.pi / 8, shots=1024)
    probabilities = np.abs(statevector) ** 2
    assert np.isclose(np.sum(probabilities), 1.0, atol=1e-10)
