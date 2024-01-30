from shwrap.transfer import SecureCopyProtocol
import os
from platform import system
import time

home = os.environ['HOME']
pem = os.environ['USWEST1']

scp = SecureCopyProtocol(
    user="nick",
    ip="54.193.254.114",
    port="22",
    pem=pem
)

#--------------------------------------------------
# Sending
#--------------------------------------------------

if system() == "Darwin":
    source_path = home + "/GitRepos/shwrap/tests/transfer/move"
    log_path = os.path.join(
        home,
        'GitRepos', 'shwrap', 'tests', 'transfer', 'logs',
        'send.log'
    )
elif system() == "Linux":
    source_path = home 
    source_path += "/GitRepos/shwrap_project/shwrap/tests/transfer/move"
    log_path = os.path.join(
        home,
        'GitRepos', 'shwrap_project', 'shwrap', 'tests', 'transfer', 'logs',
        'send.log'
    )
else:
    source_path = "wrong OS"
    log_path = "wrong OS"

save_path = "/nvme1n1users/nick/Tmp/shwrap"

scp.put(source_path, save_path, with_tqdm=True, generate_logfile_to=log_path)

#--------------------------------------------------
# Receiving
#--------------------------------------------------

source_path = "/nvme1n1users/nick/Tmp/shwrap"

save_path = home + "/Tmp/temp"

if system() == "Darwin":
    log_path = os.path.join(
        home,
        'GitRepos', 'shwrap', 'tests', 'transfer', 'logs',
        'receive.log'
    )
elif system() == "Linux":
    log_path = os.path.join(
        home,
        'GitRepos', 'shwrap_project', 'shwrap', 'tests', 'transfer', 'logs',
        'receive.log'
    )
else:
    log_path = "wrong OS"

scp.get(source_path, save_path, with_tqdm=True, generate_logfile_to=log_path)
