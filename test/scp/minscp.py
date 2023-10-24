import subprocess

path_to_bash = "./minscp.sh"

p = subprocess.Popen(
    [
        path_to_bash, 
    ],
    stdout=subprocess.PIPE,
)


with subprocess.Popen(
    [
        path_to_bash, 
    ],
    stderr=subprocess.PIPE,
    universal_newlines=True
    ) as p:
    for i, line in enumerate(p.stderr):
        if line.startswith("Sending"):
            f =line.split(" ")[-1]
            print(f"{i} : {f}", end="")


with subprocess.Popen(
    [
        path_to_bash, 
    ],
    stderr=subprocess.PIPE,
    stdout=subprocess.PIPE,
    bufsize=1,
    universal_newlines=True
    ) as p:
    count = 1
    for line in p.stderr:
        if line.startswith("Sending"):
            f =line.split(" ")[-1]
            print(f"{count} : {f}", end="")
            print('\033[1A', end='\x1b[2K')
            count += 1

