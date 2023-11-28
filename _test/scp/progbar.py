"""
tqdm integration with pyaws.transfer.scp
"""

from tqdm import tqdm
from sshtools.transfer import scp
import os


port = "22"
source_path = "/home/nicholas/GitRepos/pyaws/_test/scp/move"
save_path = "/home/ubuntu/movedir"
user = "ubuntu"
ip = "54.151.14.242"
logfile = "/home/nicholas/GitRepos/pyaws/_test/scp/logfiles/logfile.log"

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
