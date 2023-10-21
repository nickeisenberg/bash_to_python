import matplotlib.pyplot as plt
import mpld3
from flask import Flask

app = Flask(__name__)

# Function to generate a Matplotlib plot
def generate_plot():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [1, 4, 9, 16])
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('Matplotlib Plot')
    return fig

@app.route('/')
def plot_page():
    fig = generate_plot()
    # Convert the Matplotlib figure to an interactive D3.js plot
    interactive_plot = mpld3.fig_to_html(fig)
    return interactive_plot

if __name__ == '__main__':
    app.run(host="192.168.1.32")

