import subprocess
import ansiwrap

class SCPContext:
    def __init__(self, path_to_bash, port, source_path, save_path, user, ip):
        self.command = [
            "script",
            "-q",  # Quiet mode
            "-e",  # Exit after the child process exits
            "-c",  # Command to execute
            f"{path_to_bash} --port {port} --source-path {source_path} --save-path {save_path} --user {user} --ip {ip}"
        ]
        self.process = None

    def __enter__(self):
        # Start the process using Popen with stdout as PIPE
        self.process = subprocess.Popen(
            self.command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        return self.process

    def __exit__(self, exc_type, exc_value, traceback):
        if self.process:
            # Ensure process is finished
            self.process.communicate()

# Usage:

port = "22"
source_path = "/home/nicholas/GitRepos/pyaws/test/scp/move"
save_path = "/home/ubuntu/movedir"
user = "ubuntu"
ip = "50.18.80.35"
path_to_bash = "/home/nicholas/GitRepos/pyaws/transfer/scripts/scp.sh"


with SCPContext(path_to_bash, port, source_path, save_path, user, ip) as process:
    output = process.stdout.read().decode('utf-8')
    line = output.split('\n')
    for line in iter(process.stdout.readline, ''):
        line = ''.join(ch if ch.isprintable() else f"[{ord(ch):03d}]" for ch in line)
        if line.startswith("move"):
            print(line.strip()[:10])


_lines = []
with SCPContext(path_to_bash, port, source_path, save_path, user, ip) as process:
    output = process.stdout.read()
    lines = output.split('\r')  # Split by carriage return since that's what scp uses
    for line in lines:
        clean_line = ''.join(ch if ch.isprintable() else '' for ch in line)  # Strip non-printable characters
        if clean_line.startswith("move"):
            _lines.append(clean_line)
            print(clean_line.strip())
