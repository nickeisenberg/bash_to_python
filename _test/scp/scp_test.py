"""
scp prints to stderr not stdout. wtf.
"""

from transfer import scp
from transfer.utils import list_files_recursively
from tqdm import tqdm
import os

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
)

num_files = len(list_files_recursively(source_path))

with tqdm(
    desc='upload', ncols=60, total=num_files, unit='files', unit_scale=1
) as pbar:
    scp(
        port=port,
        source_path=source_path,
        save_path=save_path,
        user=user,
        ip=ip,
        progress_bar=pbar,
        measure_by="count"
    )
