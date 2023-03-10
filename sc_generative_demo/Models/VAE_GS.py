# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/15_Joint_VAE.ipynb.

# %% auto 0
__all__ = ['VAE_GS']

# %% ../../nbs/15_Joint_VAE.ipynb 3
import torch 
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import NegativeBinomial

class VAE_GS(nn.Module):
    def __init__(self, encoder, decoder_a, decoder_b, decoder_c):
        """
        The VAEGAN model with Negative Binomial distribution as Latent Variable
        """
        super(VAE_GS, self).__init__()
        self.encoder = encoder 
        self.decoder_r = decoder_a
        self.decoder_p = decoder_b
        self.decoder = decoder_c
        
    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5*logvar)
        eps = torch.randn_like(std)
        z = (mu + eps*std)
        return z
    
    def decode(self, z):
       h_a = self.decoder_a(z)
       h_b = self.decoder_b(z)
       h_c = self.decoder_c(z)
       h_a = F.relu(h_a)
       h_b = F.relu(h_b)
       h_c = F.softmax(h_c, dim = 1)
       x_hat = NegativeBinomial(h_a, logits = h_b).sample()
       y_hat = F.gumbel_softmax(h_c, tau = 0.1, hard = True)
       return x_hat, y_hat, h_a, h_b, h_c

    def forward(self, x):
        mu, logvar = self.encoder(x)
        z = self.reparameterize(mu, logvar)
        x_hat, y_hat, h_a, h_b, h_c = self.decode(z)
        
        return x_hat, y_hat, mu, logvar, h_a, h_b, h_c

