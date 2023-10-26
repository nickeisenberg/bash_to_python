import json
import boto3
from pyaws.transfer import fast_upload
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

# make a boto3 client and resource
s3_client = session.client('s3', region_name="us-west-1")
s3_res = session.resource('s3')

# list all active buckets in the account
buckets = [
    bucket['Name'] for bucket in s3_client.list_buckets()['Buckets']
]

# chose name for the new bucket
pyaws_bucket = 'pyaws-demo-bucket'

# add the bucket if its not already in there. This is actually
# redundant since bucket names must be %100 unuque across all 
# aws users.
if pyaws_bucket not in buckets:
    print('Creating the bucket')
    s3_client.create_bucket(
        Bucket=pyaws_bucket,
    )

# Add a `imgs/` folder to the bucket
bucket = s3_res.Bucket(pyaws_bucket)
_ = bucket.objects.filter(Prefix="imgs/").delete()
bucket.put_object(Key="imgs/")


# move everything from `source_dir` to `s3dir` in the s3 bucket
source_dir = "/home/nicholas/Datasets/CelebA/batched"
s3dir = 'imgs'

# find the size of the files being moved for the tqdn progress bar
filelist = [os.path.join(source_dir, f) for f in os.listdir(source_dir)]
totalsize = sum([os.stat(f).st_size for f in filelist])


with tqdm(
    desc='upload', ncols=60, total=totalsize, unit='B', unit_scale=1
) as pbar:
    fast_upload(
        session, 
        pyaws_bucket, 
        s3dir, 
        filelist, 
        pbar, 
        workers=10
    )
