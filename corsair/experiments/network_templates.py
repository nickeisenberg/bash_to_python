from abc import ABC, abstractmethod
import torch
from torch import Tensor
from abc import ABC
from torch import nn, Tensor
from experiments.util import optional


class NeuralNetwork(nn.Module, ABC):
    def __init__(self, name: str = 'classifier'):
        self._name = name
        super().__init__()

    @abstractmethod
    def train_pass(input, output) -> Tensor:
        '''
        holds the logic for a batch wise traiing 
        '''
        pass

    @abstractmethod
    def forward(inputs: Tensor) -> Tensor: pass

    @abstractmethod
    def set_optimizers(self) -> None:
        '''
        store optimizers in self variables 
        '''
        pass

    @abstractmethod
    def set_losses(self) -> None:
        '''
        store losses in self variables
        '''
        pass

    @property
    def name(self): return self._name


class Classifier(NeuralNetwork):

    @optional
    def _classify(self, inputs: Tensor) -> Tensor:
        guess = self.forward(inputs)
        classification = torch.argmax(guess, dim=1)
        return classification

