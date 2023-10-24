import subprocess
import os

PATH_TO_PYAWS = ""

def cp_recursive(
    source_dir: str, 
    save_dir: str,
    profile: str,
    generate_logfile_to: str | None=None,
    path_to_bash: str | None=None
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
    path_to_bash: str, default None
        The path to the underlying bash script being called. It default to where
        `pyaws` if `pyaws` is saved to where python looks for the libraries,
        ie in the smae folder that `pip show pip | awk '/Location/ {print $2}'`
        points too.

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



#--------------------------------------------------
#--------------------------------------------------
#--------------------------------------------------

source_dir = "/home/nicholas/Datasets/CelebA/batched"
num_b = sum([os.stat(os.path.join(source_dir, f)).st_size for f in os.listdir(source_dir)])
save_dir = "s3://speed-demo-bucket/imgs"
profile = "nick"
path_to_bash = "/home/nicholas/GitRepos/pyaws/transfer/scripts/awscp.sh"

p = subprocess.Popen(
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
        stderr=subprocess.PIPE,
        # bufsize=1,
        universal_newlines=True
)

stdout, stderr = p.communicate()
stdout = stdout.split("\n")

len(stdout)



p = subprocess.run(
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
        stderr=subprocess.PIPE,
)

p.stdout




