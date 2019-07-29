import pandas as pd
import numpy as np
from scipy import interpolate
from itertools import product
import gdal
import ogr
import json
from sklearn.preprocessing import OneHotEncoder
from keras.models import load_model
one_enc = OneHotEncoder()
# DEM and shapefile must be in the same projection that the dataframe (in this
# case all were projected using crs = epsg:37255)

model = load_model('mlp_prob_model.h5')
dataPath = 'surveyed2_emb_depth.pkl'
shapefilePath = '/home/ignacio/Documents/chapter2/AOIs/Moree.shp'
demPath = '/home/ignacio/Documents/chapter2/DEM_NSW.tif'


def find_idxs(arr, arr_B):
    ans = np.where(np.sum(np.expand_dims(arr, 0) == arr_B, 1) == 2)[0]
    if len(ans):
        return ans[0]
    return np.nan


def get_subset(resampledDF_path, shapefile_path):
    '''Function that subset Gallerini resampled dataframe based on shapefile
    Inputs:
        -resampledDF_path: path to Gallerini resampled dataframe
        -shapefile_path: path to shapefile
    Outputs:
        -subset: subset of the resampled dataset based on shapefile limits'''
    data = pd.read_pickle(resampledDF_path)
    encodes = one_enc.fit_transform(data['class'].values.reshape(-1,
                                                                 1)).toarray()
    file = ogr.Open(shapefile_path)
    feature = file.GetLayer(0).GetFeature(0)
    bounds = np.array(json.loads(feature.ExportToJson())['geometry']['coordinates'][0])
    xbounds, ybounds = bounds[:, 0], bounds[:, 1]
    AOI_Ymax, AOI_Ymin = np.max(ybounds), np.min(ybounds)
    AOI_Xmax, AOI_Xmin = np.max(xbounds), np.min(xbounds)
    subset = data[(data.x >= AOI_Xmin) & (data.x <= AOI_Xmax) &
                  (data.y >= AOI_Ymin) & (data.y <= AOI_Ymax)]
    return subset


def split_dataset(subset):
    '''Function that split dataset into test, training and validation subsets
    Inputs:
        -subset: subset dataframe based on shapefile extent
    Outputs:
        -test: test subset
        -training: training subset
        -validation: validation subset'''
    grouped_DF = subset.groupby(['x', 'y'])
    groups = np.arange(grouped_DF.ngroups)
    np.random.seed(0)
    sampling = np.random.choice(groups,
                                size=round(0.1*grouped_DF.ngroups),
                                replace=False)
    test = subset[grouped_DF.ngroup().isin(sampling)]
    others = subset[~grouped_DF.ngroup().isin(sampling)]
    others_grouped = others.groupby(['x', 'y'])
    others_groups = np.arange(others_grouped.ngroups)
    train_sampling = np.random.choice(others_groups,
                                      size=round(0.9*others_grouped.ngroups),
                                      replace=False)
    training = others[others_grouped.ngroup().isin(train_sampling)]
    validation = others[~others_grouped.ngroup().isin(train_sampling)]
    return test, training, validation


def get_2D(resampledDF_path, shapefile_path, dem_path, scale, depth_interval=1):
    '''Function that generates a numpy array with coordinates and litho classes
    Inputs:
        -resampledDF_path: path to Gallerini resampled dataframe
        -shapefile_path: path to shapefile
        -dem_path: path to DEM raster
        -scale: scale of mapping
        -depth_interval: depth interval for mapping
    Outputs:
        -data2: numpy array with coordinates and interpolated litho classes'''

    subset = get_subset(resampledDF_path, shapefile_path)
    src = gdal.Open(dem_path)
    geo = src.GetGeoTransform()
    rb = src.GetRasterBand(1)
    test, training, validation = split_dataset(subset)
    x_min, x_max = subset.x.min(), subset.x.max()
    y_min, y_max = subset.y.min(), subset.y.max()
    z_min, z_max = subset.z.min(), subset.z.max()
    points_int_x, points_int_y = np.arange(x_min, x_max, scale), np.arange(y_min, y_max, scale)
    # y rows, x columns
    xys_toint = list(product(points_int_y, points_int_x))
    data1 = []
    for n in range(60):
        de = depth_interval
        z = np.arange(z_min+n-0.5, z_min+n+0.5, de)
        points_train = training[(training.z > z[0]*de) & (training.z < (z[0]+1)*de)]
        Ln = interpolate.LinearNDInterpolator(points_train[['y', 'x']].values,
                                              np.array(points_train['mean'].tolist()))
        Ln_int = Ln(xys_toint)
        Lns = model.predict(Ln_int, verbose=0)
        onehot_Ln = np.zeros((Lns.shape[0], 18))
        onehot_Ln[np.arange(len(Lns)), Lns.argmax(axis=1)] = 1
        codes_Ln = one_enc.inverse_transform(onehot_Ln)
        elev = []
        for m in xys_toint[:]:
            mx, my = m[1], m[0]
            px = int((mx - geo[0])/geo[1])
            py = int((my - geo[3])/geo[5])
            intval = rb.ReadAsArray(px, py, 1, 1)
            elev.append(intval[0][0])

        elev = [e - n - 0.5 for e in elev]
        yxs = np.array([[n[0], n[1]] for n in xys_toint])
        yxzs = np.hstack((yxs,
                          np.array(elev).reshape(-1, 1),
                          codes_Ln.reshape(-1, 1)))
        data1.append(yxzs)
    data2 = np.vstack(data1)
    return data2


def get_3D(geo2D, subset, scale, depthMask=np.nan, xMask=np.nan, yMask=np.nan):
    '''Function that generates a 3D numpy array with coordinates and litho classes
    Inputs:
        -geo2D: numpy array with coordinates and interpolated litho classes
        -scale: scale of mapping
        -subset: subset of the resampled dataset based on shapefile limits
        -depthMask: depth to mask 3D map
        -xMask: x coordinate to mask 3D map
        -yMask: y coordinate to mask 3D map
    Outputs:
        -recake: 3Darray to map interpolated lithologies from embeddings'''
    masked = (geo2D[:, 2] > depthMask) & (geo2D[:, 1] < xMask) & (geo2D[:, 0] > yMask)
    geo2D = geo2D[~masked]
    z_grid = np.arange(np.max(geo2D[:, 2]), np.min(geo2D[:, 2]), -1)
    x_min, x_max = subset['x'].min(), subset['x'].max()
    y_min, y_max = subset['y'].min(), subset['y'].max()
    points_int_x, points_int_y = np.arange(x_min, x_max, scale), np.arange(y_min, y_max, scale)
    xys_toint = list(product(points_int_y, points_int_x))
    yxs = np.array([[m[0], m[1]] for m in xys_toint])
    yxs = np.hstack((yxs,
                     np.array([np.nan]*len(yxs)).reshape(-1, 1),
                     np.array([np.nan]*len(yxs)).reshape(-1, 1)))

    recake = np.zeros(shape=(z_grid.shape[0],
                             np.arange(y_min, y_max, scale).shape[0],
                             np.arange(x_min, x_max, scale).shape[0]))
    for i, n in enumerate(z_grid):
        data3 = geo2D[np.where((geo2D[:, 2] > n - 0.5) & (geo2D[:, 2] <= n + 0.5))]
        print(i, data3.shape[0])
        sort_indexs = np.lexsort((data3[:, 1], data3[:, 0]))
        data4 = data3[sort_indexs]
        indexes = np.apply_along_axis(find_idxs, 1, data4[:, 0:2], yxs[:, 0:2])
        yxs[indexes, 2], yxs[indexes, 3] = data4[:, 2], data4[:, 3]
        recake[i, :, :] = yxs[:, 3].reshape(np.arange(y_min, y_max, scale).shape[0],
                                            np.arange(x_min, x_max, scale).shape[0])
    return recake


# subset_data = get_subset(dataPath, shapefilePath)
#
# geo2D_data = get_2D(dataPath, shapefilePath, demPath, 100)
# np.save('points_Moree_Ln.npy', geo2D_data)
#
#
# recake = get_3D(geo2D_data, subset_data, 100,
#                 depthMask=175, xMask=772500, yMask=6740000)
#
# np.save('MoreeRecakeLn.npy', recake)
