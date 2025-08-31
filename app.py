from flask import Flask, render_template_string
import numpy as np
from quantum_simulator import run_quantum_simulation
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram, plot_state_city
import io
import base64

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Quantum Circuit Simulator</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        pre { background: #f4f4f4; padding: 10px; border-radius: 5px; }
        img { max-width: 100%; height: auto; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>Quantum Circuit Simulation Results</h1>
    <h2>Measurement Counts</h2>
    <pre>{{ counts }}</pre>
    <h2>Statevector</h2>
    <pre>{{ statevector }}</pre>
    <h2>Histogram</h2>
    <img src="data:image/png;base64,{{ histogram }}" alt="Histogram">
    <h2>State-City Plot</h2>
    <img src="data:image/png;base64,{{ state_city }}" alt="State-City Plot">
    <p><a href="/simulate">Run Simulation Again</a></p>
</body>
</html>
"""


def plot_to_base64(fig):
    """Convert a matplotlib figure to base64-encoded PNG."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


@app.route("/")
def index():
    return redirect(url_for("simulate"))


@app.route("/simulate", methods=["GET"])
def simulate():
    counts, statevector = run_quantum_simulation(theta=np.pi / 4, shots=1024)
    statevector_list = np.array(statevector).tolist()

    histogram_fig = plot_histogram(counts)
    state_city_fig = plot_state_city(statevector)

    histogram_b64 = plot_to_base64(histogram_fig)
    state_city_b64 = plot_to_base64(state_city_fig)

    return render_template_string(
        HTML_TEMPLATE,
        counts=counts,
        statevector=statevector_list,
        histogram=histogram_b64,
        state_city=state_city_b64,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
