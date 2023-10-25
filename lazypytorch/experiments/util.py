
from typing import Tuple, Any, List
from torch import Tensor


def optional(function):
    def wrap(*args, **kwargs):
        return function(*args, **kwargs)
    return wrap


############### Dataset utils##################
# I want to put all dataset into their own directory
# and give them their own interface

def add_class_names(cls, class_names: List[str]) -> None:
    cls._class_names = class_names

def default_unpacker(data, device: str) -> Tuple[Tensor, Any]:
    return data[0].to(device), data[1].to(device)

def add_data_unpacker(cls, data_unpacker: callable) -> None:
    cls.unpack_data = data_unpacker
