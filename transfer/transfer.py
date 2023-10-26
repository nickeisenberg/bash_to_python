import subprocess
import os
from typing import Optional
import botocore
import boto3
import boto3.s3.transfer as s3transfer
from tqdm import tqdm

#--------------------------------------------------
# Get the path to the pyaws folder. This allows the bash scripts to be called
# without have the python compiler opened in the pyaws folder

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

#--------------------------------------------------

def scp(
        source_path: str, 
        save_path: str,
        user: str,
        ip: str,
        port: str="22", 
        progress_bar: Optional[tqdm]=None,
        measure_by: Optional[str]="count",
        pem: Optional[str]=None,
        generate_logfile_to: Optional[str]=None,
        path_to_bash: Optional[str]=None
        ):

    """
    A call to `scp`.

    Parameters
    ----------
    port: str, default = 22
        The port you want to scp with

    source_path: str
        Either a path to a file or a folder contating files. If `source_path` 
        is a folder, than all files in the folder will be transfered.

    save_path: str
        The location on the remote host where you want the files moved to.

    user: str,
        The user of the remote machine

    ip: str,
        The ip address of the remote machine

    progress_bar: Optional[tqdm]=None
        A tqdm progress bar

    measure_by : Optional[str]=None, default="count"
        The metric used to measure the speed with the tqdm bar. The current 
        options are "count", "KiB", and "MiB".

    pem: Optional[str]=None
        The pem key to access the remote machine

    generate_logfile_to: Optional[str]=None
        The path you would like a complete log file of the output of `scp`.

    path_to_bash: Optional[str]=None
        The path to the underlying bash script being called. If None then it 
        assumes that the `pyaws` module is located where python looks for the libraries,
        ie in the same folder that `pip show pip | awk '/Location/ {print $2}'`.

    Returns
    -------
    None

    Example
    -------
    >>> from pyaws.transfer import scp
    >>> 
    >>> port = "22"
    >>> source_path = "/path/to/local/folder"
    >>> save_path = "/path/to/remote/save/destination"
    >>> user = "remote_user"
    >>> ip = "50.1.1.1"
    >>> path_to_bash = "/path/to/scp/script/script.sh"
    >>> logfile = "/where/to/save/log/test.log"
    >>> pem = "/path/to/pem/credentials.pem"
    >>> 
    >>> scp(
    >>>     port, 
    >>>     source_path, 
    >>>     save_path, 
    >>>     user, 
    >>>     ip,
    >>>     pem=pem,
    >>>     generate_logfile_to=logfile,
    >>>     path_to_bash=path_to_bash
    >>> )
    """
    
    num_files = 1
    if os.path.isdir(source_path):
        num_files = len(os.listdir(source_path))

    if path_to_bash is None:
        path_to_bash = os.path.join(
            PATH_TO_PYAWS, 'transfer', 'scripts', 'scp.sh'
        )

    
    if pem is not None:
        command = [
            path_to_bash, 
            "--port", 
            port, 
            "--source-path", 
            source_path, 
            "--save-path", 
            save_path, 
            "--user", 
            user, 
            "--ip", 
            ip,
            "--pem",
            pem
        ]
    else:
        command = [
            path_to_bash, 
            "--port", 
            port, 
            "--source-path", 
            source_path, 
            "--save-path", 
            save_path, 
            "--user", 
            user, 
            "--ip", 
            ip, 
        ]

    try:
        # Call the Bash script with specified parameters
        with subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        ) as p:

            count = 1
            current_file = ""
            file_size = 0.
            for line in p.stderr:
                if line.startswith("Sending"):
                    current_file =line.split(" ")[-1]
                    file_size =float(line.split(" ")[-2])
                    print(f"{count} / {num_files} : {current_file}", end="")
                    print('\033[1A', end='\x1b[2K')
                    count += 1

                if progress_bar is not None:
                    if measure_by == "count":
                        progress_bar.update(1)
                    elif measure_by == "KiB":
                        progress_bar.update(file_size / 1000)
                    elif measure_by == "MiB":
                        progress_bar.update(file_size / 1000000)

                if generate_logfile_to is not None:
                    with open(generate_logfile_to, "a") as log:
                        _ = log.write(line + "\n")

            print("All files successfully transfered")

    except subprocess.CalledProcessError as e:
        print(f"Error calling the Bash script: {e}")

    except FileNotFoundError as e:
        print(f"Bash script not found: {e}")

    return None


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


#--------------------------------------------------
# Depreciated below. Will delete soon
#--------------------------------------------------

def sync_dir(
    source_dir, 
    # bucket_name,
    save_dir,
    profile,
    notify_after=0
    ):

    """
    DEPRECIATED

    A python function that calls a bash function that applies 
    aws s3 sync on a whole local directory. According to the internet
    aws s3 cp is faster aws s3 sync and I believe both of these are faster than
    using boto3 functions directly to move files from local to s3. However, 
    sync seems to be just as fast as cp. I think sync is mainly for when you 
    dont want to overwrite files already in a bucket. Sync will not copy the 
    file over if it already exists so if you are moving alot of files then sync 
    may take some extra time making sure that it does not move files over that 
    are already there. I could be wrng about this.

    Parameters
    ----------
    source_dir: str
        The full file path to the local dir containing the files that need to be
        moved to s3.
    bucket_name: str
        Just the name of the s3 bucket. In other words, <bucket_name> and not
        s3://<bucket_name>.
        
    profile: str
        The name of the profile that is configured with aws configure
    notify_after: str default 0
        This will return a status message to the python interpreter after each
        "notify_after" file shave been uploaded. 0 will silent all notifiations.

    Returns
    -------
    None


    Example
    -------
    source_dir = '/home/nicholas/Datasets/CelebA/img_64_10'
    save_dir = 's3://celeba-demo-bucket'
    profile = "nick"
    notify_after = 2

    pyaws.copy_dir_to_s3(
        source_dir,
        save_dir,
        profile,
        notify_after
    )
    """
    
    # path_to_bash = "/home/nicholas/GitRepos/aws/pyaws/scripts"
    # path_to_bash = "./scripts"
    # path_to_bash += "/sync_dir.sh"
    path_to_bash = os.path.join(
        PATH_TO_PYAWS, 'scripts', 'depreciated', 'sync_dir.sh'
    )

    try:
        # Call the Bash script with specified parameters
        with subprocess.Popen(
            [
                path_to_bash, 
                "--source-dir", 
                source_dir, 
                # "--bucket-name", 
                # bucket_name, 
                "--save-dir", 
                save_dir, 
                "--profile", 
                profile, 
                "--notify-after", 
                str(notify_after)
            ],
            stdout=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        ) as p:
            for line in p.stdout:
                print(line, end='')


    except subprocess.CalledProcessError as e:
        print(f"Error calling the Bash script: {e}")
    except FileNotFoundError as e:
        print(f"Bash script not found: {e}")

    return None


def copy_dir(
    source_dir, 
    save_dir,
    profile,
    notify_after=0
    ):

    """
    DEPRECIATED

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
    notify_after: str default 0
        This will return a status message to the python interpreter after each
        "notify_after" file shave been uploaded. 0 will silent all notifiations.

    Returns
    -------
    None
    
    Example
    -------

    source_dir = '/home/nicholas/Datasets/CelebA/img_64_10'
    save_dir = 's3://celeba-demo-bucket'
    profile = "nick"
    notify_after = 2

    pyaws.copy_dir_to_s3(
        source_dir,
        save_dir,
        profile,
        notify_after
    )
    """

    # path_to_bash = "/home/nicholas/GitRepos/aws/pyaws/scripts"
    # path_to_bash = "./scripts"
    # path_to_bash += "/copy_dir.sh"
    path_to_bash = os.path.join(
        PATH_TO_PYAWS, 'scripts', 'depreciated', 'copy_dir.sh'
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
                "--notify-after", 
                str(notify_after)
            ],
            stdout=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        ) as p:
            for line in p.stdout:
                print(line, end='')

    except subprocess.CalledProcessError as e:
        print(f"Error calling the Bash script: {e}")

    except FileNotFoundError as e:
        print(f"Bash script not found: {e}")

    return None
