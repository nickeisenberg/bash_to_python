import subprocess
import os
import time


def scp(
    port: str, 
    source_path: str, 
    save_path: str,
    user: str,
    ip: str,
    generate_logfile_to: str | None=None,
    path_to_bash: str | None=None
    ):


    # if path_to_bash is None:
    #     path_to_bash = os.path.join(
    #         PATH_TO_PYAWS, 'scripts', 'scp.sh'
    #     )

    try:
        # Call the Bash script with specified parameters
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
            stdout=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        ) as p:
            for line in p.stdout:
                print('hello')
                print(line[2])
                time.sleep(1)
                # if generate_logfile_to is not None:
                #     with open(generate_logfile_to, "a") as log:
                #         _ = log.write(line + "\n")

    except subprocess.CalledProcessError as e:
        print(f"Error calling the Bash script: {e}")

    except FileNotFoundError as e:
        print(f"Bash script not found: {e}")

    return None

port = "2222"
source_path = "/home/ubuntu/pyscripts/scp/share/"
save_path = "/home/nicholas/"
user = "nicholas"
ip = "174.72.155.21"
path_to_bash = "/home/ubuntu/pyscripts/scp/scp.sh"


scp(
    port, 
    source_path, 
    save_path, 
    user, 
    ip, 
    path_to_bash=path_to_bash
)

os.listdir("/home/ubuntu/pyscripts/scp")



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
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
    ) as p:
    stdout, stderr = p.communicate()
    stdout = stdout.split("\n")
    for line in p.stdout:
        print(line)
    
p = subprocess.Popen(
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
    ]
)
