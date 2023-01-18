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
        self.use_norm = use_norm

        # create a list of layers
        layers = []

        # input layer
        layers.append(nn.Linear(self.input_size, self.hidden_sizes[0]))
        layers.append(nn.ReLU(0.2))
        if self.dropout > 0:
            layers.append(nn.Dropout(p=self.dropout))

        # hidden layers
        for i in range(1, len(self.hidden_sizes)):
            layers.append(nn.Linear(self.hidden_sizes[i-1], self.hidden_sizes[i]))
            if self.use_norm:
                layers.append(nn.InstanceNorm1d(self.hidden_sizes[i]))
            layers.append(nn.ReLU(0.2))
            if self.dropout > 0:
                layers.append(nn.Dropout(p=self.dropout))
            
        # layers.append(nn.Linear(self.hidden_sizes[-1], self.latent_size))
      
        # create the model using Sequential
        self.model = nn.Sequential(*layers)
        self.mu_layer = nn.Linear(self.latent_size, self.latent_size)
        self.logvar_layer = nn.Linear(self.latent_size, self.latent_size)
       
        

    def forward(self, x):
        x = self.model(x)
        mu = self.mu_layer(x)
        logvar = self.logvar_layer(x)
        return mu, logvar
