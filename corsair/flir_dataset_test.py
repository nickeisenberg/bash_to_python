from torch.utils.data import Dataset
import os
import json
from torchvision import transforms
from torch import Tensor
from typing import Tuple, List, TypedDict
from torch.utils.data import DataLoader
from PIL import Image
import torch
from typing import TypeAlias


class FlirLabel(TypedDict):
    bounding_boxes: List[Tensor]
    labels: List[Tensor]


FlirDatapoint: TypeAlias = Tuple[str, FlirLabel]


class FlirDataset(Dataset):

    def __init__(self, main_dir, dataset_type: str, mode: str, transforms=transforms.Compose([
            transforms.ToTensor()])):

        modes = ['rgb', 'thermal']
        dataset_types = ['train', 'val', 'test']
        self.dataset = {}
        self.transforms = transforms
        if mode not in modes:
            print(
                f'Mode {mode} is not supported in the FLIR dataset, supported modes are {modes}')
        if dataset_type not in dataset_types:
            print(
                f'{dataset_type} is not a valid types, valid types are{dataset_types}')
        train_flag = dataset_type in ['train', 'val']
        if train_flag:
            self.data_dir_name = os.path.join(
                main_dir, 'images_' + mode + '_' + dataset_type)
        else:
            self.data_dir_name = os.path.join(
                main_dir, 'video_' + mode + '_test')
        json_path = os.path.join(self.data_dir_name, 'coco.json')
        f = open(json_path)
        flir_data = json.load(f)
        f.close()
        images = flir_data['images']
        anno = flir_data['annotations']
        self._unpack_flir(images, anno)
        self._class_map = None

    def __getitem__(self, index):
        print(self.dataset[index])
        data = self.dataset[index]
        image = Image.open(data[0])
        image = self.transforms(image)
        output = data[1]

        return image, output

    @staticmethod
    def collate_fn(batch):
        images = list()
        boxes = list()
        labels = list()

        for b in batch:
            temp_boxes = b[1]['bounding_boxes']
            temp_labels = b[1]['labels']
            images.append(b[0])
            boxes.append(temp_boxes)
            labels.append(temp_labels)
        images = torch.stack(images, dim=0)
        return images, boxes, labels

    def _unpack_flir(self, images, anno):
        '''
        method responsable for gathering flir data
        for each annotation grab image id, based on that id collect all bounding
        boxes and image labels.

        data is formated as {image_id: [image, output_dict]}
        output_dict = {'bounding_boxes': [[bounding_box]],
        'labels': [ label]
        }
        bounding_box[i] has label label[i]
        '''
        image_index = 0
        bb_list = []
        label_list = []
        current_image_path = os.path.join(
            self.data_dir_name, images[image_index]['file_name'])
        for ann in anno:
            if ann['image_id'] == images[image_index]['id']:
                bb_list.append(self.format_bb(ann['bbox']))
                label_list.append(self.format_label(ann['category_id']))
            else:
                datapoint: FlirDatapoint = self.create_flir_datapoint(
                    current_image_path, bb_list, label_list)
                self.update_dataset(image_index, datapoint)
                image_index += 1
                current_image_path = os.path.join(
                    self.data_dir_name, images[image_index]['file_name']
                )
                bb_list = [ann['bbox']]
                label_list = [ann['category_id']]
        datapoint: FlirDatapoint = self.create_flir_datapoint(
            current_image_path, bb_list, label_list)
        self.update_dataset(image_index, label_list)

    def update_dataset(self, image_index: int, datapoint: FlirDatapoint):
        self.dataset[image_index] = datapoint

    @ staticmethod
    def format_bb(bounding_box: List[int]):
        return Tensor(bounding_box)

    @ staticmethod
    def format_label(label: int):
        return Tensor([label])

    @ staticmethod
    def format_label_list(label_list: List[int]):
        return Tensor(label_list)

    @ staticmethod
    def create_flir_datapoint(image_path: str, bb_list: List, labels: List) -> FlirDatapoint:
        flir_labels: FlirLabel = {'bounding_boxes': [Tensor(bb) for bb in bb_list],
                                  'labels': labels}

        return (image_path, flir_labels)

    def __len__(self): return len(self.dataset)


if __name__ == '__main__':
    test = FlirDataset(main_dir=os.path.join(os.getcwd(), '_data','FLIR_ADAS_v2'),
                       dataset_type='train',
                       mode='thermal'
                       )

    test_loader = DataLoader(
        test, batch_size=10, shuffle=True, collate_fn=test.collate_fn)
    for i, data in enumerate(test_loader):
        print(data)
# single example of plotting a box
# write a function for this
# [533, 114, 17, 44]
# y_min = 114
# x_min = 533
# p[0, y_min, x_min+width] = 0
# p[0, y_min, x_min:x_min+width] = 0
# p[0, y_min:y_min+height, x_min+width] = 0
# p[0, y_min+height, x_mind:x_min+width] = 0dat

    # @ staticmethod
    # def unpack_data(data) -> Tuple[Tensor, FlirLabel]:

    #     output = data[1]
    #     bounding_boxes = output['bounding_boxes']
    #     labels = output['labels']
    #     inputs = image
    #     outputs = (bounding_boxes, labels)
    #     return inputs, outputs


def help_me(images):
    for i, image in enumerate(images):
        if i != image['id']:
            print(i)
            print(image)
            break
