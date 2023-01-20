# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_data_management.ipynb.

# %% auto 0
__all__ = ['SplitData', 'Meta']

# %% ../nbs/02_data_management.ipynb 3
import random
import math
from fastcore.utils import *
from sklearn.model_selection import train_test_split
import pandas as pd

class SplitData:
    """A class for splitting a Scanpy AnnData object into training, evaluation, and test sets."""
    def __init__(self, 
                 scdata, # a Scanpy AnnData object
                 train_fraction = 0.8,  # the fraction of the data to use for training
                 eval_fraction = 0.2, # the fraction of the data to use for evaluation
                 test = False, # whether to include a test set in the split
                 random_seed = 1234 # the random seed to use for the split
                 ):
        self.scdata = scdata
        self.train_fraction = train_fraction
        self.eval_fraction = eval_fraction
        self.test = test
        self.random_seed = random_seed
        self._check_input()


    def _check_input(self):
        """Check the input parameters for errors."""
        if self.train_fraction + self.eval_fraction > 1:
            raise ValueError("train_fraction + eval_fraction should be less than 1")
        if self.train_fraction <= 0:
            raise ValueError("train_fraction should be greater than 0")

    def split_data(self):
        """ Split the data into training, evaluation, and (optionally) test sets."""
        # Initialize the random number generator with the specified seed
        if self.random_seed:
            random.seed(self.random_seed)
            
        # Calculate the number of training samples based on the train_fraction
        train_size = int(len(self.scdata.obs.index) * self.train_fraction)
        # Calculate the number of evaluation samples based on the eval_fraction
        eval_size = int(len(self.scdata.obs.index) - train_size)
        # If the test flag is set to True
        if self.test:
            # Calculate the number of test samples by subtracting the number of training and evaluation samples from the total number of samples
            eval_size = int(eval_size * self.eval_fraction)
            test_size = len(self.scdata.obs.index) - train_size - eval_size
            # Generate a list of random indices with the same length as the number of samples
            indices = random.sample(range(len(self.scdata.obs.index)), train_size + eval_size + test_size)
            # Split the indices into training, evaluation, and test sets
            train_indices = indices[:train_size]
            eval_indices = indices[train_size:train_size + eval_size]
            test_indices = indices[train_size + eval_size:]
            # Return the indices for the training, evaluation, and test sets
            return [self.scdata.obs.index[i] for i in train_indices], [self.scdata.obs.index[i] for i in eval_indices], [self.scdata.obs.index[i] for i in test_indices]
        # If the test flag is set to False
        else:
            # Generate a list of random indices with the same length as the number of training and evaluation samples
            indices = random.sample(range(len(self.scdata.obs.index)), train_size + eval_size)
            # Split the indices into training and evaluation sets
            train_indices = indices[:train_size]
            eval_indices = indices[train_size:]
            # Return the indices for the training and evaluation sets
            return [self.scdata.obs.index[i] for i in train_indices], [self.scdata.obs.index[i] for i in eval_indices]
        
    def _split_data(self, scdata, train_fraction, eval_fraction, test=False, random_seed=None):
        """ Split the data into training, evaluation, and (optionally) test sets."""
        # Initialize the random number generator with the specified seed
        if random_seed:
            random.seed(random_seed)
            
        # Calculate the number of training samples based on the train_fraction
        train_size = int(len(scdata.obs.index) * train_fraction)
        # Calculate the number of evaluation samples based on the eval_fraction
        eval_size = int(len(scdata.obs.index) - train_size)
        # If the test flag is set to True
        if test:
            # Calculate the number of test samples by subtracting the number of training and evaluation samples from the total number of samples
            eval_size = int(eval_size * eval_fraction)
            test_size = len(scdata.obs.index) - train_size - eval_size
            # Generate a list of random indices with the same length as the number of samples
            indices = random.sample(range(len(scdata.obs.index)), train_size + eval_size + test_size)
            # Split the indices into training, evaluation, and test sets
            train_indices = indices[:train_size]
            eval_indices = indices[train_size:train_size + eval_size]
            test_indices = indices[train_size + eval_size:]
            # Return the indices for the training, evaluation, and test sets
            return [scdata.obs.index[i] for i in train_indices], [scdata.obs.index[i] for i in eval_indices], [scdata.obs.index[i] for i in test_indices]
        # If the test flag is set to False
        else:
            # Generate a list of random indices with the same length as the number of training and evaluation samples
            indices = random.sample(range(len(scdata.obs.index)), train_size + eval_size)
            # Split the indices into training and evaluation sets
            train_indices = indices[:train_size]
            eval_indices = indices[train_size:]
            # Return the indices for the training and evaluation sets
            return [scdata.obs.index[i] for i in train_indices], [scdata.obs.index[i] for i in eval_indices]

        
    def split_data_stratified(self, stratify_by):
        """ Split the data into training, evaluation, and (optionally) test sets stratified by the specified factor"""
        
        # Get the unique classes from the stratify_by column
        classes = self.scdata.obs[stratify_by].unique()
        
        # Lists to store the indices of the split data
        train_idxs = []
        evaluation_idxs = []
        
        # If test set is requested, create an empty list to store its indices
        if self.test:
            test_idxs = []
        
        # For each class in the data
        for batch in classes:
            # Split the data for this class into training, evaluation, and (if requested) test sets
            if self.test:
                train_idx, eval_idx, test_idx = self._split_data(self.scdata[self.scdata.obs[stratify_by] == batch], train_fraction=self.train_fraction, eval_fraction=self.eval_fraction, test=self.test, random_seed=self.random_seed)
                # Add the indices for this class to the overall list of indices
                train_idxs.extend(train_idx)
                evaluation_idxs.extend(eval_idx)
                test_idxs.extend(test_idx)
            else:
                # Split the data for this class into training and evaluation sets
                train_idx, eval_idx = self._split_data(self.scdata[self.scdata.obs[stratify_by] == batch], train_fraction=self.train_fraction, eval_fraction=self.eval_fraction, test=self.test, random_seed=self.random_seed)
                # Add the indices for this class to the overall list of indices
                train_idxs.extend(train_idx)
                evaluation_idxs.extend(eval_idx)
        
        # If a test set was requested, check that the sets are disjoint and their union is the full set of indices
        if self.test:
            assert set(train_idxs).intersection(set(evaluation_idxs)) == set()
            assert set(train_idxs).intersection(set(test_idxs)) == set()
            assert set(evaluation_idxs).intersection(set(test_idxs)) == set()
            assert len(train_idxs) + len(evaluation_idxs) + len(test_idxs) == len(self.scdata.obs.index)
            
            
            # Return the indices for the training, evaluation, and test sets
            return list(train_idxs), list(evaluation_idxs), list(test_idxs)
        else:
            # Check that the training and evaluation sets are disjoint and their union is the full set of indices
            assert set(train_idxs).intersection(set(evaluation_idxs)) == set()
            assert len(train_idxs) + len(evaluation_idxs) == len(self.scdata.obs.index)
            
            # Return the indices for the training and evaluation sets
            return list(train_idxs), list(evaluation_idxs)

    
    def pct_summary(self, idxs_list, stratify_by):
        """ Return a dataframe summarizing the percentage of samples in each class for each subset of the data"""
        
        # If there are two subsets of the data
        if len(idxs_list) == 2:
            # Concatenate the value counts of the stratify_by column for each subset, normalizing so that they sum to 1
            df = pd.concat([self.scdata[idxs_list[0]].obs[stratify_by].value_counts(normalize=True), self.scdata[idxs_list[1]].obs[stratify_by].value_counts(normalize=True)], axis=1)
            # Rename the columns of the dataframe
            df.columns = ["train", "eval"]
            # Return the dataframe
            return df
        # If there are three subsets of the data
        elif len(idxs_list) == 3:
            # Concatenate the value counts of the stratify_by column for each subset, normalizing so that they sum to 1
            df = pd.concat([self.scdata[idxs_list[0]].obs[stratify_by].value_counts(normalize=True), self.scdata[idxs_list[1]].obs[stratify_by].value_counts(normalize=True), self.scdata[idxs_list[2]].obs[stratify_by].value_counts(normalize=True)], axis=1)
            # Rename the columns of the dataframe
            df.columns = ["train", "eval", "test"]
            # Return the dataframe
            return df
        



# %% ../nbs/02_data_management.ipynb 4
class Meta:
    ...

# %% ../nbs/02_data_management.ipynb 5
@patch_to(Meta)
def strip(scdata, filters, copy = False, verbose = False):
    possible_dims = ["obs", "var", "obsm", "varm", "uns", "obsp", "varp"]
    keep = set ([dim for dim, _ in filters]).intersection(set(possible_dims))
    striped_items_dict = {}
    
    if copy:
        for dim in possible_dims:
                for key in list(scdata.__getattribute__(dim).keys()):
                    if key not in [k for d, ks in filters for k in ks]:
                        inner_dict = scdata.__getattribute__(dim).pop(key)
                        if dim not in striped_items_dict:
                            striped_items_dict[str(dim)] = {}
                            striped_items_dict[dim][key] = inner_dict
                    if verbose:
                        print(f"Removing {key} from {dim}")
        return scdata, striped_items_dict
    else:
        for dim in possible_dims:
                for key in list(scdata.__getattribute__(dim).keys()):
                    if key not in [k for d, ks in filters for k in ks]:
                        scdata.__getattribute__(dim).pop(key)
                        if verbose:
                            print(f"Removing {key} from {dim}")
        return scdata

                


# %% ../nbs/02_data_management.ipynb 6
@patch_to(Meta)
def sew(scdata, stripped_items, verbose = False):
    for dim in stripped_items:
        for key in stripped_items[dim]:
            scdata.__getattribute__(dim)[key] = stripped_items[dim][key]
            if verbose:
                print(f"Adding {key} to {dim}")


