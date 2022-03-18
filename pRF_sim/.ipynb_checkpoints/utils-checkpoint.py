import pkg_resources
import yaml,os
import re
import nibabel as nib
import neuropythy as npy
import numpy as np

from scipy import stats
from sklearn.model_selection import KFold
import random
import pandas as pd

DATA_PATH = pkg_resources.resource_filename('pRF_sim', 'test/data')

MMP_PATH = pkg_resources.resource_filename('pRF_sim', 'test/data/HCP-MMP')


pkg_yaml=os.path.join(DATA_PATH,'config.yml')


def load_pkg_yaml():
    """
    Loads the package yaml into memory.
    
    """
    with open(pkg_yaml, 'r') as f:
        y = yaml.safe_load(f)
    return y

def load_retprior():
    """
    Loads the retinotopy prior into memory.
    
    """
    retprior=pd.read_csv(os.path.join(DATA_PATH,'retprior.csv'))
    return retprior

class MMP_masker:
    """
    Creates masks for regions defined in the multimodal parcellation defined by Glasser. 
    
    (http://corticalexplorer.com/)
    
    """
    
    def __init__(self,MMPloc=MMP_PATH):
        self.MMPloc=MMPloc
        self.load()

    def load(self):
        self.annotfile_L = os.path.join(self.MMPloc,'lh.HCP-MMP1.annot')
        self.annotfile_R = os.path.join(self.MMPloc,'rh.HCP-MMP1.annot')

        self.lh_labels, self.lh_ctab, self.lh_names = nib.freesurfer.io.read_annot(self.annotfile_L)
        self.rh_labels, self.rh_ctab, self.rh_names = nib.freesurfer.io.read_annot(self.annotfile_R)
        self.lh_names=self.decode_list(self.lh_names)
        self.rh_names=self.decode_list(self.rh_names)

    def decode_list(self,inlist):
        outlist=[x.decode() for x in inlist]
        return outlist

    def get_roi_index(self,label,hem='L'):
        idx=self.lh_names.index('{hem}_{label}_ROI'.format(label=label,hem=hem))

        return idx

    def get_roi_verts(self,label):
        Lverts,Rverts=np.where(self.lh_labels==self.get_roi_index(label))[0],np.where(self.rh_labels==self.get_roi_index(label))[0]
        return Lverts, Rverts

    def downsample(self,inarray,vertsperhem=10242):

        outarray=inarray[:vertsperhem]
        return outarray

    def make_roi_mask(self,label,downsample=False,boolean=True):
        L_empty,R_empty=np.zeros(len(self.lh_labels)),np.zeros(len(self.rh_labels))
        Lverts,Rverts=self.get_roi_verts(label)
        L_empty[Lverts]=1
        R_empty[Rverts]=1
        if downsample==True:
            L_empty,R_empty=self.downsample(L_empty),self.downsample(R_empty)

        combined_mask=np.concatenate([L_empty,R_empty])

        if boolean==True:
             L_empty,R_empty,combined_mask=L_empty.astype(bool),R_empty.astype(bool),combined_mask.astype(bool)

        return L_empty, R_empty, combined_mask


    def make_composite_mask(self,labels):
        roimasks=np.sum([self.make_roi_mask(label) for label in labels],axis=0)
        return roimasks
