from sshtools.transfer import SecureCopyProtocol
import os

home = os.environ['HOME']
pem = os.environ['USWEST1']

scp = SecureCopyProtocol(
    user="nick",
    ip="54.215.93.24",
    port="22",
    pem=pem
)

#--------------------------------------------------
# Sending
#--------------------------------------------------

# mac
source_path = home + "/GitRepos/sshtools/tests/transfer/move"

# ubunut
source_path = home + "/GitRepos/sshtools_project/sshtools/tests/transfer/move"

save_path = "/nvme1n1/nick/Tmp/sshtools_test"

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
