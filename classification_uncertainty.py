from keras.models import load_model
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def entropy(probabilities):
    return np.nansum([n * np.log(n) for n in probabilities])*-1/np.log(18)


def get_entropies(embeddings_path, model):
    '''Function to create entropies from embeddings
    Inputs:
        -embeddings_path: dataframe with embeddings
        -model: mlp model trained
    Outputs:
        -ent_mean: mean entropy per lithological class
        -quantity: quantity (%) of lithological class'''
    ver = pd.read_pickle(embeddings_path)
    probs = model.predict(np.array(ver['mean'].tolist()))
    ver['probs'] = probs.tolist()
    ver['entropy'] = ver['probs'].apply(lambda x: entropy(x))
    ent_mean = [ver[ver['pred'] == n].entropy.mean() for n in range(18)]
    quantity = [ver[ver['pred'] == n].entropy.count()/len(ver)*100 for n in range(18)]
    return ent_mean, quantity


def classification_entropies(mean_entropies, quantities, colors, patches, classes):
    '''Function to plot uncertainties and quantities for lithological classes
    Intputs:
        -mean_entropies: mean entropy per lithological class
        -quantities: quantity (%) of lithological class
        -colors: colors for lithologies
        -patches: patches for lithologies
        -classes: labels for lithological classes
    Outputs:
        -fig: barplot with uncertainties and quantities for lithologies'''
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].bar(classes, mean_entropies, color=cols, label='NSW',
              edgecolor='black')
    ax[0].set_ylim(0, 1)
    ax[0].tick_params(axis='y', labelsize=10)
    ax[0].set_ylabel('Mean entropy', fontsize=13)
    ax[0].tick_params(axis='x', which='both', bottom=False, top=False,
                      labelbottom=False)
    ax[1].bar(classes, quantities, color=colors, label='NSW',
              edgecolor='black')
    ax[1].tick_params(axis='y', labelsize=10)
    ax[1].tick_params(axis='x', which='both', bottom=False, top=False,
                      labelbottom=False)
    ax[1].set_ylabel('Lithological classes (%)', fontsize=13)
    lgd = fig.legend(handles=patches, ncol=6,
                     fontsize='small', bbox_to_anchor=(0.84, 0.17),
                     fancybox=True)
    fig.subplots_adjust(bottom=0.7)
    fig.tight_layout()
    return fig


litho_classes = {0: 'alluvium', 1: 'bedrock', 2: 'carbonaceous',
                 3: 'cavity', 4: 'chemical', 5: 'coarse sediments',
                 6: 'conglomerate', 7: 'fine sediments', 8: 'intrusive',
                 9: 'limestone', 10: 'metamorphic', 11: 'peat',
                 12: 'sandstone', 13: 'sedimentary', 14: 'shale',
                 15: 'soil', 16: 'volcanic', 17: 'water', 18: 'empty'}

litho_colors = {0: (0.2, 0.15, 0.05, 0.4), 1: (0.8, 0.8, 0.8, 0.7),
                2: (0.6, 0.4, 0.05, 0.6), 3: (0.8, 0.9, 0.1, 0.2),
                4: (0.4, 0.4, 0.9, 0.6), 5: (0.7, 0.7, 0.5, 1),
                6: (0.1, 0.2, 0.1, 0.7), 7: (0.54, 0.3, 0.04, 1),
                8: (0.9, 0.3, 0.2, 0.6), 9: (0.85, 0.96, 0.1, 0.6),
                10: (0.95, 0.8, 0.1, 0.7), 11: (0.25, 0.8, 0.3, 0.4),
                12: (0.9, 0.06, 0.5, 0.6), 13: (0.2, 0.5, 0.4, 0.6),
                14: (0.35, 0.45, 0.5, 0.7), 15: (0.5, 0.5, 0.2, 0.8),
                16: (0.45, 0.36, 0.46, 0.7), 17: (0.4, 0.8, 0.99, 0.4),
                18: (1, 1, 1, 0)}

classes = ['alluvium', 'bedrock', 'carbonaceous', 'cavity', 'chemical',
           'coarse sediments', 'conglomerate', 'fine sediments', 'intrusive',
           'limestone', 'metamorphic', 'peat', 'sandstone', 'sedimentary',
           'shale', 'soil', 'volcanic', 'water']

cols = [litho_colors[n] for n in range(18)]
patches = [mpatches.Patch(color=litho_colors[n], label=litho_classes[n])
           for n in range(18)]
model = load_model('mlp_prob_model.h5')
embeddings_path = 'NSWpredictions.pkl'

# ents, quants = get_entropies(embeddings_path, model)
# figure = classification_entropies(ents, quants, cols, patches, classes)
