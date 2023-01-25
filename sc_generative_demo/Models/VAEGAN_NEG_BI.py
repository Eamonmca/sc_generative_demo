# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/11_Model_VAEGAN_NEG_BI.ipynb.

# %% auto 0
__all__ = ['VAEGAN_NEG_BI']

# %% ../../nbs/11_Model_VAEGAN_NEG_BI.ipynb 3
import torch 
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import NegativeBinomial

class VAEGAN_NEG_BI(nn.Module):
    def __init__(self, encoder, decoder, classifier):
        """
        The VAEGAN model with Negative Binomial distribution as Latent Variable
        """
        super(VAEGAN_NEG_BI, self).__init__()
        self.encoder = encoder 
        self.decoder = decoder
        self.classifier = classifier
        assert(self.encoder.latent_size == self.decoder.input_size)
        assert(self.encoder.latent_size == self.classifier.input_size)
        
    def reparameterize(self, mu, log_disp):
        disp = torch.exp(log_disp)
        z = NegativeBinomial(mu, disp).rsample()
        return z

    def forward(self, x):
        mu, log_disp = self.encoder(x)
        z = self.reparameterize(mu, log_disp)
        x_hat = self.decoder(z)
        y_hat = self.classifier(z)
        return x_hat, y_hat, mu, log_disp
    
