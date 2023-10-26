"""
scp prints to stderr not stdout. wtf.
"""

from pyaws.transfer import scp

port = "22"
source_path = "/home/nicholas/GitRepos/pyaws/_test/scp/move"
save_path = "/home/ubuntu/movedir"
user = "ubuntu"
ip = "54.151.14.242"
logfile = "/home/nicholas/GitRepos/pyaws/_test/scp/logfiles/logfile.log"

scp(
    port=port,
    source_path=source_path,
    save_path=save_path,
    user=user,
    ip=ip,
    generate_logfile_to=logfile,
)
