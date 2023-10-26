"""
The following code is to be run on the ec2 instance.
Use a REPL to do so.
"""

import matplotlib.pyplot as plt
from pyaws.plotting import Plotter

port = "<the port that you local network allows for incoming ssh>"
save_path = "/path/to/folder/that/trigger/is/active/in"
user = "username of local computer"
ip = "local ip address"

plotter = Plotter(user, ip, save_path, port)

fig = plt.figure()

plt.plot(
    x=[1, 2, 3, 4, 5], 
    y=[1, 3, 2, 4, 8]
)

plotter.show("figure_name", fig)
