"""
scp prints to stderr not stdout. wtf.
"""

from sshtools.transfer import SecureCopyProtocol

port = "22"
user = "ubuntu"
ip = "184.72.19.219"

scp = SecureCopyProtocol(user, ip, port)

source_path = "/home/nicholas/GitRepos/sshtools_project/sshtools/tests/scp/move"
save_path = "/home/ubuntu/Tmp"

scp.scp(source_path, save_path)
