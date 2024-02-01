import subprocess
import os
from typing import Optional
from tqdm import tqdm
from .utils import count_all_files
from platform import system
import importlib.resources as pkg
import re


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


    """
    def __init__(self, user, ip, port, pem=None):
        self.user = user
        self.ip = ip
        self.port = port
        self.pem = pem
        
        self._system = system()

        if self._system not in ["Linux", "Darwin"]:
            raise Exception("Operating system in not supported")

    def put(self,
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
        >>> from shwrap.transfer import SecureCopyProtocol
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

        if self._system == "Linux":
            path_to_bash = str(
                pkg.path('shwrap.transfer._scripts.linux', 'send.sh')
            )
        elif self._system == "Darwin":
            path_to_bash = str(
                pkg.path('shwrap.transfer._scripts.darwin', 'send.sh')
            )
        else:
            raise Exception("Operating system in not supported")

        num_files = 1
        if os.path.isdir(source_path):
            num_files = count_all_files(source_path)
        
        if self.pem is not None:
            command = [
                path_to_bash, 
                "--port", self.port, 
                "--source-path", source_path, 
                "--save-path", save_path, 
                "--user", self.user, 
                "--ip", self.ip,
                "--pem", self.pem
            ]
        else:
            command = [
                path_to_bash, 
                "--port", self.port, 
                "--source-path", source_path, 
                "--save-path", save_path, 
                "--user", self.user, 
                "--ip", self.ip, 
            ]

        try:
            with subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                universal_newlines=True
            ) as p:
                
                progress_bar = None
                if with_tqdm:
                    progress_bar = tqdm(
                        desc='upload', ncols=60, total=num_files, 
                        unit='files', unit_scale=1, leave=True
                    )

                count = 1
                
                if self._system == 'Darwin':
                    if with_tqdm is False:
                        raise Exception("At the momemnt, Darwin OS requires tqdm")

                    success = self._darwin(p.stdout, progress_bar, generate_logfile_to,
                                 count, num_files, measure_by, with_tqdm)

                elif self._system == "Linux":
                    success = self._linux(p.stderr, progress_bar, generate_logfile_to,
                                 count, num_files, measure_by, with_tqdm)

                else:
                    success = "Operating system not supported"
                    
                if success:
                    print(f"\n \n {success}")
                else:
                    print("\n \n Process successfully completed")

        except subprocess.CalledProcessError as e:
            print(f"Error calling the Bash script: {e}")

        except FileNotFoundError as e:
            print(f"Bash script not found: {e}")

        return None

    def get(self,
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
        >>> from shwrap.transfer import SecureCopyProtocol
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

        if self._system == "Linux":
            path_to_bash = str(
                pkg.path('shwrap.transfer._scripts.linux', 'receive.sh')
            )
        elif self._system == "Darwin":
            path_to_bash = str(
                pkg.path('shwrap.transfer._scripts.darwin', 'receive.sh')
            )
        else:
            raise Exception("Operating system in not supported")

        num_files = 1
        if os.path.isdir(source_path):
            num_files = count_all_files(source_path)
        
        if self.pem is not None:
            command = [
                path_to_bash, 
                "--port", self.port, 
                "--source-path", source_path, 
                "--save-path", save_path, 
                "--user", self.user, 
                "--ip", self.ip,
                "--pem", self.pem
            ]
        else:
            command = [
                path_to_bash, 
                "--port", self.port, 
                "--source-path", source_path, 
                "--save-path", save_path, 
                "--user", self.user, 
                "--ip", self.ip, 
            ]

        try:
            with subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                universal_newlines=True
            ) as p:
                
                progress_bar = None
                if with_tqdm:
                    progress_bar = tqdm(
                        desc='upload', ncols=60, total=num_files, 
                        unit='files', unit_scale=1, leave=True
                    )

                count = 1

                if self._system == 'Darwin':
                    if with_tqdm is False:
                        raise Exception("At the momemnt, Darwin OS requires tqdm")

                    success = self._darwin(p.stdout, progress_bar, generate_logfile_to,
                                 count, num_files, measure_by, with_tqdm)

                elif self._system == "Linux":
                    success = self._linux(p.stderr, progress_bar, generate_logfile_to,
                                 count, num_files, measure_by, with_tqdm)

                else:
                    success = "Operating system not supported"
                
                if success:
                    print(f"\n \n {success}")
                else:
                    print("Process sucessfully completed")

        except subprocess.CalledProcessError as e:
            print(f"Error calling the Bash script: {e}")

        except FileNotFoundError as e:
            print(f"Bash script not found: {e}")

        return None
    
    @staticmethod
    def _darwin(stdout, progress_bar, generate_logfile_to, count, 
                num_files, measure_by, with_tqdm):
        """
        darwin logic
        """

        for line in stdout:
            if "100%" in line:
                s_line = line.strip().split()
                current_file = s_line[0]
                file_size = float(s_line[2])

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


    @staticmethod
    def _linux(stderr, progress_bar, generate_logfile_to, count, 
                num_files, measure_by, with_tqdm):
        """
        linux logic
        """

        for line in stderr:
            if "Permission denied" in line:
                return "Permission denied. Check the pem file."
            if line.startswith("Sending"):
                current_file =line.split(" ")[-1]
                file_size =float(line.split(" ")[-2])

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
