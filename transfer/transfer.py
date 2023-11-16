import subprocess
import os
from typing import Optional
import botocore
import boto3
import boto3.s3.transfer as s3transfer
from tqdm import tqdm
import time

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
TRANSFER_SCRIPT_PATH = os.path.join(PATH_TO_PYAWS, 'transfer', 'scripts')

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
    source_path: str
        Either a path to a file or a folder contating files. If `source_path` 
        is a folder, than all files in the folder will be transfered.

    save_path: str
        The location on the remote host where you want the files moved to.

    user: str,
        The user of the remote machine

    ip: str,
        The ip address of the remote machine

    port: str, default = 22
        The port you want to scp with

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
            TRANSFER_SCRIPT_PATH, 'scp.sh'
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

