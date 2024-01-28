import json
import boto3
from btp.transfer.aws import fast_upload
from tqdm import tqdm
import os

with open("/home/nicholas/.credentials/password.json") as oj:
    pw = json.load(oj)

ACCESS_KEY = pw['aws_ACCESS_KEY_nick']
SECRET_ACCESS_KEY = pw['aws_SECRET_ACCESS_KEY_nick']

# start the boto3 session
session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    profile_name="nick",
    region_name="us-west-1"
)

home = os.environ["HOME"]
root = home + "/GitRepos/bash_to_python_project/bash_to_python/tests/transfer/aws/"
source_dir  = root + 'move/'

# find the size of the files being moved for the tqdn progress bar
filelist = [os.path.join(source_dir, f) for f in os.listdir(source_dir)]
totalsize = sum([os.stat(f).st_size for f in filelist])

with tqdm(
    desc='upload', ncols=60, total=totalsize, unit='B', unit_scale=1
) as pbar:
    fast_upload(
        session, 
        "sshtools-demo-bucket", 
        "", 
        filelist, 
        pbar, 
        workers=10
    )
