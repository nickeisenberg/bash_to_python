from sshtools.transfer import SecureCopyProtocol
import os

scp = SecureCopyProtocol(
    user="nick",
    ip="54.183.226.197",
    port="22"
)

home = os.environ['HOME']

#--------------------------------------------------
# Sending
#--------------------------------------------------

# mac
source_path = home + "/GitRepos/sshtools/tests/transfer/move"

# ubunut
source_path = home + "/GitRepos/sshtools_project/sshtools/tests/transfer/move"

save_path = "/ebs0/nick/Tmp/sshtools_test"

log_path = os.path.join(
    home,
    'GitRepos', 'sshtools_project', 'sshtools', 'tests', 'transfer', 'logs',
    'send.log'
)

scp.send(source_path, save_path, with_tqdm=True, generate_logfile_to=log_path)

#--------------------------------------------------
# Receiving
#--------------------------------------------------

source_path = "/ebs0/nick/Tmp/sshtools_test/move"

save_path = home + "/Tmp/temp"

log_path = os.path.join(
    home,
    'GitRepos', 'sshtools_project', 'sshtools', 'tests', 'transfer', 'logs',
    'receive.log'
)

scp.receive(source_path, save_path, with_tqdm=True, generate_logfile_to=log_path)
