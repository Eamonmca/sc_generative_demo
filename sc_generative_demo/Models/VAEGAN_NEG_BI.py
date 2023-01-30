# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/11_Model_VAEGAN_NEG_BI.ipynb.

# %% auto 0
__all__ = ['VAEGAN_NEG_BI']

# %% ../../nbs/11_Model_VAEGAN_NEG_BI.ipynb 3
import torch 
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import scvi
from scvi.models.distributions import NegativeBinomial
from torch.distributions import Normal

class VAEGAN_NEG_BI(nn.Module):
    def __init__(self, encoder, decoder_r, decoder_p, classifier, log = True):
        """
        The VAEGAN model with Negative Binomial distribution as Latent Variable
        """
        super(VAEGAN_NEG_BI, self).__init__()
        self.encoder = encoder 
        self.decoder_r = decoder_r
        self.decoder_p = decoder_p
        
        self.classifier = classifier
    
        
    def reparameterize(self, mu, logvar):
        var = logvar.exp() + 1e-8
        z = Normal(mu, var.sqrt()).rsample()
        return z
    
    def decode(self, z):
        h_r = self.decoder_r(z) 
        h_p = self.decoder_p(z)
        h_r = F.softmax(h_r)
        h_p = F.relu(h_p)
        x_hat = NegativeBinomial(h_r, h_p).sample()
        return x_hat, h_r, h_p


    def forward(self, x, log=False):
        if log :
            x= torch.log(x+1)
        mu, logvar = self.encoder(x)
        z = self.reparameterize(mu, logvar)
        x_hat, h_r, h_p = self.decode(z)
        y_hat = self.classifier(z) 
        return x_hat, y_hat, mu, logvar, h_r, h_p


