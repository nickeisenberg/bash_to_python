from sshtools.transfer import SecureCopyProtocol
from sshtools.transfer.utils import list_files_recursively
import os

scp = SecureCopyProtocol(
    user="nick",
    ip="54.183.226.197",
    port="22"
)

home = os.environ['HOME']

# mac
source_path = home + "/GitRepos/sshtools/tests/transfer/move"

save_path = "/ebs0/nick/Tmp/sshtools_test"

scp.scp(source_path, save_path, with_tqdm=False)
