from tqdm import tqdm
import time
from typing import Optional

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
