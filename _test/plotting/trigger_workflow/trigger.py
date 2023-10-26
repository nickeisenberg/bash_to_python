#--------------------------------------------------
# Use REPL to run below in the ec2 instance
#--------------------------------------------------

import matplotlib.pyplot as plt
from pyaws.plotting import Plotter

port = "2222"
save_path = "/home/nicholas/Tmp/png_trigger_folder"
user = "nicholas"
ip = "174.72.155.21"
# path_to_bash = "/home/ubuntu/gitrepos/pyaws/transfer/scripts/scp.sh"

# plotter = Plotter(user, ip, save_path, port, path_to_bash=path_to_bash)
plotter = Plotter(user, ip, save_path, port)

fig = plt.figure()
plt.plot([1, 2, 3, 4, 5], [1, 3, 2, 4, 8])

plotter.show("test1", fig)
