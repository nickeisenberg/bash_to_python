"""
scp prints to stderr not stdout. wtf.
"""

from transfer import scp

port = "22"
source_path = "/home/nicholas/GitRepos/sshtools_project/sshtools/_test/scp/move"
save_path = "/home/ubuntu/Tmp"
user = "ubuntu"
ip = "184.72.19.219"


scp(
    port=port,
    source_path=source_path,
    save_path=save_path,
    user=user,
    ip=ip,
    with_tqdm=True
)
