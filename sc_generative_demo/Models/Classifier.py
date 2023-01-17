# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/04_Model_Classifier.ipynb.

# %% auto 0
__all__ = ['Classifier']

# %% ../../nbs/04_Model_Classifier.ipynb 3
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

class Classifier(nn.Module):
    def __init__(self, input_size, hidden_sizes, output_size, dropout, use_batch_norm, spectral_norm=False):
        super().__init__()

        self.input_size = input_size
        self.dropout = dropout
        self.hidden_sizes = hidden_sizes
        self.output_size = output_size
        self.use_batch_norm = use_batch_norm
        self.spectral_norm = spectral_norm
            
        if spectral_norm:
            self.spectral_norm = nn.utils.spectral_norm

        # create a list of layers
        layers = []

        # input layer
        if spectral_norm:
            layers.append(self.spectral_norm(nn.Linear(self.input_size, self.hidden_sizes[0])))
        else:
            layers.append(nn.Linear(self.input_size, self.hidden_sizes[0]))
        layers.append(nn.LeakyReLU(0.2))
        if self.dropout > 0:
            layers.append(nn.Dropout(p=self.dropout))

        # hidden layers
        for i in range(1, len(self.hidden_sizes)):
            if spectral_norm:
                layers.append(self.spectral_norm(nn.Linear(self.hidden_sizes[i-1], self.hidden_sizes[i])))
            else:
                layers.append(nn.Linear(self.hidden_sizes[i-1], self.hidden_sizes[i]))
            if self.use_batch_norm:
                layers.append(nn.InstanceNorm1d(self.hidden_sizes[i]))
            layers.append(nn.LeakyReLU(0.2))
            if self.dropout > 0:
                layers.append(nn.Dropout(p=self.dropout))

        # output layer
        layers.append(nn.Linear(self.hidden_sizes[-1], self.output_size))
        # create the model using Sequential
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        x = self.model(x)
        return F.softmax(x,dim=1)
      

