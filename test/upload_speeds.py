from tqdm import tqdm
import pyaws
import os
import time
import os
import boto3
import botocore
import boto3.s3.transfer as s3transfer
import json

# get the access and secret keys to the aws account
with open("/home/nicholas/.credentials/password.json") as oj:
    pw = json.load(oj)

ACCESS_KEY = pw['aws_ACCESS_KEY_nick']
SECRET_ACCESS_KEY = pw['aws_SECRET_ACCESS_KEY_nick']

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    profile_name="nick",
    region_name="us-west-1"
)

# delete and remake the folder
s3_res = session.resource('s3')

bucket = s3_res.Bucket('speed-demo-bucket')
_ = bucket.objects.filter(Prefix="imgs/").delete()
bucket.put_object(Key="imgs/")

#-------------------------------------------------- 

source_dir = "/home/nicholas/Datasets/CelebA/img64_1000"
num_b = sum([os.stat(os.path.join(path, f)).st_size for f in os.listdir(path)])
save_dir = "s3://speed-demo-bucket/imgs"
profile = "nick"
notify_after = 25

totalsize = sum([os.stat(f).st_size for f in filelist])

before = time.time()
pyaws.copy_dir(source_dir, save_dir, profile, notify_after)
after = time.time()

print(totalsize / (after - before) / 1000)

#-------------------------------------------------- 

def fast_upload(
    session, 
    bucketname, 
    s3dir, 
    filelist, 
    progress_func, 
    workers=20
    ):
    botocore_config = botocore.config.Config(max_pool_connections=workers)
    s3client = session.client('s3', config=botocore_config)
    transfer_config = s3transfer.TransferConfig(
        use_threads=True,
        max_concurrency=workers,
    )
    s3t = s3transfer.create_transfer_manager(s3client, transfer_config)
    for src in filelist:
        dst = os.path.join(s3dir, os.path.basename(src))
        s3t.upload(
            src, bucketname, dst,
            subscribers=[
                s3transfer.ProgressCallbackInvoker(progress_func),
            ],
        )
    s3t.shutdown()  # wait for all the upload tasks to finish


bucketname = 'speed-demo-bucket'
s3dir = 'imgs'
filelist = [os.path.join(source_dir, f) for f in os.listdir(source_dir)]

with tqdm(
    desc='upload', ncols=60, total=totalsize, unit='B', unit_scale=1
) as pbar:
    fast_upload(session, bucketname, s3dir, filelist, pbar.update, workers=20)



