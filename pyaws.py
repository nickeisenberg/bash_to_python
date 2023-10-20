import subprocess
import os
import botocore
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

def copy_dir(
    source_dir, 
    save_dir,
    profile,
    notify_after=0
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
        PATH_TO_PYAWS, 'scripts', 'copy_dir.sh'
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


def cp_recursive(
    source_dir, 
    save_dir,
    profile,
    notify_after = 1
    ):

    """
    Link to overwrite previously printed lines

    https://itnext.io/overwrite-previously-printed-lines-4218a9563527

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
    )
    """

    path_to_bash = os.path.join(
        PATH_TO_PYAWS, 'scripts', 'awscp.sh'
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
            count = 0
            for line in p.stdout:
                count += 1 
                if count % notify_after == 0:
                    line = line.split(" ")[:6]
                    message = "PROGRESS " 
                    message += str.join(" ", line[1:4]) 
                    message += "    SPEED " 
                    message += str.join(" ", line[4:])
                    print(message, end='\n')
                    print('\033[1A', end='\x1b[2K')

    except subprocess.CalledProcessError as e:
        print(f"Error calling the Bash script: {e}")

    except FileNotFoundError as e:
        print(f"Bash script not found: {e}")

    return None


def sync_dir(
    source_dir, 
    # bucket_name,
    save_dir,
    profile,
    notify_after=0
    ):

    """
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
        PATH_TO_PYAWS, 'scripts', 'sync_dir.sh'
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



def sync(
    source_dir, 
    save_dir,
    profile,
    notify_after = 1
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
    )
    """

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
            count = 0
            for line in p.stdout:
                count += 1 
                if count % notify_after == 0:
                    line = line.split(" ")[:6]
                    message = "PROGRESS " 
                    message += str.join(" ", line[1:4]) 
                    message += "    SPEED " 
                    message += str.join(" ", line[4:])
                    print(message, end='\n')

    except subprocess.CalledProcessError as e:
        print(f"Error calling the Bash script: {e}")

    except FileNotFoundError as e:
        print(f"Bash script not found: {e}")

    return None



def fast_upload(
    session, 
    bucketname, 
    s3dir, 
    filelist, 
    progress_func, 
    workers=20,
    ):
    """
    Taken from...
    https://stackoverflow.com/questions/56639630/how-can-i-increase-my-aws-s3-upload-speed-when-using-boto3

    Parameters
    ----------
    session: boto3.session()
    bucketname: str
    s3dir: str
        the folder path within the bucket
    filelist:
        list of local files to be moved to the bucket
    progress_func: tqdm
    workers: int

    Example
    -------
    from tqdm import tqdm
    import pyaws
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
        region_name="us-east-1"
    )
    bucketname = 'celeba-demo-bucket'
    s3dir = 'imgs'
    filelist = [os.path.join(source_dir, f) for f in os.listdir(source_dir)]
    totalsize = sum([os.stat(f).st_size for f in filelist])
    
    with tqdm(
        desc='upload', ncols=60, total=totalsize, unit='B', unit_scale=1
    ) as pbar:
        fast_upload(session, bucketname, s3dir, filelist, pbar.update, workers=50)
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
                s3transfer.ProgressCallbackInvoker(progress_func),
            ],
        )
    s3t.shutdown()  # wait for all the upload tasks to finish





def fast_download(
    session, 
    bucketname, 
    keylist, 
    localdir, 
    progress_func, 
    workers=20,
    ):
    """
    Taken from...
    https://stackoverflow.com/questions/56639630/how-can-i-increase-my-aws-s3-upload-speed-when-using-boto3

    Parameters
    ----------
    session: boto3.session()
    bucketname: str
    keylist: str
        the full key of the object in the bucket you want downloaded
    localdir:
        the full path on your local machine where you want the data downloaded to
    progress_func: tqdm
    workers: int

    Example
    -------
    from tqdm import tqdm
    import pyaws
    import os
    import time
    import os
    import boto3
    import json
    
    with open("/home/nicholas/.credentials/password.json") as oj:
        pw = json.load(oj)
    
    ACCESS_KEY = pw['aws_ACCESS_KEY_nick']
    SECRET_ACCESS_KEY = pw['aws_SECRET_ACCESS_KEY_nick']

    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_ACCESS_KEY,
        profile_name="nick",
        region_name="us-east-1"
    )

    s3_res = session.resource('s3')
    bucketname = 'speed-demo-bucket'
    bucket = s3_res.Bucket(bucketname)
    bucket_objects = [
        x.key 
        for x in bucket.objects.filter(Prefix="imgs/") 
        if x.key.endswith('jpg')
    ]
    object_sizes = [
        x.size 
        for x in bucket.objects.filter(Prefix="imgs/") 
        if x.key.endswith('jpg')
    ]
    totalsize = sum(object_sizes)
    localdir = "/home/nicholas/Datasets/CelebA/ret"
    
    with tqdm(
        desc='download', ncols=60, total=totalsize, unit='B', unit_scale=1
    ) as pbar:
        pyaws.fast_download(
            session, 
            bucketname, 
            bucket_objects, 
            localdir, 
            pbar.update, 
            workers=20
        )
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
                s3transfer.ProgressCallbackInvoker(progress_func),
            ],
        )
    s3t.shutdown()  # wait for all the upload tasks to finish



