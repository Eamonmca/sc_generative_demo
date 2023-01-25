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
    def __init__(self, encoder, decoder_r, decoder_p, classifier):
        """
        The VAEGAN model with Negative Binomial distribution as Latent Variable
        """
        super(VAEGAN_NEG_BI, self).__init__()
        self.encoder = encoder 
        self.decoder_r = decoder_r
        self.decoder_p = decoder_p
        
        self.classifier = classifier
        assert(self.encoder.latent_size == self.decoder.input_size)
        assert(self.encoder.latent_size == self.classifier.input_size)
        
    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5*logvar)
        eps = torch.randn_like(std)
        z = (mu + eps*std)
        return z

    def forward(self, x):
        mu, logvar = self.encoder(x)
        z = self.reparameterize(mu, logvar)
        h_r = self.decoder_r(z)
        h_p = self.decoder_p(z)
        y_hat = self.classifier(z)
        x_hat = NegativeBinomial(h_r, h_p).sample()
        return x_hat, y_hat, mu, logvar, h_r, h_p

