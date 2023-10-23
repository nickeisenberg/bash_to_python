from typing import Callable, List
from sklearn.metrics import confusion_matrix
import numpy
import matplotlib.pyplot as plt
import itertools
from types import NoneType

from experiments.network_templates import Classifier



#TODO: find a good place for classifier putting it in .mnist_experiment.network_template seems wrong


def make_confusion_matrix(actual, guess):
    cm = confusion_matrix(actual, guess)
    cm = cm.astype('float') / cm.sum(axis=1)[:, numpy.newaxis]
    return cm


def get_acutal_guess_list(neural_net: Classifier,
                          test_dataloader,
                          device: str
                          ):
    actual = []
    guess = []
    for i, data in enumerate(test_dataloader):
        inputs, outputs = test_dataloader.dataset.unpack_data(data, device)
        temp_guess = neural_net._classify(inputs)
        guess.extend(temp_guess.to('cpu').tolist())
        actual.extend(outputs.tolist())
    return actual, guess


def plot_confusion_matrix(
        confusion_matrix: numpy.ndarray, 
        accuracy,
        cmap=plt.get_cmap('Blues'),
        class_names: List[str] | NoneType = None,
        ):

    rows = confusion_matrix.shape[0]
    columns = confusion_matrix.shape[1]
    class_names = list(range(num_classes)) if not class_names else class_names
    num_classes = len(class_names)
    plt.figure(figsize=(num_classes, num_classes))
    plt.imshow(confusion_matrix, interpolation='nearest', cmap=cmap)
    tick_marks = numpy.arange(num_classes)
    plt.xticks(tick_marks, class_names, rotation=45)
    plt.yticks(tick_marks, class_names)
    plt.grid(visible=False)

    thresh = confusion_matrix.max() / 2.0
    for row, column in itertools.product(range(rows), range(columns)):
        value = confusion_matrix[column, row]
        plt.text(
            row, column, "{:.2f}%".format(value * 100),
            horizontalalignment='center',
            color='white' if value > thresh else 'black', fontsize=11
        )
    plt.colorbar(fraction=0.046, pad=0.04)
    plt.title('Classification Accuracy {:.2f}%'.format(accuracy * 100))
    plt.ylabel("True Label")
    plt.xlabel("Predicted Label")
    plt.tight_layout()
    plt.show()


def calculate_accuracy(actual: List[int], guess: List[int]):
    return (numpy.array(actual) == numpy.array(guess)).sum()/len(actual)


def get_confusion_matrix(neural_net: Classifier, test_dataloader, device):
    actual, guess = get_acutal_guess_list(neural_net, test_dataloader, device)
    accuracy = calculate_accuracy(actual, guess)
    cm = make_confusion_matrix(actual, guess)
    class_names = test_dataloader.dataset._class_names
    plot_confusion_matrix(cm, accuracy, class_names=class_names)



