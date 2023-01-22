# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/08_Model_VAEGAN.ipynb.

# %% auto 0
__all__ = ['VAEGAN']

# %% ../../nbs/08_Model_VAEGAN.ipynb 3
import torch 
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

class VAEGAN(nn.Module):
    def __init__(self, encoder, decoder, classifier):
        """
        The VAE-GAN model.
        """
        super(VAEGAN, self).__init__()
        self.encoder = encoder 
        self.decoder = decoder
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
        x_hat = self.decoder(z)
        y_hat = self.classifier(z)
        return x_hat, y_hat, mu, logvar
    