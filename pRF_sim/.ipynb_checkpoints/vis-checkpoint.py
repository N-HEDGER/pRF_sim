
import cortex
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import nibabel as nib
import pkg_resources
import yaml



def basic_plot(dat,vmax,subject='fsaverage',vmin=0,rois=False,colorbar=False,cmap='plasma',ax=None,labels=True):
    
    dat=np.array(dat)
    
    light=cortex.Vertex(dat,subject=subject, vmin=vmin, vmax=vmax,cmap=cmap)
    mfig=cortex.quickshow(light,with_curvature=True,with_rois=rois,with_colorbar=colorbar,with_labels=labels,fig=ax)
    return mfig

def alpha_plot(dat,dat2,vmin,vmax,vmin2,vmax2,subject='fsaverage',rois=False,labels=False,colorbar=False,cmap='nipy_spectral_alpha',ax=None):
    light=cortex.Vertex2D(dat,dat2,subject=subject, vmin=vmin, vmax=vmax,vmin2=vmin2,vmax2=vmax2,cmap=cmap)
    mfig=cortex.quickshow(light,with_curvature=True,with_rois=rois,with_colorbar=colorbar,fig=ax,with_labels=labels)
    
    
def zoom_to_roi(subject, roi, hem,ax, margin=15.0):
    roi_verts = cortex.get_roi_verts(subject, roi)[roi]
    roi_map = cortex.Vertex.empty(subject)
    roi_map.data[roi_verts] = 1

    (lflatpts, lpolys), (rflatpts, rpolys) = cortex.db.get_surf(subject, "flat",
                                                                nudge=True)
    sel_pts = dict(left=lflatpts, right=rflatpts)[hem]
    roi_pts = sel_pts[np.nonzero(getattr(roi_map, hem))[0],:2]

    xmin, ymin = roi_pts.min(0) - margin
    xmax, ymax = roi_pts.max(0) + margin
    
    
    ax.axis([xmin, xmax, ymin, ymax])
    print([xmin, xmax, ymin, ymax])
    return


def zoom_to_rect(myrect):
    plt.axis(myrect)


    
def zoomed_plot(dat,vmin,vmax,ROI,hem,subject='fsaverage',rois=False,colorbar=False,cmap='plasma',ax=None,labels=True,alpha=False):
    
    basic_plot(dat,vmax,subject,vmin,rois,colorbar,cmap,ax,labels)
        
    zoom_to_roi(subject,ROI,hem,ax)
    
def zoomed_alpha_plot(dat,dat2,vmin,vmax,vmin2,vmax2,ROI,hem,subject='fsaverage',rois=False,colorbar=False,cmap='plasma',ax=None,labels=True,alpha=False):
    alpha_plot(dat,dat2,vmin,vmax,vmin2,vmax2,cmap=cmap,rois=rois,labels=labels)
    zoom_to_roi(subject,ROI,hem)
    
    
def zoomed_plot2(dat,vmin,vmax,subject='fsaverage',rect=[-229.33542, -121.50809, -117.665405, 28.478895],rois=False,colorbar=False,cmap='plasma',ax=None,labels=True):
    basic_plot(dat,vmax,subject,vmin,rois,colorbar,cmap,ax,labels)
    zoom_to_rect(rect)
    
    
def zoomed_alpha_plot2(dat,dat2,vmin,vmax,vmin2,vmax2,subject='hcp_999999',rect=[-229.33542, -121.50809, -117.665405, 28.478895],rois=False,colorbar=False,cmap='plasma',ax=None,labels=True):
    alpha_plot(dat,dat2,vmin,vmax,vmin2,vmax2,cmap=cmap,rois=rois,labels=labels)
    zoom_to_rect(rect)