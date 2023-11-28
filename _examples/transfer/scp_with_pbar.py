"""
tqdm integration with pyaws.transfer.scp
"""

from tqdm import tqdm
from sshtools.transfer import scp
import os


port = "<port used to scp to remote server>"
source_path = "/path/to/data/that/needs/to/be/transfered"
save_path = "/path/to/save/to"
user = "<login name of remote server>"
ip = "<pubic_ip of remote server>"
logfile = "/local/path/to/generate/log/file"

num_files = len(os.listdir(source_path))

with tqdm(
    desc='upload', ncols=60, total=num_files, unit='files', unit_scale=1
) as pbar:
    scp(
        port=port,
        source_path=source_path,
        save_path=save_path,
        user=user,
        ip=ip,
        generate_logfile_to=logfile,
        progress_bar=pbar,
        measure_by="count"
    )
