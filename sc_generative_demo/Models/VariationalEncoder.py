# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/05_Model_Variational_Encoder.ipynb.

# %% auto 0
__all__ = ['VariationalEncoder']

# %% ../../nbs/05_Model_Variational_Encoder.ipynb 3
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

class VariationalEncoder(nn.Module):
    """ Variational Encoder pytorch model
    """
    def __init__(self, input_size, hidden_sizes, latent_size, dropout, use_norm):
        super().__init__()
        self.input_size = input_size
        self.hidden_sizes = hidden_sizes
        self.latent_size = latent_size
        self.dropout = dropout
        self.use_batch_norm = use_norm

        # create a list of layers
        layers = []

        # input layer
        layers.append(nn.Linear(self.input_size, self.hidden_sizes[0]))
        layers.append(nn.LeakyReLU(0.2))
        if self.dropout > 0:
            layers.append(nn.Dropout(p=self.dropout))

        # hidden layers
        for i in range(1, len(self.hidden_sizes)):
            layers.append(nn.Linear(self.hidden_sizes[i-1], self.hidden_sizes[i]))
            if self.use_batch_norm:
                layers.append(nn.InstanceNorm1d(self.hidden_sizes[i]))
            layers.append(nn.LeakyReLU(0.2))
            if self.dropout > 0:
                layers.append(nn.Dropout(p=self.dropout))
      
        # create the model using Sequential
        self.model = nn.Sequential(*layers)
        self.model.mu_layer = nn.Linear(self.hidden_sizes[-1], self.latent_size)
        self.model.logvar_layer = nn.Linear(self.hidden_sizes[-1], self.latent_size)
        

    def forward(self, x):
        for layer in self.model[:-2]:
            x = layer(x)
        mu = self.model.mu_layer(x)
        logvar = self.model.logvar_layer(x)
        return mu, logvar

