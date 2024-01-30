"""
A speed test of scp with subprocess vs scp with paramiko
"""

import paramiko
from scp import SCPClient
import os
import time
from shwrap.transfer import SecureCopyProtocol

class SecureCopyProtocolParamiko:
    def __init__(self, hostname, port, username, pem_file_path):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.pem_file_path = pem_file_path

        self.ssh_client: paramiko.SSHClient = self._create_ssh_client()

    def put(self, local_path, remote_path):
        """Copy a directory recursively from the remote host to local host using SCP."""
        transport = self.ssh_client.get_transport()
        assert isinstance(transport, paramiko.Transport)
        with SCPClient(transport, progress=self._progress) as scp:
            scp.put(local_path, remote_path, recursive=True)

    def get(self, remote_path, local_path):
        """Copy a directory recursively from the remote host to local host using SCP."""
        transport = self.ssh_client.get_transport()
        assert isinstance(transport, paramiko.Transport)
        with SCPClient(transport, progress=self._progress) as scp:
            scp.get(remote_path, local_path, recursive=True)

    def _create_ssh_client(self):
        """Create and return an SSH client, connected to the host."""
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            self.hostname, 
            self.port, 
            self.username,
            key_filename=self.pem_file_path
        )
        return ssh
    
    @staticmethod
    def _progress(filename, size, sent):
        """ Function to track the progress of the SCP transfer """
        print(f"Transferring {filename}: {float(sent)/float(size)*100:.2f}% complete")
        print('\033[1A', end='\x1b[2K')

hostname = '13.56.233.243'
port = 22
username = 'nick'
pem_file_path = os.environ["USWEST1"]

scp_paramiko = SecureCopyProtocolParamiko(
    hostname=hostname, 
    port=port, 
    username=username, 
    pem_file_path=pem_file_path
)

scp = SecureCopyProtocol(
    user=username,
    ip=hostname,
    port=str(port),
    pem=pem_file_path
)

celebA_path = "/home/nicholas/Datasets/celebA/imgs_1000"

# this took 53 seconds
remote_path_shwrap = '/nvme1n1users/nick/Tmp/shwrap'
now = time.time()
scp.put(
    source_path=celebA_path, 
    save_path=remote_path_shwrap, 
    with_tqdm=True
)
after = time.time() - now
print(after)

# this took 88 seconds
remote_path_paramiko = '/nvme1n1users/nick/Tmp/paramiko'
now = time.time()
scp_paramiko.put(
    local_path=celebA_path,
    remote_path=remote_path_paramiko
)
after = time.time() - now
print(after)
