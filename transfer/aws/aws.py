import subprocess
import os
from typing import Optional
import botocore
import boto3
import boto3.s3.transfer as s3transfer
from tqdm import tqdm
import time

p = subprocess.run(
    "pip show pip | awk '/Location/ {print $2}'", 
    shell=True,
    capture_output=True,
    text=True
)
PATH_TO_PYAWS = os.path.join(
    p.stdout.strip(),
    "pyaws"
)

def cp_recursive(
    source_dir: str, 
    save_dir: str,
    profile: str,
    generate_logfile_to: Optional[str]=None,
    path_to_bash: Optional[str]=None
    ):

    """
    A python function that calls a bash function that applies 
    aws s3 cp --recurisve on a whole local directory.

    Parameters
    ----------
    source_dir: str
        The full file path to the local dir containing the files that need to be
        moved.

    save_dir: str
        Full path of the dir being saved to.

    profile: str
        The name of the profile that is configured with `aws configure`

    generate_log_file: str, default None
        The full path to where a log file will be created give the full stdout
        output of the `aws s3 cp` function. If None, then no log file will be 
        generated

    path_to_bash: Optional[str]=None
        The path to the underlying bash script being called. If None then it 
        assumes that the `pyaws` module is located where python looks for the libraries,
        ie in the same folder that `pip show pip | awk '/Location/ {print $2}'`.

    Returns
    -------
    None
    
    Example
    -------

    >>> source_dir = '/home/nicholas/Datasets/CelebA/img_64_10'
    >>> save_dir = 's3://celeba-demo-bucket'
    >>> profile = "nick"
    >>> log_file = "/home/nicholas/Tmp/update.log"

    >>> pyaws.cp_recursive(
    >>>     source_dir,
    >>>     save_dir,
    >>>     profile,
    >>>     generate_log_file=log_file
    >>> )
    """

    if path_to_bash is None:
        path_to_bash = os.path.join(
            PATH_TO_PYAWS, 'scripts', 'awssync.sh'
        )

    try:
        # Call the Bash script with specified parameters
        with subprocess.Popen(
            [
                path_to_bash, 
                "--source-dir", 
                source_dir, 
                "--save-dir", 
                save_dir, 
                "--profile", 
                profile, 
            ],
            stdout=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        ) as p:
            last_status = "None"
            last_file_uploaded = "None"
            for i, line in enumerate(p.stdout):
                line = line[:-1]
                if line.startswith("Completed"):
                    last_status = line
                    output = f"{last_status}\n{last_file_uploaded}"
                    print(f"{output}")
                    print('\033[1A', end='\x1b[2K')
                    print('\033[1A', end='\x1b[2K')
                    
                else:
                    last_file_uploaded = line
                    output = f"{last_status}\n{last_file_uploaded}"
                    print(f"{output}")
                    print('\033[1A', end='\x1b[2K')
                    print('\033[1A', end='\x1b[2K')

                if generate_logfile_to is not None:
                    with open(generate_logfile_to, "a") as log:
                        _ = log.write(line + "\n")

    except subprocess.CalledProcessError as e:
        print(f"Error calling the Bash script: {e}")

    except FileNotFoundError as e:
        print(f"Bash script not found: {e}")

    return None


def sync(
    source_dir: str, 
    save_dir: str,
    profile: str,
    generate_logfile_to: Optional[str]=None,
    path_to_bash: Optional[str]=None
    ):

    """
    A python function that calls a bash function that applies 
    aws s3 cp --recurisve on a whole local directory. According to the internet
    aws s3 cp is faster aws s3 sync and I believe both of these are faster than
    using boto3 functions directly to move files from local to s3.

    Parameters
    ----------
    source_dir: str
        The full file path to the local dir containing the files that need to be
        moved.

    save_dir: str
        Full path of the dir being saved to.

    profile: str
        The name of the profile that is configured with aws configure

    generate_log_file: str, default None
        The full path to where a log file will be created give the full stdout
        output of the `aws s3 sync` function. If None, then no log file will be 
        generated

    path_to_bash: Optional[str]=None
        The path to the underlying bash script being called. If None then it 
        assumes that the `pyaws` module is located where python looks for the libraries,
        ie in the same folder that `pip show pip | awk '/Location/ {print $2}'`.

    Returns
    -------
    None
    
    Example
    -------

    >>> source_dir = '/home/nicholas/Datasets/CelebA/img_64_10'
    >>> save_dir = 's3://celeba-demo-bucket'
    >>> profile = "nick"
    >>> log_file = "/home/nicholas/Tmp/update.log"
    
    >>> pyaws.sync(
    >>>     source_dir,
    >>>     save_dir,
    >>>     profile,
    >>>     generate_log_file=log_file
    >>> )

    """
    
    if path_to_bash is None:
        path_to_bash = os.path.join(
            PATH_TO_PYAWS, 'scripts', 'awssync.sh'
        )

    try:
        # Call the Bash script with specified parameters
        with subprocess.Popen(
            [
                path_to_bash, 
                "--source-dir", 
                source_dir, 
                "--save-dir", 
                save_dir, 
                "--profile", 
                profile, 
            ],
            stdout=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        ) as p:

            last_status = "None"
            last_file_uploaded = "None"
            for i, line in enumerate(p.stdout):
                line = line[:-1]

                if line.startswith("Completed"):
                    last_status = line
                    output = f"{last_status}\n{last_file_uploaded}"
                    print(f"{output}")
                    print('\033[1A', end='\x1b[2K')
                    print('\033[1A', end='\x1b[2K')
                    
                else:
                    last_file_uploaded = line
                    output = f"{last_status}\n{last_file_uploaded}"
                    print(f"{output}")
                    print('\033[1A', end='\x1b[2K')
                    print('\033[1A', end='\x1b[2K')

                if generate_logfile_to is not None:
                    with open(generate_logfile_to, "a") as log:
                        _ = log.write(line + "\n")


    except subprocess.CalledProcessError as e:
        print(f"Error calling the Bash script: {e}")

    except FileNotFoundError as e:
        print(f"Bash script not found: {e}")

    return None


def fast_upload(
    session: boto3.Session, 
    bucketname: str, 
    s3dir: str, 
    filelist: list, 
    progress_func: tqdm, 
    workers: int=20,
    ):
    """
    This is a uploder that can be used to move all files within a folder to a 
    AWS s3 bucket. This essentially behaves exactly the same as 
    pyaws.cp_recursive.

    Taken from...
    https://stackoverflow.com/questions/56639630/how-can-i-increase-my-aws-s3-upload-speed-when-using-boto3

    Parameters
    ----------
    session: boto3.Session
    bucketname: str
        Just the name of the bucket, not the full bucket path 
    s3dir: str
        the folder path within the bucket
    filelist:
        list of local files to be moved to the bucket
    progress_func: tqdm
        An instance of a tqdm class
    workers: int
        The number of workers to work in parallel and move the data to AWS

    Example
    -------
    >>> from tqdm import tqdm
    >>> import pyaws
    >>> import os
    >>> import time
    >>> import os
    >>> import boto3
    >>> import json
    >>> 
    >>> # get the access and secret keys to the aws account
    >>> with open("/home/nicholas/.credentials/password.json") as oj:
    >>>     pw = json.load(oj)
    >>> 
    >>> ACCESS_KEY = pw['aws_ACCESS_KEY_nick']
    >>> SECRET_ACCESS_KEY = pw['aws_SECRET_ACCESS_KEY_nick']

    >>> session = boto3.Session(
    >>>     aws_access_key_id=ACCESS_KEY,
    >>>     aws_secret_access_key=SECRET_ACCESS_KEY,
    >>>     profile_name="nick",
    >>>     region_name="us-east-1"
    >>> )
    >>> bucketname = 'celeba-demo-bucket'
    >>> s3dir = 'imgs'
    >>> filelist = [os.path.join(source_dir, f) for f in os.listdir(source_dir)]
    >>> totalsize = sum([os.stat(f).st_size for f in filelist])
    >>> 
    >>> with tqdm(
    >>>     desc='upload', ncols=60, total=totalsize, unit='B', unit_scale=1
    >>> ) as pbar:
    >>>     fast_upload(
                session, 
                bucketname, 
                s3dir, 
                filelist, 
                pbar, 
                workers=50
            )
    """

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
                s3transfer.ProgressCallbackInvoker(progress_func.update),
            ],
        )
    s3t.shutdown()  # wait for all the upload tasks to finish


def fast_download(
    session: boto3.Session, 
    bucketname: str, 
    keylist: list, 
    localdir: str, 
    progress_func: tqdm, 
    workers: int=20,
    ):
    """
    This is a downloader that can be used to move all files within a folder 
    on a s3 bucket to a folder local on your computer. This essentially behaves 
    exactly the same as pyaws.cp_recursive.

    A slight modification from...
    https://stackoverflow.com/questions/56639630/how-can-i-increase-my-aws-s3-upload-speed-when-using-boto3

    Parameters
    ----------
    session: boto3.Session
    bucketname: str
        Just the name of the bucket, not the full bucket path 
    keylist: list
        list of keys from the s3 bucket to be moved to the local computer
    progress_func: tqdm
        An instance of a tqdm class
    workers: int
        The number of workers to work in parallel and move the data to AWS

    Example
    -------
    >>> from tqdm import tqdm
    >>> import pyaws
    >>> import os
    >>> import time
    >>> import os
    >>> import boto3
    >>> import json
    >>> 
    >>> # get the access and secret keys to the aws account
    >>> with open("/home/nicholas/.credentials/password.json") as oj:
    >>>     pw = json.load(oj)
    >>> 
    >>> ACCESS_KEY = pw['aws_ACCESS_KEY_nick']
    >>> SECRET_ACCESS_KEY = pw['aws_SECRET_ACCESS_KEY_nick']

    >>> session = boto3.Session(
    >>>     aws_access_key_id=ACCESS_KEY,
    >>>     aws_secret_access_key=SECRET_ACCESS_KEY,
    >>>     profile_name="nick",
    >>>     region_name="us-east-1"
    >>> )
    >>> s3_res = session.resource('s3')
    >>> bucketname = 'speed-demo-bucket'
    >>> bucket = s3_res.Bucket(bucketname)
    >>> bucket_objects = [
    >>>     x.key 
    >>>     for x in bucket.objects.filter(Prefix="imgs/") 
    >>>     if x.key.endswith('<some desired filetype>')
    >>> ]
    >>> object_sizes = [
    >>>     x.size 
    >>>     for x in bucket.objects.filter(Prefix="imgs/")
    >>>     if x.key.endswith('<some desired filetype>')
    >>> ]
    >>> totalsize = sum(object_sizes)
    >>> localdir = "/home/nicholas/Datasets/CelebA/ret"
    >>> 
    >>> with tqdm(
    >>>     desc='upload', ncols=60, total=totalsize, unit='B', unit_scale=1
    >>> ) as pbar:
    >>>     fast_upload(
    >>>         session, 
    >>>         bucketname, 
    >>>         s3dir, 
    >>>         filelist, 
    >>>         pbar, 
    >>>         workers=50
    >>>    )
    """

    botocore_config = botocore.config.Config(max_pool_connections=workers)
    s3client = session.client('s3', config=botocore_config)
    transfer_config = s3transfer.TransferConfig(
        use_threads=True,
        max_concurrency=workers,
    )
    s3t = s3transfer.create_transfer_manager(s3client, transfer_config)
    for src in keylist:
        dst = os.path.join(localdir, os.path.basename(src))
        s3t.download(
            bucketname, src, dst,
            subscribers=[
                s3transfer.ProgressCallbackInvoker(progress_func.update),
            ],
        )
    s3t.shutdown()  # wait for all the upload tasks to finish
