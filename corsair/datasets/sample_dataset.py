from PIL import Image
from torchvision import transforms
from torch.utils.data import Dataset
import os
from typing import List, Tuple
from torch import Tensor

from experiments.util import default_unpacker


class BaseSampleDataset(Dataset):
    def __init__(self, style: str, main_dir: str, transforms=transforms.Compose([
            transforms.CenterCrop(64),
            transforms.ToTensor()]),
            criterion=None):
        image_directory = os.path.join(main_dir, style)
        self.dataset: Tuple[Tensor, int] = []

        self._class_names: List[str] = ['2s1', 'bmp2',
                                       'btr70', 'm1',
                                       'm2', 'm35',
                                       'm60', 'm548',
                                       't72', 'zsu23'
                                       ]
        self.unpack_data = default_unpacker

        for path, directories, files in os.walk(image_directory):
            for i, file in enumerate(files):
                label = self.get_label(file.split('_')[0])
                add_flag = criterion(file, i) if criterion else True
                image_path = os.path.join(path, file)
                image = Image.open(image_path)
                image = transforms(image)
                temp = (image, label)
                if add_flag:
                    self.dataset.append(temp)
 

    def __getitem__(self, indx):
        return self.dataset[indx]

    def __len__(self):
        return len(self.dataset)


