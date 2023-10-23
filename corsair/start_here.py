import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch import Tensor
import os
from experiments.mnist.classifier import run_mnist_classification_exp
from experiments.network_templates import Classifier


'''
Included in this file is a working example of how to run the an  experiment in the corsair framework.


All source code and a working example, for a given experiment can be found in the approperate experiment
directory. For this mnist_experiment:

Corsair
    |_ experiments
        |_ mnist_experiment
            |_ mnist_exp.py (source code for mnist_exp includes the run_mnist_classification_exp function)
            |_ working_example.py (example of how to run an mnist experiment)

Below is copied and pasted from Corsair/experiments/mnist_experiment/working_example.py
'''


class MModel(Classifier):

    '''
    An example of an MnistModel (MModel) 
    An MnistModel is a child of the Classifier class see 
    The Classifier class is a child of the NeuralNetwork class, and so all @abstractmethods of the 
    NeuralNetwork class must also be defined. 
    The NeuralNetwork and Classifier class are found in network_templates.py

    Corsair
        |_ experiments
            |_ network_templates.py

    '''

    def __init__(self):
        '''
        name: str must be defined and passed to Classifier  
        At the moment the name parameter is not used, but it will be used when save funtionality is implemented. 
        >>> name: str = 'my_network
        >>> super().__init__(name=name)

        the __init__() is also where you will intalize all nn.Modules needed for your network. 
        >>> self.my_first_conv_layer = torch.nn.conv2d(1,32,3,1)
        >>> self.my_second_conv_layer = torch.nn.conv2d(32,64,3,1) 

        common layers can be found https://pytorch.org/docs/stable/nn.html

        '''

        # the name of this model is mnist_classifier
        name = 'mnist_classifier'

        # super call to the Classifier parent class passing the name as an argument
        super().__init__(name=name)

        # define first conv layer 1 input channel 32 output channels kernel size 3 stride 1
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)  # define second conv layer

        # define a dropout layer: probablity 0.25
        self.dropout1 = nn.Dropout(0.25)

        self.dropout2 = nn.Dropout(0.5)  # define a second dropout layer
        # define a fully connected layer with 9216 input nodes and 128 output nodes
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def set_optimizers(self) -> None:
        '''
        Method for setting optimizers
        ClassiferExperiment class will call this method and intalize all optimizers 
        This is implemented so that the user does not forget about optimizers 
        All optimizers are stored in their own self variables and take the parameters they are to optimize as a first argument

        Single optimizer. All parameters are store in self
        >>> self.optimizer = torch.optim.Adam(self.parameters(), lr=0.001)

        optimizers for different blocks 
        >>> self.optimizer1 = torch.optim.SGD(self.block1.parameters(), lr=.001)
        >>> self.optimizer2 = torch.optim.Adam(self.block2.parameters(), lr=0.001)


        '''

        # set one optimizer to update all parameters
        self.optimizer = optim.Adam(self.parameters(), lr=0.001)

    def set_losses(self):
        '''
        method to set losses for your model
        ClassifierExperiment class will call this method and intalize all losses 
        All losses are stored in their own self variables 

        >>> self.loss1 = torch.nn.CrossEntropyLoss()
        >>> self.loss2 = torch.nn.MSELoss()

        common losses can be found at https://pytorch.org/docs/stable/nn.html
        '''

        self.loss: nn.Module = nn.CrossEntropyLoss()

    def forward(self, inputs: Tensor):
        '''
        Method that defines the behavior when your model is called. 
        All user defined nn.Modules Classes (like this model) must define this function

        Parameters 
        ------------
        inputs (torch.tensor): 
        '''
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
        '''
        Method that defines how your network should handle a batch of training inputs and training outputs.


        Parameters 
        ----------
        inputs (torch.Tensor): mnist images in Tensor format. Batched with each individual dimension given by 1X32X32
        label (torch.Tensor): labels for the corresponing mnist images. 
        ----------
        Returns loss (torch.Tensor)

        every train_pass function should start by zeroing out the gradients in your optimizer 
        and retruns the loss of your network. 
        The ClassiferExperiment class will use this loss for logging purposes. 
        >>> self.optimizer1.zero_grad()
        >>> guess = self.forward(input)
        >>> loss = self.loss(guess, label)
        >>> loss.backward()
        >>> self.optimizer.step()
        >>> return loss 
        '''

        self.optimizer.zero_grad()  # zero our your graident

        # pass the inputs to the forward call of your network to get the guess
        guess = self.forward(input)

        # compare the guess and label via loss function
        loss: Tensor = self.loss(guess, label)
        loss.backward()  # use the loss to backprop your graidents
        self.optimizer.step()  # tell the optimize to step each parameter
        return loss  # return the loss to ClassifierExperiment

    # optional function unchanged
    def _classify(self, inputs: Tensor) -> Tensor:
        '''
        Optional method. Optional methods have defaulted behavior, but may be overwritten.
        Method is called by the Evaluation to get the your models final prediction


        Parameters 
        -----------
        inputs (torch.Tensor): Mnist sample
        -----------
        Returns
        classification (torch.LongTensor): model's classification

        '''
        # define how your network classifies an input
        guess = self.forward(inputs)  # Get the network logits
        # argmax the logits to get a classification
        classification = torch.argmax(guess, dim=1)
        return classification  # return classification


'''
Once a network that follows the Classifier interface has been created
you can run the mnist_experiment. Create a file in the full scope of Corsiar and follow the example below 

'''
# what a main function looks like
if __name__ == '__main__':
    '''
    Create an instance of your model. 
    Models can be stored in the networks dir or anywhere you wish
    '''
    my_model = MModel()

'''
The function call below will run an mnist experiment 

def run_mnist_classification_exp(
    neural_net=my_model,
    save_root=os.getcwd(),  # Save function no implemented yet.
    train_batch_size=100,
    test_batch_size=100,
    number_of_epochs=2,
    name='mnist-experiment',
    device='cuda',
)
    Parameters
    -------------
    neural_net (nn.Module): neural net that will be trained and test with MNIST data
    save_root (str): directory to save information (not iimplemented)
    train_batch (int): batch size for training data
    test_batch (int): batch size for testing data. This has no effect on results but may need to be changed 
        based on pc specs
    number_of_epochs (int): number of training epochs
    name (str): the name of the experiment. Again for saving
    device (str): device to run the experiment ('cpu', 'cuda', 'cuda:0', 'cuda:1'...)
    trials (int): number of times to run the experiment (1 is enough for mnist)

    Returns
    ---------
    None 
    displays confusion matrix generated by your model 

'''

run_mnist_classification_exp(
    neural_net=my_model,
    save_root=os.getcwd(),  # Save function no implemented yet.
    train_batch_size=100,
    test_batch_size=100,
    number_of_epochs=2,
    name='mnist-experiment',
    device='cuda',
    trials=1
)
