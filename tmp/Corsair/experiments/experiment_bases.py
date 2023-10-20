from abc import ABC, abstractmethod
from torch import Tensor
from torch.utils.data import DataLoader
from experiments.evaulation import get_confusion_matrix
from experiments.mnist_experiment.network_template import Classifier



# Todo: Add valadation (if a valadation set is provided)


class _ExperimentBase(ABC):

    def __init__(self, name: str, save_root: str, save_file_name: str):
        self._name = name
        self._save_root = save_root
        self._save_file_name = save_file_name

    @property
    def name(self): return self._name
    @property
    def save_root(self): return self._save_root
    @property
    def save_file_name(self): return self._save_file_name

    @abstractmethod
    def run(self): pass
    @abstractmethod
    def _gather_results(self): pass


class ClassifierExperiment(_ExperimentBase):

    def __init__(self, name: str, save_root: str, save_file_name: str,
                 neural_net: Classifier, train_dataloader: DataLoader,
                 test_dataloader: DataLoader, number_of_epochs: int, device: str):

        super().__init__(name=name, save_root=save_root,
                         save_file_name=save_file_name
                         )
        self.device = device
        self.neural_net = neural_net
        self.train_dataloader = train_dataloader
        self.test_dataloader = test_dataloader
        self.neural_net.set_optimizers()
        self.neural_net.set_losses()
        self.neural_net.to(device)
        self.number_of_epochs = number_of_epochs
        # self.device = neural_net.device
        self.neural_net.to(self.device)

    def run(self):
        self._train()
        self._gather_results()

    def _train(self):
        for i in range(self.number_of_epochs):
            # This needs to be removed loss calculations need to be handeled by the network or a logger.
            running_loss: float = 0.0
            for j, data in enumerate(self.train_dataloader):
                inputs, outputs = self.train_dataloader.dataset.unpack_data(
                    data, self.device)
                loss: Tensor = self.neural_net.train_pass(
                    inputs, outputs)  # Todo need to supoort multiplie losses!
                running_loss += loss.item()

            print(
                f"the loss for epoch {i} is {running_loss/len(self.train_dataloader.dataset)}"
            )

    def _gather_results(self):
        get_confusion_matrix(self.neural_net,
                             self.test_dataloader,
                             self.device)
