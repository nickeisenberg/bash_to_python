import subprocess

path_to_bash = "./minscp.sh"

p = subprocess.run(
    [
        path_to_bash, 
    ],
)

with subprocess.Popen(
    [
        path_to_bash, 
    ],
    stderr=subprocess.PIPE,
    bufsize=1,
    universal_newlines=True
) as p:
    for line in p.stderr:
        print(line)

with subprocess.Popen(
    [
        path_to_bash, 
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
    ) as p:
    stdout, stderr = p.communicate()
    stdout = stdout.split("\n")
    for line in p.stdout:
        print(line)

