# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/07_Evaluation.ipynb.

# %% auto 0
__all__ = ['Visualize', 'Inferance']

# %% ../nbs/07_Evaluation.ipynb 3
import torch
import scanpy as sc
import numpy as np
from fastcore.utils import *
import wandb
import scib



class Visualize:
    "Evaluation of the model"
    pass
    

# %% ../nbs/07_Evaluation.ipynb 4
@patch_to(Visualize)
def plot_embeddings(scdata, color_key_list, basis_list, device, show=False, log=True):
    for basis in basis_list:
        for color_key in color_key_list:
            plot_embeddings = sc.pl.embedding(scdata, basis=basis, color=color_key, wspace=0.3,  show=show)
            if log:
                wandb.log({"plot_embeddings_{}_{}".format(basis, color_key): wandb.Image(plot_embeddings)})

# %% ../nbs/07_Evaluation.ipynb 5
@patch_to(Visualize)
def plot_umaps(scdata, color_key_list, rep_list, device, show=False, log=True):
    for rep in rep_list:
        umap = sc.pp.neighbors(scdata, use_rep=rep)
        sc.tl.umap(scdata)
        for color_key in color_key_list:
            umap = sc.pl.umap(scdata, color=color_key, wspace=0.3, show = show)
            if log:
                wandb.log({"UMAP_{}_{}".format(rep, color_key): wandb.Image(umap)})

# %% ../nbs/07_Evaluation.ipynb 6
class Inferance:
   "Inferance of the model"
   pass

# %% ../nbs/07_Evaluation.ipynb 7
@patch_to(Inferance)
def get_embeddings_VAEGAN(VAEGAN, dataloader, device):
    with torch.no_grad():
        embeddings = []
        labels = []
        for batch, label in dataloader:
            batch = batch.to(device)
            x_hat, y_hat, mu, logvar, h_r, h_p = VAEGAN(batch)
            embeddings.append(mu.cpu().numpy())
            labels.append(label.cpu().numpy())
        embeddings = np.concatenate(embeddings)
        labels = np.concatenate(labels)
        return embeddings

# %% ../nbs/07_Evaluation.ipynb 8
@patch_to(Inferance)
def decode_embeddings_VAEGAN(VAEGAN, embeddings, device):
    with torch.no_grad():
        embeddings = torch.from_numpy(embeddings).to(device)
        x_hat = VAEGAN.decode(embeddings)
        return x_hat.cpu().numpy()
