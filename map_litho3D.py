from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches
# one issue is that plt.voxels requieres a lot of memory, therefore
# if no resampling is applied, consider memory limits

geo2D_path = 'points_Moree_Ln.npy'
geo3D_path = 'MoreeRecakeLn.npy'


litho_classes = {0: 'alluvium', 1: 'bedrock', 2: 'carbonaceous',
                 3: 'cavity', 4: 'chemical', 5: 'coarse sediments', 6: 'conglomerate',
                 7: 'fine sediments', 8: 'intrusive', 9: 'limestone', 10: 'metamorphic',
                 11: 'peat', 12: 'sandstone', 13: 'sedimentary', 14: 'shale',
                 15: 'soil', 16: 'volcanic', 17: 'water', 18: 'empty'}

litho_colors = {0: (0.2, 0.15, 0.05, 0.4), 1: (0.8, 0.8, 0.8, 0.7),
                2: (0.3, 0.4, 0.05, 0.6), 3: (0.8, 0.9, 0.1, 0.2),
                4: (0.4, 0.4, 0.9, 0.6), 5: (0.7, 0.7, 0.5, 1),
                6: (0.1, 0.2, 0.1, 0.7), 7: (0.54, 0.3, 0.04, 1),
                8: (0.9, 0.3, 0.2, 0.6), 9: (0.85, 0.96, 0.1, 0.6),
                10: (0.95, 0.8, 0.1, 0.7), 11: (0.25, 0.8, 0.3, 0.4),
                12: (0.9, 0.06, 0.5, 0.6), 13: (0.2, 0.35, 0.4, 0.6),
                14: (0.35, 0.45, 0.5, 0.7), 15: (0.5, 0.5, 0.2, 0.8),
                16: (0.45, 0.36, 0.46, 0.7), 17: (0.4, 0.8, 0.99, 0.4),
                18: (1, 1, 1, 0)}


def preprocess_3Ddata(geo3D_path):
    recake = np.load(geo3D_path)
    recake1 = recake[::-1, ::-1, ::-1]
    recake1 = recake1[:, :, :]
    recake1[np.isnan(recake1)] = 18
    recake1[recake1 == 0] = 18
    classes_array = recake1.astype('int16')
    return classes_array


def preprocess_2Ddata(geo2D_path, depthMask=np.nan, xMask=np.nan, yMask=np.nan):
    data1 = np.load(geo2D_path)
    masked = (data1[:, 2] > depthMask) & (data1[:, 1] < xMask) & (data1[:, 0] > yMask)
    data_sliced = data1[~masked]
    return data_sliced


def explode(data):
    shape_arr = np.array(data.shape)
    size = shape_arr[:3]*2 - 1
    exploded = np.zeros(np.concatenate([size, shape_arr[3:]]),
                        dtype=data.dtype)
    exploded[::2, ::2, ::2] = data
    return exploded


def expand_coordinates(indices):
    x, y, z = indices
    x[1::2, :, :] += 1
    y[:, 1::2, :] += 1
    z[:, :, 1::2] += 1
    return x, y, z


def plot3D(x, y, z, unprocessed2D, processed2D, filled, facecolors, title, figsize=(10, 8), elevation=30, azimuth=320):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.view_init(elevation, azimuth)
    ax.tick_params(axis='both', labelsize=16)
    ax.set_xlabel('x', fontsize=16)
    ax.set_xticks(np.linspace(np.min(x), np.max(x), 4))
    ax.set_xticklabels(np.round(np.linspace(np.max(unprocessed2D[:, 1]),
                                            np.min(unprocessed2D[:, 1]),
                                            4), 1))
    ax.set_ylabel('y', fontsize=16)
    ax.set_yticks(np.linspace(np.min(y), np.max(y), 4))
    ax.set_yticklabels(np.round(np.linspace(np.max(unprocessed2D[:, 0]),
                                            np.min(unprocessed2D[:, 0]),
                                            4), 1))
    ax.set_zlabel('z', fontsize=16)
    ax.set_zticks(np.linspace(np.min(z)-80, np.max(z)+80, 4))
    ax.set_zticklabels(np.round(np.linspace(np.min(processed2D[:, 2])-80*((np.max(processed2D[:, 2])-np.min(processed2D[:, 2]))/(np.max(z)-np.min(z))),
                                np.max(processed2D[:, 2])+80*((np.max(processed2D[:, 2])-np.min(processed2D[:, 2]))/(np.max(z)-np.min(z))),
                                4), 1))
    ax.set_zlim3d(np.min(z)-80, np.max(z)+80)
    ax.voxels(x, y, z, filled, facecolors=facecolors)
    ax.set_title(title, fontsize=18, loc='left', fontweight='bold')
    fig.tight_layout()
    return fig


data1 = np.load(geo2D_path)
processed3D = preprocess_3Ddata(geo3D_path)
processed2D = preprocess_2Ddata(geo2D_path)
patches = [mpatches.Patch(color=litho_colors[n], label=litho_classes[n]) for n in np.unique(processed2D[:, 3])]
facecolors = np.array([litho_colors.get(i, -1) for i in range(processed3D.min(), processed3D.max() + 1)])
facecolors = facecolors[(processed3D - processed3D.min())]
facecolors = explode(facecolors)
filled = facecolors[:, :, :, -1] != 0
z, y, x = expand_coordinates(np.indices(np.array(filled.shape) + 1))

figure = plot3D(x, y, z, data1, processed2D, filled, facecolors, 'Lin')
figure.savefig('test.png', dpi=300)
