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

# ubunut
source_path = home + "/GitRepos/sshtools_project/sshtools/tests/transfer/move"

save_path = "/ebs0/nick/Tmp/sshtools_test"

log_path = os.path.join(home, 'file.log')

scp.scp(source_path, save_path, with_tqdm=True, generate_logfile_to=log_path)
