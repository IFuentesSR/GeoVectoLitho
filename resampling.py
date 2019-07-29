from __future__ import division
import pandas as pd
from gallerini import geoSurvey


def resampling(predDF_path):
    '''Function that creates a resampled pandas dataframe using the Gallerini &
    Donatis methodology
    Inputs:
        -predDF_path: path to your MLP predicted lithological classes
    Outputs:
        -toMap: resampled pandas dataframe'''
    cols_in = ['x', 'y', 'ToDepth', 'FromDepth', 'code', 'mean', 'pred']
    cols_out = ['x', 'y', 'z', 'class', 'mean', 'pred']
    DF = pd.read_pickle(predDF_path)
    DF['TopElev'] = pd.to_numeric(DF['TopElev'])
    DF['BottomElev'] = pd.to_numeric(DF['BottomElev'])
    DF = DF[DF.BottomElev > -1200]
    index = range(len(DF))
    DF['ix'] = index
    DF = DF.set_index('ix')
    toMap = geoSurvey(Dataframe=DF, cols_in=cols_in, cols_out=cols_out, Imax=1)
    return toMap


resampled = resampling('/home/ignacio/Documents/chapter2/GeoVectoLitho/NSWpredictions.pkl')
resampled.to_pickle('surveyed2_emb_depth.pkl')
