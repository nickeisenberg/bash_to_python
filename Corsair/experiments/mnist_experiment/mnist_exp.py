from torch.utils.data import DataLoader
from experiments.experiment_bases import ClassifierExperiment
from experiments.network_templates import Classifier

from experiments.util import add_class_names, add_data_unpacker, default_unpacker

import torchvision


class MNISTClassifierExperiment(ClassifierExperiment):

    def __init__(self, neural_net: Classifier, save_root: str,
                 train_batch_size: int = 100,
                 test_batch_size: int = 100,
                 number_of_epochs: int = 4,
                 name: str = 'mnist-experiment',
                 trial_number: int = 1, device: str = 'cpu'
                 ):
        save_file_name = name + neural_net.name
        class_names = [f'digit {i}' for i in range(10)]

        train_dataset = torchvision.datasets.MNIST('/_data/', train=True, download=True,
                                                   transform=torchvision.transforms.Compose([
                                                       torchvision.transforms.ToTensor(),
                                                       torchvision.transforms.Normalize(
                                                           (0.1307,), (0.3081,))]))

        add_data_unpacker(train_dataset, default_unpacker)
        add_class_names(train_dataset, class_names)

        train_loader = DataLoader(
            train_dataset, batch_size=train_batch_size, shuffle=True)

        test_dataset = torchvision.datasets.MNIST('/_data/', train=False, download=True,
                                                  transform=torchvision.transforms.Compose([
                                                      torchvision.transforms.ToTensor(),
                                                      torchvision.transforms.Normalize(
                                                          (0.1307,), (0.3081,))
                                                  ]))

        add_class_names(test_dataset, class_names=class_names)
        add_data_unpacker(test_dataset, default_unpacker)

        test_loader = DataLoader(
            test_dataset, batch_size=test_batch_size, shuffle=True)

        # Add required atributes to match dataset interface

        super().__init__(name=name, save_root=save_root,
                         save_file_name=save_file_name,
                         neural_net=neural_net, train_dataloader=train_loader,
                         test_dataloader=test_loader,
                         number_of_epochs=number_of_epochs, device=device)


def run_mnist_classification_exp(
        neural_net: Classifier,
        save_root,
        train_batch_size=100,
        test_batch_size=100,
        number_of_epochs=30,
        name='mnist-experiment', trials=1, device='cpu'
):
    '''
    function that runs the MNISTClassifierExperiment class 


    Parameters
    -------------
    neural_net (nn.Module): neural net that will be trained and test with MNIST data
    save_root (str): directory to save information (not implamented)
    train_batch (int): batch size for training data
    test_batch (int): batch size for testing data. This has no effect on results but may need to be changed
        based on pc specs
    number_of_epochs (int): number of training epochs
    name (str): the name of the experiment. Again for saving
    device (str): device to run the experiment ('cpu', 'cuda', 'cuda:0', 'cuda:1'...)
    trials (int): number of times to run the experiment

    Returns
    ---------
    None
    '''
    for trial_number in range(trials):
        print(f' Starting experiment on {device}')
        experiment = MNISTClassifierExperiment(neural_net=neural_net,
                                               save_root=save_root,
                                               train_batch_size=train_batch_size,
                                               test_batch_size=test_batch_size,
                                               number_of_epochs=number_of_epochs,
                                               name=name, trial_number=trial_number, device=device
                                               )
        experiment.run()
