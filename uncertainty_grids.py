from regular_grid import get_subset, get_3D
from scipy import interpolate
import numpy as np
from itertools import product
from keras.models import load_model
import gdal


def entropy(probabilities):
    return np.nansum([n * np.log(n) for n in probabilities])*-1/np.log(18)


def CIfunction(arr):
    sort_indices = np.argsort(arr)
    return 1 - (arr[sort_indices[-1]] - arr[sort_indices[-2]])


def train_vali(subset):
    grouped_DF = subset.groupby(['x', 'y'])
    groups = np.arange(grouped_DF.ngroups)
    np.random.seed(0)
    sampling = np.random.choice(groups,
                                size=round(0.1*grouped_DF.ngroups),
                                replace=False)
    test = subset[grouped_DF.ngroup().isin(sampling)]
    others = subset[~grouped_DF.ngroup().isin(sampling)]
    return test, others


def uncertainties2D(subset, repetitions, model, raster_path):
    src = gdal.Open(raster_path)
    geo = src.GetGeoTransform()
    rb = src.GetRasterBand(1)
    x_min, x_max = subset.x.min(), subset.x.max()
    y_min, y_max = subset.y.min(), subset.y.max()
    z_min, z_max = subset.z.min(), subset.z.max()
    points_int_x, points_int_y = np.arange(x_min, x_max, 100), np.arange(y_min, y_max, 100)
    xys_toint = list(product(points_int_y, points_int_x))
    test, others = train_vali(subset)
    others_grouped = others.groupby(['x', 'y'])
    others_groups = np.arange(others_grouped.ngroups)
    z_min, z_max = subset.z.min(), subset.z.max()
    lins = []
    for n in range(repetitions):
        train_sampling = np.random.choice(others_groups,
                                          size=round(0.9*others_grouped.ngroups),
                                          replace=False)
        training = others[others_grouped.ngroup().isin(train_sampling)]
        Lnss = []
        for x in np.arange(0, 60, 1):
            de = 1
            z = np.arange(z_min+x-0.5, z_min+x+0.5, de)
            points_train = training[(training.z > z[0]*de) &
                                    (training.z < (z[0]+1)*de)]

            Ln = interpolate.LinearNDInterpolator(points_train[['y', 'x']].values,
                                                  np.array(points_train['mean'].tolist()))
            Ln_int = Ln(xys_toint)
            Lns = model.predict(Ln_int, verbose=0)

            Lns.sort(axis=1)
            CIs = np.apply_along_axis(CIfunction, axis=1, arr=Lns)
            entro = np.apply_along_axis(entropy, axis=1, arr=Lns)

            elev = []
            for m in xys_toint[:]:
                mx, my = m[1], m[0]
                px = int((mx - geo[0])/geo[1])
                py = int((my - geo[3])/geo[5])
                intval = rb.ReadAsArray(px, py, 1, 1)
                elev.append(intval[0][0])

            elev = [e - x - 0.5 for e in elev]
            yxs = np.array([[n[0], n[1]] for n in xys_toint])
            yxzsLn = np.hstack((yxs,
                                np.array(elev).reshape(-1, 1),
                                CIs.reshape(-1, 1),
                                entro.reshape(-1, 1)))
            Lnss.append(yxzsLn)
        Lns1 = np.vstack(Lnss)
        lins.append(Lns1)
        return lins


def CI_points(list_arrays, mask=False):
    yxs = list_arrays[0][:, :3]
    Cis = np.stack([n[:, 3] for n in list_arrays], axis=1)
    ConfusionIndex = np.apply_along_axis(np.nanmean, axis=1, arr=Cis)
    return np.hstack([yxs,
                      ConfusionIndex.reshape(-1, 1)])


def Ent_points(list_arrays, mask=False):
    yxs = list_arrays[0][:, :3]
    Ents = np.stack([n[:, 4] for n in list_arrays], axis=1)
    Entropies = np.apply_along_axis(np.nanmean, axis=1, arr=Ents)
    return np.hstack([yxs,
                      Entropies.reshape(-1, 1)])


# demPath = '/home/ignacio/Documents/chapter2/DEM_NSW.tif'
# model = load_model('mlp_prob_model.h5')
# dataPath = 'surveyed2_emb_depth.pkl'
# shapefilePath = '/home/ignacio/Documents/chapter2/AOIs/Moree.shp'
# Moree = get_subset(dataPath, shapefilePath)
# uncsss = uncertainties2D(Moree, 10, model, demPath)
# Confusion2D = CI_points(uncsss, True)
# Entropy2D = Ent_points(uncsss, True)
# Ent3D = get_3D(Entropy2D, Moree, 100,
#                depthMask=175, xMask=772500, yMask=6740000)
# print(np.nanmax(Ent3D), np.nanmin(Ent3D), np.nanmean(Ent3D))
#
# CI3D = get_3D(Confusion2D, Moree, 100,
#               depthMask=175, xMask=772500, yMask=6740000)
# print(np.nanmax(CI3D), np.nanmin(CI3D), np.nanmean(CI3D))
