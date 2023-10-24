"""
scp prints to stderr not stdout. wtf.
"""

import subprocess
import os
import time


def scp(
    port: str, 
    source_path: str, 
    save_path: str,
    user: str,
    ip: str,
    pem: str | None=None,
    generate_logfile_to: str | None=None,
    path_to_bash: str | None=None
    ):
    
    num_files = 1
    if os.path.isdir(source_path):
        num_files = len(os.listdir(source_path))

    if path_to_bash is None:
        path_to_bash = os.path.join(
            PATH_TO_PYAWS, 'scripts', 'scp.sh'
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
            for line in p.stderr:
                if line.startswith("Sending"):
                    f =line.split(" ")[-1]
                    print(f"{count} / {num_files} : {f}", end="")
                    print('\033[1A', end='\x1b[2K')
                    count += 1

                if generate_logfile_to is not None:
                    with open(generate_logfile_to, "a") as log:
                        _ = log.write(line + "\n")

            print("All files successfully transfered")

    except subprocess.CalledProcessError as e:
        print(f"Error calling the Bash script: {e}")

    except FileNotFoundError as e:
        print(f"Bash script not found: {e}")

    return None


port = "22"
source_path = "/home/nicholas/GitRepos/pyaws/test/scp/move"
save_path = "/home/ubuntu/movedir"
user = "ubuntu"
ip = "50.18.80.35"
path_to_bash = "/home/nicholas/GitRepos/pyaws/transfer/scripts/scp.sh"
logfile = "/home/nicholas/test.log"
pem = "/home/nicholas/.credentials/keypairs/us-west-1-kp.pem"

scp(
    port, 
    source_path, 
    save_path, 
    user, 
    ip,
    pem=pem,
    generate_logfile_to=logfile,
    path_to_bash=path_to_bash
)




with subprocess.Popen(
    [
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
    ],
    # stderr=subprocess.PIPE,
    # bufsize=1,
    # universal_newlines=True
) as p:








