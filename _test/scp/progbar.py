from tqdm import tqdm
import time
from typing import Optional
from pyaws.transfer import scp

def fake_loader(
        numfiles=20, sleep=.2, progbar: Optional[tqdm]=None
    ):
    for i in range(numfiles):
        print(f"file {i} uploaded")
        print('\033[1A', end='\x1b[2K')
        time.sleep(sleep)
        if progbar:
            progbar.update(1)


with tqdm(
    desc='upload', ncols=60, total=20, unit='files', unit_scale=1
) as pbar:
    fake_loader(sleep=.5, progbar=pbar)


port = "22"
source_path = "/home/nicholas/GitRepos/pyaws/_test/scp/move"
save_path = "/home/ubuntu/movedir"
user = "ubuntu"
ip = "54.151.14.242"
logfile = "/home/nicholas/GitRepos/pyaws/_test/scp/logfiles/logfile.log"

with tqdm(
    desc='upload', ncols=60, total=3, unit='files', unit_scale=1
) as pbar:
    scp(
        port=port,
        source_path=source_path,
        save_path=save_path,
        user=user,
        ip=ip,
        generate_logfile_to=logfile,
        progress_bar=pbar
    
    )
