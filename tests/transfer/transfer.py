from sshtools.transfer import SecureCopyProtocol
import os
from platform import system

home = os.environ['HOME']
pem = os.environ['USWEST1']

scp = SecureCopyProtocol(
    user="nick",
    ip="54.183.251.193",
    port="22",
    pem=pem
)

#--------------------------------------------------
# Sending
#--------------------------------------------------

if system() == "Darwin":
    source_path = home + "/GitRepos/sshtools/tests/transfer/move"
    log_path = os.path.join(
        home,
        'GitRepos', 'sshtools', 'tests', 'transfer', 'logs',
        'send.log'
    )
elif system() == "Linux":
    source_path = home 
    source_path += "/GitRepos/sshtools_project/sshtools/tests/transfer/move"
    log_path = os.path.join(
        home,
        'GitRepos', 'sshtools_project', 'sshtools', 'tests', 'transfer', 'logs',
        'send.log'
    )
else:
    source_path = "wrong OS"
    log_path = "wrong OS"


save_path = "/nvme1n1/nick/Tmp/sshtools_test"

scp.send(source_path, save_path, with_tqdm=True, generate_logfile_to=log_path)

#--------------------------------------------------
# Receiving
#--------------------------------------------------

source_path = "/nvme1n1/nick/Tmp/sshtools_test"

save_path = home + "/Tmp/temp"

if system() == "Darwin":
    log_path = os.path.join(
        home,
        'GitRepos', 'sshtools', 'tests', 'transfer', 'logs',
        'send.log'
    )
elif system() == "Linux":
    log_path = os.path.join(
        home,
        'GitRepos', 'sshtools_project', 'sshtools', 'tests', 'transfer', 'logs',
        'send.log'
    )
else:
    log_path = "wrong OS"

scp.receive(source_path, save_path, with_tqdm=True, generate_logfile_to=log_path)
