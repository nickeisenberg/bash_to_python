import subprocess
import os
from typing import Optional
from tqdm import tqdm
from .utils import list_files_recursively
import importlib.resources as pkg


class SecureCopyProtocol:
    """
    A call to `scp`.

    Parameters
    ----------
    user: str,
        The user of the remote machine

    ip: str,
        The ip address of the remote machine

    port: str, default = 22
        The port you want to scp with

    pem: Optional[str]=None
        The pem key to access the remote machine

    path_to_bash: Optional[str]=None
        The path to the underlying bash script being called. If None then it 
        assumes that the `pyaws` module is located where python looks for the libraries,
        ie in the same folder that `pip show pip | awk '/Location/ {print $2}'`.



    """
    def __init__(self, user, ip, port, pem=None, path_to_bash=None):
        self.user = user
        self.ip = ip
        self.port = port
        self.pem = pem
        if path_to_bash is None:
            self.path_to_bash = str(
                pkg.path('sshtools.transfer.scripts', 'scp.sh')
            )
        else:
            self.path_to_bash = path_to_bash

    def scp(self,
            source_path: str, 
            save_path: str,
            with_tqdm: bool = True,
            measure_by: Optional[str]="count",
            generate_logfile_to: Optional[str]=None):
        """
        Parameters
        ----------
        source_path: str
            Either a path to a file or a folder contating files. If `source_path` 
            is a folder, than all files in the folder will be transfered.

        save_path: str
            The location on the remote host where you want the files moved to.


        progress_bar: Optional[tqdm]=None
            A tqdm progress bar

        measure_by : Optional[str]=None, default="count"
            The metric used to measure the speed with the tqdm bar. The current 
            options are "count", "KiB", and "MiB".

        generate_logfile_to: Optional[str]=None
            The path you would like a complete log file of the output of `scp`.

        Example
        -------
        >>> from sshtools.transfer import SecureCopyProtocol
        >>> 
        >>> user = "remote_user"
        >>> ip = "50.1.1.1"
        >>> port = "22"
        >>> pem = "/path/to/pem/credentials.pem"
        >>> scp = SecureCopyProtocol(user, ip , port, pem)
        >>>
        >>> source_path = "/path/to/local/folder"
        >>> save_path = "/path/to/remote/save/destination"
        >>> logfile = "/where/to/save/log/test.log"
        >>> 
        >>> scp.scp(
        >>>     source_path, 
        >>>     save_path, 
        >>>     generate_logfile_to=logfile,
        >>> )
        """

        num_files = 1
        if os.path.isdir(source_path):
            all_files = list_files_recursively(source_path)
            num_files = len(all_files)
        
        if self.pem is not None:
            command = [
                self.path_to_bash, 
                "--port", 
                self.port, 
                "--source-path", 
                source_path, 
                "--save-path", 
                save_path, 
                "--user", 
                self.user, 
                "--ip", 
                self.ip,
                "--pem",
                self.pem
            ]
        else:
            command = [
                self.path_to_bash, 
                "--port", 
                self.port, 
                "--source-path", 
                source_path, 
                "--save-path", 
                save_path, 
                "--user", 
                self.user, 
                "--ip", 
                self.ip, 
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
                
                if with_tqdm:
                    progress_bar = tqdm(
                        desc='upload', ncols=60, total=num_files, 
                        unit='files', unit_scale=1, leave=True
                    )

                count = 1
                current_file = ""
                file_size = 0.
                for line in p.stderr:
                    if line.startswith("Sending"):
                        current_file =line.split(" ")[-1]
                        file_size =float(line.split(" ")[-2])

                    # if "100%" in line:
                    #     current_file =line.split(" ")[0]
                    #     file_size =float(line.split(" ")[2])

                        if not with_tqdm:
                            print(f"{count} / {num_files} : {current_file}", end="")
                            print('\033[1A', end='\x1b[2K')
                            count += 1

                        else:
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
