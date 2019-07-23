from torch.utils.data import Subset
from ..utils.module_loading import load_class
from ..utils.serialize import load_yaml, save_yaml
from .splitters import Split


class DataProvider:
    def __init__(self, config, data_path, splits_path):
        self.config = config
        self.dataset = load_class(config.dataset)
        self.splits = load_yaml(splits_path)

    def get_loader(self, name, outer_fold=0, inner_fold=0):
        indices = self.splits[name][outer_fold][inner_fold]
        partition = Subset(self.dataset, indices)
        loader = load_class(self.config.loader, partition)
        return loader

    @property
    def dim_features(self):
        assert hasattr(self.dataset, 'dim_features')
        return self.dataset.dim_features

    @property
    def dim_target(self):
        assert hasattr(self.dataset, 'dim_target')
        return self.dataset.dim_target

    @property
    def num_outer_folds(self):
        return len(self.splits[Split.TEST])

    @property
    def num_inner_folds(self):
        return len(self.splits[Split.TRAINING][0])

    def __iter__(self):
        for outer_fold in range(self.outer_folds):
            for inner_fold in range(self.inner_folds):

                training_fold = self.get_loader(Split.TRAINING, outer_fold, inner_fold)
                yield Split.TRAINING, training_fold

                validation_fold = self.get_loader(Split.VALIDATION, outer_fold, inner_fold)
                yield Split.VALIDATION, validation_fold

            test_fold = self.get_loader(Split.TEST, outer_fold, inner_fold)
            yield Split.TEST, test_fold