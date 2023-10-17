from tqdm import tqdm
import pyaws.pyaws as pyaws
import os
import time
import os
import boto3
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

source_dir = "/home/nicholas/Datasets/CelebA/batched"
num_b = sum([os.stat(os.path.join(source_dir, f)).st_size for f in os.listdir(source_dir)])
save_dir = "s3://speed-demo-bucket/imgs"
profile = "nick"
notify_after = 1

before = time.time()
pyaws.copy_dir(source_dir, save_dir, profile, notify_after)
after = time.time()

print(num_b / (after - 7 - before) / 1000 / 1000)

#-------------------------------------------------- 


bucketname = 'speed-demo-bucket'
s3dir = 'imgs'
filelist = [os.path.join(source_dir, f) for f in os.listdir(source_dir)]
totalsize = sum([os.stat(f).st_size for f in filelist])

with tqdm(
    desc='upload', ncols=60, total=totalsize, unit='B', unit_scale=1
) as pbar:
    pyaws.fast_upload(session, bucketname, s3dir, filelist, pbar.update, workers=50)
