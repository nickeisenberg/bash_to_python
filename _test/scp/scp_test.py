"""
scp prints to stderr not stdout. wtf.
"""

from transfer import scp

port = "22"
source_path = "/home/nicholas/GitRepos/pyaws/test/scp/move"
save_path = "/home/ubuntu/movedir"
user = "ubuntu"
ip = "50.18.80.35"
path_to_bash = "/home/nicholas/GitRepos/pyaws/transfer/scripts/scp.sh"
logfile = "/home/nicholas/test.log"
pem = "/home/nicholas/.credentials/keypairs/us-west-1-kp.pem"

scp(
    port, 
    source_path, 
    save_path, 
    user, 
    ip,
    pem=pem,
    generate_logfile_to=logfile,
    path_to_bash=path_to_bash
)
