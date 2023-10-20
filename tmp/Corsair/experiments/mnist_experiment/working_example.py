import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from torch import Tensor
import os

from experiments.mnist_experiment.mnist_exp import run_mnist_classification_exp
from experiments.network_templates import Classifier



class MModel(Classifier):
    def __init__(self):
        name = 'mnist_classifier'

        # define all layers for your model
        # must call super().__init__(name=name) before any layers can be added
        # common layers https://pytorch.org/docs/stable/nn.html
        super().__init__(name=name)
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def set_optimizers(self) -> None:
        # define the optimizers for your networks
        # common optimizers https://pytorch.org/docs/stable/optim.html
        self.optimizer = optim.Adam(self.parameters(), lr=0.001)

    def set_losses(self):
        # set the losses your network will need for training
        # common losses https://pytorch.org/docs/stable/nn.html
        self.loss: nn.Module = nn.CrossEntropyLoss()

    def forward(self, inputs: Tensor):
        # define the behavior when your network receives an input
        x = self.conv1(inputs)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        return x

    def train_pass(self, input: torch.Tensor, label: torch.Tensor):
        # define what your network does on a trainining instance
        self.optimizer.zero_grad()
        guess = self.forward(input)
        loss: Tensor = self.loss(guess, label)
        loss.backward()
        self.optimizer.step()
        return loss

    # optional function unchanged
    def _classify(self, inputs: Tensor) -> Tensor:
        # define how your network classifies an input
        guess = self.forward(inputs)
        classification = torch.argmax(guess, dim=1)
        return classification


# what a main function looks like
if __name__ == '__main__':
    my_model = MModel()

# below are the the hyperparameters you can change for your experimental run

run_mnist_classification_exp(
    neural_net=my_model,
    save_root=os.getcwd(),  # Save function no implemented yet.
    train_batch_size=100,
    test_batch_size=100,
    number_of_epochs=2,
    name='mnist-experiment',
    device='cuda'
)
