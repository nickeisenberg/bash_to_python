from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from ..transfer import scp
import subprocess
from typing import Optional
import os

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

def start_trigger(
        path_to_image_folder: str, 
        path_to_bash: Optional[str]=None
        ):

    if path_to_bash is None:
        path_to_bash = os.path.join(
            PATH_TO_PYAWS, 'plotting', 'trigger.sh'
        )

    command = [
        path_to_bash,
        "--folder",
        path_to_image_folder
    ]
    
    print("Creating the trigger. This will run indefinatly. Use <C-c> to stop")
    subprocess.run(
        command
    )


class Plotter:

    def __init__(
            self,
            user: str,
            ip: str,
            save_path: str,
            port: str="22", 
            pem: Optional[str]=None,
            path_to_bash: Optional[str]=None
        ):

        self.user = user
        self.ip = ip
        self.save_path = save_path
        self.port = port
        self.pem = pem
        self.path_to_bash = path_to_bash
    

    def show(
        self, 
        name: str, 
        figure: Figure
        ):
        
        if os.path.isfile(f"./{name}.png"):
            try:
                figure.savefig(f"./___{name}.png")
            except:
                print("file name already exists")
                return None
        else:
            figure.savefig(f"./{name}.png")

        scp(
            source_path=f"./{name}.png",
            save_path=self.save_path,
            user=self.user,
            ip=self.ip,
            port=self.port,
            pem=self.pem,
            path_to_bash=self.path_to_bash
        )

        os.remove(f"./{name}.png")

        return None
