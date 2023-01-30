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
    def __init__(self, encoder_z, encoder_l, decoder_x, decoder_r, decoder_p, classifier, log = True):
        """
        The VAEGAN model with Negative Binomial distribution as Latent Variable
        """
        super(VAEGAN_NEG_BI, self).__init__()
        self.encoder_z = encoder_z
        self.encoder_l = encoder_l
        self.decoder_x = decoder_x
        self.decoder_r = decoder_r
        self.decoder_p = decoder_p
        
        self.classifier = classifier
    
        
    def reparameterize(self, mu, logvar):
        var = torch.exp(logvar) + 1e-8
        z = Normal(mu, var.sqrt()).rsample()
        return z
    
    def decode(self, z, l):
        h_x = self.decoder_x(z) 
        h_x = F.relu(h_x)
        h_r = self.decoder_r(h_x)      
        h_r = F.softmax(h_r)
        
        h_p = torch.exp(torch.clamp(l, max=12)) * h_r
        x_hat = NegativeBinomial(mu = h_r, theta= h_p).sample()
        return x_hat, h_r, h_p


    def forward(self, x, log=False):
        if log :
            x= torch.log(x+1)
        mu_l, logvar_l = self.encoder_l(x)
        mu_z, logvar_z = self.encoder_z(x)
        
        l = self.reparameterize(mu_l, logvar_l)
        z = self.reparameterize(mu_z, logvar_z)
        
        x_hat, h_r, h_p = self.decode(z,l)
        
        y_hat = self.classifier(z) 
        
        return x_hat, y_hat, mu_z, logvar_z, h_r, h_p, l


