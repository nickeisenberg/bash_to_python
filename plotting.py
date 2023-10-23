import matplotlib.pyplot as plt
import mpld3
from flask import Flask
import matplotlib.pyplot as plt

def ec2plotter(
    fig,
    public_ip
    ):
    app = Flask(__name__)
    @app.route('/')
    def _plot(fig=fig):
        interactive_plot = mpld3.fig_to_html(fig)
        return interactive_plot
    _plot(fig=fig)
    app.run(host=public_ip, port=80)
    return None


fig = plt.figure()
plt.plot([1, 2, 3], [1, 2, 3])
plt.xlabel("x axis")

ec2plotter(fig, "0.0.0.0")
