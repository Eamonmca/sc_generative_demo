# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/03_datasets.ipynb.

# %% auto 0
__all__ = ['Gex_DTS_Data_Label']

# %% ../nbs/03_datasets.ipynb 3
import torch
class Gex_DTS_Data_Label(torch.utils.data.Dataset):
    def __init__(self, 
                 data
                 ,labels):
        self.data = data
        self.labels = labels

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]
