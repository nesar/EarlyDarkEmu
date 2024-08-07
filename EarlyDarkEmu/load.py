# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_load.ipynb.

# %% auto 0
__all__ = ['DATA_DIR', 'LIBRARY_PARAM_FILE', 'LIBRARY_PK_FILE', 'LIBRARY_K_FILE', 'LIBRARY_Z_FILE', 'OBS_DIR', 'SDSS_FILE',
           'WMAP_FILE', 'PARAM_NAME', 'load_npy_pk_k_z', 'load_sdss', 'load_wmap', 'load_params', 'sepia_data_format']

# %% ../nbs/00_load.ipynb 3
import numpy as np
import pkg_resources
from sepia.SepiaData import SepiaData
import matplotlib.pylab as plt


# %% ../nbs/00_load.ipynb 6
DATA_DIR = "data/pkg_data/"
LIBRARY_PARAM_FILE = pkg_resources.resource_stream("EarlyDarkEmu", DATA_DIR + "params_latin.txt").name
LIBRARY_PK_FILE = pkg_resources.resource_stream("EarlyDarkEmu", DATA_DIR + "pk_all.npy").name
LIBRARY_K_FILE = pkg_resources.resource_stream("EarlyDarkEmu", DATA_DIR + "k_all.npy").name
LIBRARY_Z_FILE = pkg_resources.resource_stream("EarlyDarkEmu", DATA_DIR + "z_all.npy").name


OBS_DIR = "data/obs_data/"
SDSS_FILE = pkg_resources.resource_stream("EarlyDarkEmu", OBS_DIR + "reid_DR7.txt").name
WMAP_FILE = pkg_resources.resource_stream("EarlyDarkEmu", OBS_DIR + "wmap_act.txt").name


PARAM_NAME = [r"$\omega_m$", r"h", r"$\sigma_8$", r"$\log(z_c)$", r"$f_{ede}$", r"$\theta_i$"]

# LIBRARY_ZK_FILE_VAL = pkg_resources.resource_stream("EarlyDarkEmu", DATA_DIR + "z_k_validation.txt").name
# LIBRARY_BK_FILE_VAL = pkg_resources.resource_stream("EarlyDarkEmu", DATA_DIR + "Boost_validation.npy").name
# LIBRARY_PARAM_FILE_VAL = pkg_resources.resource_stream("EarlyDarkEmu", DATA_DIR + "cosmo_validation.txt").name


# %% ../nbs/00_load.ipynb 11
_k_base = np.logspace(-5,  0, 210)
print(_k_base.shape)

# %% ../nbs/00_load.ipynb 13
def load_npy_pk_k_z(Pk_fileIn:str=LIBRARY_PK_FILE, # Input file for Pk
                     k_fileIn:str=LIBRARY_K_FILE,  # Input file for k
                     z_fileIn:str=LIBRARY_Z_FILE, # Input file for z
                     pk_log_scale:bool=True, #log10 scaling for P(k)
                     ) -> tuple:#Three n-D arrays for P(k), k and z


    # Pk_all = np.load(Pk_fileIn, allow_pickle=True, encoding='latin1')
    Pk_all = np.load(Pk_fileIn)
    k_all = np.load(k_fileIn)
    z_all = np.load(z_fileIn)

    # Pk_all = np.reshape(Pk_all, newshape=(-1, z_all.shape[0], k_all.shape[0]))
    
    if pk_log_scale: 
        Pk_all = np.log10(Pk_all)        

    return Pk_all, k_all, z_all


# %% ../nbs/00_load.ipynb 14
if True: 
    Pk_all, k_all, z_all = load_npy_pk_k_z(LIBRARY_PK_FILE, LIBRARY_K_FILE, LIBRARY_Z_FILE)

# %% ../nbs/00_load.ipynb 16
def load_sdss(fileIn:str=SDSS_FILE, #Input file
              ):
    k, pk, pk_error = np.loadtxt(fileIn, delimiter=' ').T
    return k, np.log10(pk), np.abs(pk_error/pk)

# %% ../nbs/00_load.ipynb 17
def load_wmap(fileIn:str=WMAP_FILE, #Input file
              ):
    k, pk, pk_error = np.loadtxt(fileIn).T
    return k, np.log10(pk), ((pk_error-pk)/pk)

# %% ../nbs/00_load.ipynb 21
def load_params(p_fileIn:str=LIBRARY_PARAM_FILE, # Input file for parameters
               ) -> np.array: # Parameters
    p_all = np.loadtxt(p_fileIn)

    return p_all[:, 1:-1]

# %% ../nbs/00_load.ipynb 23
def sepia_data_format(design:np.array=None, # Params array of shape (num_simulation, num_params)
                     y_vals:np.array=None, # Shape (num_simulation, num_y_values)
                     y_ind:np.array=None # Shape (num_y_values,)
                     ) -> SepiaData: #Sepia data format
    sepia_data = SepiaData(t_sim=design, y_sim=y_vals, y_ind_sim=y_ind)
    return sepia_data
