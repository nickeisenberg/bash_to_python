from transfer import scp
from plotting import Plotter

#--------------------------------------------------

port = "22"
source_path = "/home/nicholas/GitRepos/pyaws/transfer/scripts/scp.sh"
save_path = "/home/ubuntu/pyscripts/showplots"
user = "ubuntu"
ip = "50.18.80.35"
path_to_bash = "/home/nicholas/GitRepos/pyaws/transfer/scripts/scp.sh"

scp(source_path, save_path, user, ip, port, path_to_bash=path_to_bash)

#--------------------------------------------------

port = "22"
source_path = "/home/nicholas/GitRepos/pyaws/plotting"
save_path = "/home/ubuntu/pyscripts/showplots"
user = "ubuntu"
ip = "50.18.80.35"
path_to_bash = "/home/nicholas/GitRepos/pyaws/transfer/scripts/scp.sh"

scp(source_path, save_path, user, ip, port, path_to_bash=path_to_bash)

#--------------------------------------------------

port = "2222"
source_path = "/home/ubuntu/pyscripts/scp/tempfile.txt"
save_path = "/home/nicholas/temp"
user = "nicholas"
ip = "174.72.155.21"
path_to_bash = "/home/ubuntu/pyscripts/showplots/scp.sh"

from plotting import Plotter

plotter = Plotter(user, ip, save_path, port, path_to_bash=path_to_bash)
