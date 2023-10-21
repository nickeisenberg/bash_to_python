from dataclasses import dataclass
from torch.utils.data import DataLoader
from datasets.sample_dataset import BaseSampleDataset
from experiments.experiment_bases import ClassifierExperiment

from networks.network_base import Classifier

# Not implamented (nor should they be) missing_poses / missing_classes


@dataclass
class SampleExpDatasettings:
    '''
    Train style: real, synth, lr_synth(lr:= low rank), lr_reall respentation. 
    Test style: real, synth, lr_synth, lr_real
    missing_poses: float that represents the missing percentage of poses
    missing_classes: int that represents how many classes to remove (starting 
    from 9-ith class to i)
    '''
    train_style: str
    test_style: str = 'real'
    missing_poses: float = None
    missing_classes: int = None
    main_dir: str = r'C:\Users\SWANMB\Documents\_datasets\SAMPLE_dataset_public-master\png_images\qpm'


class SampleExp(ClassifierExperiment):

    def __init__(self, neural_net: Classifier, save_root: str,
                 dataset_settings: SampleExpDatasettings,
                 train_batch_size: int = 32,
                 test_batch_size: int = 100,
                 number_of_epochs: int = 50,
                 name: str = 'sample-experiment', trial_number=1,
                 ):
        # a little helper function. Might evolve into its own file
        def dataset_parser(dataset_settings: SampleExpDatasettings):
            train_style = dataset_settings.train_style
            test_style = dataset_settings.test_style
            main_dir = dataset_settings.main_dir
            train_dataset = BaseSampleDataset(style=train_style,
                                              main_dir=main_dir)
            test_dataset = BaseSampleDataset(style=test_style,
                                             main_dir=main_dir)
            return train_dataset, test_dataset

        save_file_name = self.neural_net.name + name
        train_data, test_data = dataset_parser(dataset_settings)
        train_dataloader = DataLoader(train_data, batch_size=train_batch_size,
                                      shuffle=True)
        test_dataloader = DataLoader(test_data,
                                     batch_size=test_batch_size, shuffle=False)

        super().__init__(name=name, save_root=save_root,
                         save_file_name=save_file_name, neural_net=neural_net,
                         train_dataloader=train_dataloader,
                         test_dataloader=test_dataloader, number_of_epochs=number_of_epochs)


def run_sample_exp(neural_net: Classifier, save_root: str,
                   dataset_settings: SampleExpDatasettings,
                   train_batch_size: int = 32,
                   test_batch_size: int = 100,
                   number_of_epochs: int = 50,
                   name: str = 'sample-experiment', trials: int = 1,):
    for trial in range(trials):
        experiment = SampleExp(nueral_net=neural_net,
                               save_root=save_root,
                               dataset_settings=dataset_settings,
                               train_batch_size=train_batch_size,
                               test_batch_size=test_batch_size,
                               number_of_epochs=number_of_epochs,
                               name=name
                               )
        experiment.run()
