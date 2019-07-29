import os
import geopandas
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# Replace Dir with path of groundwaterExplorer files
Dir = '/home/ignacio/Downloads/groundwaterExplorer/shp_NSW'


def litho_Dataframe(path):
    '''Function that creates a single georeferenced dataframe with
    lithologic descriptions
    Input:
        -path: path to groundwater explorer files
    Output:
        -DF: pandas dataframe with georeferenced lithologic descriptions'''

    shapefile = 'NGIS_Bore.shp'
    lithologs = 'NGIS_LithologyLog.csv'

    shapefile_df = geopandas.read_file(os.path.join(path, shapefile))
    shapefile_df = shapefile_df.set_index('HydroCode')
    shapefile_df['geometry'] = shapefile_df['geometry'].to_crs(epsg=32755)
    litho_df = pd.read_csv(os.path.join(path, lithologs))
    litho_df = litho_df.set_index('HydroCode')
    litho_df['HydroCode'] = litho_df.index
    litho_df['geometry'] = shapefile_df['geometry']
    DF2 = litho_df[['Description', 'HydroCode', 'FromDepth', 'ToDepth',
                    'TopElev', 'BottomElev', 'MajorLithCode', 'geometry']]
    DF2 = DF2.dropna(how='any')
    DF2 = DF2[(DF2['TopElev'] != 'None') & (DF2['BottomElev'] != 'None')]
    DF2['z'] = (pd.to_numeric(DF2.TopElev) + pd.to_numeric(DF2.BottomElev))/2
    DF = DF2.copy()
    DF['FromDepth'] = pd.to_numeric(DF.FromDepth)
    DF['ToDepth'] = pd.to_numeric(DF.ToDepth)
    DF['TopElev'] = pd.to_numeric(DF.TopElev)
    DF['BottomElev'] = pd.to_numeric(DF.BottomElev)
    print('number of original litho classes:', len(DF.MajorLithCode.unique()))
    return DF


def manual_reclass(DF):
    '''Function that uses a set of RE rules for manual classification
    and aggregation
    Inputs:
        -DF: original dataframe_file
    Outputs:
        -DFint1: output dataframe containing 18 major lithological classes
        manually obtained'''
    DF['OWN'] = np.nan
    DF['OWN'][DF.MajorLithCode == 'OPAL'] = 'opal'
    DF['OWN'][DF.MajorLithCode == 'PRNX'] = 'pyroxenite'
    DF['OWN'][DF.MajorLithCode == 'PDRY'] = 'shale'
    DF['OWN'][DF.MajorLithCode == 'VTRC'] = 'volcanic'
    DF['OWN'][DF.MajorLithCode == '14'] = 'pyrite'
    DF['OWN'][DF.MajorLithCode == 'XCST'] = 'tuff'
    DF['OWN'][DF.MajorLithCode == 'CLBN'] = 'coal'
    DF['OWN'][DF.MajorLithCode == 'APTT'] = 'apatite'
    DF['OWN'][DF.MajorLithCode == 'SDRK'] = 'sand'
    DF['OWN'][DF.MajorLithCode == '07'] = 'lignite'
    DF['OWN'][DF.MajorLithCode == '09'] = 'marble'
    DF['OWN'][DF.MajorLithCode == 'PRLS'] = 'pyroclastic'
    DF['OWN'][DF.MajorLithCode == 'LGNC'] = 'lignite'
    DF['OWN'][DF.MajorLithCode == '13'] = 'peat'
    DF['OWN'][DF.MajorLithCode == 'GRNC'] = 'granite'
    DF['OWN'][DF.MajorLithCode == 'ALBT'] = 'bitumen'
    DF['OWN'][DF.MajorLithCode == 'PRPC'] = 'porphyry'
    DF['OWN'][DF.MajorLithCode == 'PGGY'] = 'clay'
    DF['OWN'][DF.MajorLithCode == 'LRED'] = 'clay'
    DF['OWN'][DF.MajorLithCode == 'STFF'] = 'clay'
    DF['OWN'][DF.MajorLithCode == 'PGMT'] = 'pegmatite'
    DF['OWN'][DF.MajorLithCode == 'LTIT'] = 'latite'
    DF['OWN'][DF.MajorLithCode == 'CBSK'] = 'carbonaceous'
    DF['OWN'][DF.MajorLithCode == 'FLDR'] = 'basalt'
    DF['OWN'][DF.MajorLithCode == 'CSSD'] = 'sand gravel'
    DF['OWN'][DF.MajorLithCode == 'HCMB'] = 'basalt'
    DF['OWN'][DF.MajorLithCode == 'BRRC'] = 'basalt'
    DF['OWN'][DF.MajorLithCode == 'DCRM'] = 'clay'
    DF['OWN'][DF.MajorLithCode == 'BRCB'] = 'clay'
    DF['OWN'][DF.MajorLithCode == 'MDDY'] = 'clay'
    DF['OWN'][DF.MajorLithCode == 'SLRN'] = 'andesite'
    DF['OWN'][DF.MajorLithCode == 'AGLC'] = 'argillite'
    DF['OWN'][DF.MajorLithCode == 'ARGL'] = 'argillite'
    DF['OWN'][DF.MajorLithCode == 'TRSC'] = 'sandstone'
    DF['OWN'][DF.MajorLithCode == '08'] = 'limestone'
    DF['OWN'][DF.MajorLithCode == 'CLPN'] = 'clay'
    DF['OWN'][DF.MajorLithCode == 'PETY'] = 'clay'
    DF['OWN'][DF.MajorLithCode == 'KNKR'] = 'clay'
    DF['OWN'][DF.MajorLithCode == 'VGTN'] = 'soil'
    DF['OWN'][DF.MajorLithCode == 'CSLN'] = 'coal'
    DF['OWN'][DF.MajorLithCode == 'FORM'] = 'sand'
    DF['OWN'][DF.MajorLithCode == 'CBLL'] = 'sand'
    DF['OWN'][DF.MajorLithCode == 'TRCT'] = 'trachyte'
    DF['OWN'][DF.MajorLithCode == 'MRBL'] = 'marble'
    DF['OWN'][DF.MajorLithCode == 'BAR'] = 'cement'
    DF['OWN'][DF.MajorLithCode == 'FRCL'] = 'clay'
    DF['OWN'][DF.MajorLithCode == 'BUXT'] = 'bauxite'
    DF['OWN'][DF.MajorLithCode == 'GRYL'] = 'drift'
    DF['OWN'][(DF.MajorLithCode == 'VRGD') &
              (DF.Description.str.contains('clay'))] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'VRGD') &
              (DF.Description.str.contains('sand'))] = 'sand'
    DF['OWN'][(DF.MajorLithCode == 'LYSD') &
              (DF.Description.str.contains('Clayey sand'))] = 'clay sand'
    DF['OWN'][(DF.MajorLithCode == 'LYSD') &
              (DF.Description.str.contains('loam'))] = 'sandy loam'
    DF['OWN'][(DF.MajorLithCode == 'EVPR') &
              (DF.Description.str.contains('basalt'))] = 'basalt'
    DF['OWN'][(DF.MajorLithCode == 'DBLY') &
              (DF.Description.str.contains('basalt'))] = 'basalt'
    DF['OWN'][(DF.MajorLithCode == 'DBLY') &
              (DF.Description.str.contains('clay'))] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'DBLY') &
              (DF.Description.str.contains('sand'))] = 'sand'
    DF['OWN'][(DF.MajorLithCode == 'DBLY') &
              (DF.Description.str.contains('shale'))] = 'shale'
    DF['OWN'][(DF.MajorLithCode == 'TALC') &
              (DF.Description.str.contains('clay'))] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'TALC') &
              (DF.Description.str.contains('silty'))] = 'silty clay'
    DF['OWN'][(DF.MajorLithCode == 'MTLD') &
              (DF.Description.str.contains('clay'))] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'MTLD') &
              (DF.Description.str.contains('silty'))] = 'silty clay'
    DF['OWN'][(DF.MajorLithCode == 'CLBA') &
              (DF.Description.str.contains('Clay'))] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'CLBA') &
              (DF.Description.str.contains('sand'))] = 'clay sand'
    DF['OWN'][(DF.MajorLithCode == 'FREE') &
              (DF.Description.str.contains('sand'))] = 'sand'
    DF['OWN'][(DF.MajorLithCode == 'FREE') &
              (DF.Description.str.contains('granite'))] = 'granite'
    DF['OWN'][(DF.MajorLithCode == 'MDGD') &
              (DF.Description.str.contains('sand'))] = 'sand'
    DF['OWN'][(DF.MajorLithCode == 'MDGD') &
              (DF.Description.str.contains('soil'))] = 'soil'
    DF['OWN'][(DF.MajorLithCode == 'MDGD') &
              (DF.Description.str.contains('stone'))] = 'mudstone'
    DF['OWN'][(DF.MajorLithCode == 'GRSD') &
              (DF.Description.str.contains('sand'))] = 'sand gravel'
    DF['OWN'][(DF.MajorLithCode == 'GRSD') &
              (DF.Description.str.contains('clay'))] = 'clay gravel'
    DF['OWN'][(DF.MajorLithCode == 'AOLN') &
              (DF.Description.str.contains('sand'))] = 'sand'
    DF['OWN'][(DF.MajorLithCode == 'AOLN') &
              (DF.Description.str.contains('basalt'))] = 'basalt'
    DF['OWN'][(DF.MajorLithCode == 'FRLY') &
              (DF.Description.str.contains('clay'))] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'FRLY') &
              (DF.Description.str.contains('sand'))] = 'sand'
    DF['OWN'][(DF.MajorLithCode == 'FRLY') &
              (DF.Description.str.contains('soil'))] = 'soil'
    DF['OWN'][(DF.MajorLithCode == 'FRLY') &
              ((DF.Description.str.contains('sand')) &
               (DF.Description.str.contains('clay')))] = 'clay sand'
    DF['OWN'][(DF.MajorLithCode == 'FIRM') &
              (DF.Description.str.contains('basalt'))] = 'basalt'
    DF['OWN'][(DF.MajorLithCode == 'FIRM') &
              (DF.Description.str.contains('sand'))] = 'sand'
    DF['OWN'][(DF.MajorLithCode == 'FIRM') &
              (DF.Description.str.contains('clay'))] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'FIRM') &
              (DF.Description.str.contains('sandstone'))] = 'sandstone'
    DF['OWN'][(DF.MajorLithCode == 'FIRM') &
              (DF.Description.str.contains('granite'))] = 'granite'
    DF['OWN'][(DF.MajorLithCode == 'FIRM') &
              (DF.Description.str.contains('shale'))] = 'shale'
    DF['OWN'][(DF.MajorLithCode == 'FIRM') &
              (DF.Description.str.contains('siltstone'))] = 'siltstone'
    DF['OWN'][(DF.MajorLithCode == 'GREY') &
              (DF.Description.str.contains('clay'))] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'GREY') &
              (DF.Description.str.contains('acke'))] = 'wacke'
    DF['OWN'][(DF.MajorLithCode == 'GREY') &
              (DF.Description.str.contains('shale'))] = 'shale'
    DF['OWN'][(DF.MajorLithCode == 'GREY') &
              (DF.Description.str.contains('sandstone'))] = 'sandstone'
    DF['OWN'][(DF.MajorLithCode == 'BECH') &
              (DF.Description.str.contains('sand'))] = 'sand'
    DF['OWN'][(DF.MajorLithCode == 'BECH') &
              (DF.Description.str.contains('clay'))] = 'sandy clay'
    DF['OWN'][(DF.MajorLithCode == 'PKBN') &
              (DF.Description.str.contains('granite'))] = 'granite'
    DF['OWN'][(DF.MajorLithCode == 'BCLC') &
              (DF.Description.str.contains('itumen'))] = 'bitumen'
    DF['OWN'][(DF.MajorLithCode == 'BCLC') &
              (DF.Description.str.contains('gravel'))] = 'gravel'
    DF['OWN'][(DF.MajorLithCode == 'MFIC') &
              (DF.Description.str.contains('monzo'))] = 'monzonite'
    DF['OWN'][(DF.MajorLithCode == 'MZNT') &
              (DF.Description.str.contains('Monzo'))] = 'monzonite'
    DF['OWN'][(DF.MajorLithCode == 'DCIT') &
              (DF.Description.str.contains('acite'))] = 'dacite'
    DF['OWN'][(DF.MajorLithCode == 'DCIT') &
              (DF.Description.str.contains('granite'))] = 'granite'
    DF['OWN'][(DF.MajorLithCode == 'SYNT') &
              (DF.Description.str.contains('yenite'))] = 'syenite'
    DF['OWN'][(DF.MajorLithCode == 'AMPB') &
              (DF.Description.str.contains('Amphibolite'))] = 'amphibolite'
    DF['OWN'][(DF.MajorLithCode == 'BJCN') &
              (DF.Description.str.contains('Basalt'))] = 'basalt'
    DF['OWN'][(DF.MajorLithCode == 'BJCN') &
              (DF.Description.str.contains('sand'))] = 'sand'
    DF['OWN'][(DF.MajorLithCode == 'BJCN') &
              (DF.Description.str.contains('clay'))] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'BJCN') &
              (DF.Description.str.contains('claystone'))] = 'claystone'
    DF['OWN'][(DF.MajorLithCode == 'BJCN') &
              (DF.Description.str.contains('granite'))] = 'granite'
    DF['OWN'][(DF.MajorLithCode == 'CORD') &
              (DF.Description.str.contains('slate'))] = 'slate'
    DF['OWN'][(DF.MajorLithCode == 'CORD') &
              (DF.Description.str.contains('schist'))] = 'schist'
    DF['OWN'][(DF.MajorLithCode == 'CORD') &
              (DF.Description.str.contains('Clay'))] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'CORD') &
              (DF.Description.str.contains('granite'))] = 'granite'
    DF['OWN'][(DF.MajorLithCode == 'CORD') &
              (DF.Description.str.contains('andstone'))] = 'sandstone'
    DF['OWN'][(DF.MajorLithCode == 'HMTT') &
              (DF.Description.str.contains('sandstone'))] = 'sandstone'
    DF['OWN'][(DF.MajorLithCode == 'HMTT') &
              (DF.Description.str.contains('volcano'))] = 'volcanic'
    DF['OWN'][(DF.MajorLithCode == 'HMTT') &
              (DF.Description.str.contains('conglomerate'))] = 'conglomerate'
    DF['OWN'][(DF.MajorLithCode == 'HMTT') &
              (DF.Description.str.contains('granite'))] = 'granite'
    DF['OWN'][(DF.MajorLithCode == 'HMTT') &
              (DF.Description.str.contains('andesite'))] = 'andesite'
    DF['OWN'][DF.MajorLithCode == 'MMPC'] = np.nan
    DF['OWN'][(DF.MajorLithCode == 'MMPC') &
              (DF.Description.str.contains('etamorphic'))] = 'metamorphic'
    DF['OWN'][(DF.MajorLithCode == 'MMPC') &
              (DF.Description.str.contains('siltstone'))] = 'siltstone'
    DF['OWN'][(DF.MajorLithCode == 'MMPC') &
              (DF.Description.str.contains('ornfels'))] = 'hornfels'
    DF['OWN'][(DF.MajorLithCode == 'MMPC') &
              (DF.Description.str.contains('sand'))] = 'sand'
    DF['OWN'][(DF.MajorLithCode == 'MMPC') &
              (DF.Description.str.contains('clay'))] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'MMPC') &
              ((DF.Description.str.contains('sand')) &
               (DF.Description.str.contains('clay')))] = 'clay sand'
    DF['OWN'][DF.MajorLithCode == 'CLCS'] = 'earth'
    DF['OWN'][(DF.MajorLithCode == 'CLCS') &
              (DF.Description.str.contains('shale'))] = 'shale'
    DF['OWN'][DF.MajorLithCode == '04'] = 'gypsum'
    DF['OWN'][(DF.MajorLithCode == '04') &
              (DF.Description.str.contains('sand'))] = 'sand'
    DF['OWN'][(DF.MajorLithCode == '04') &
              (DF.Description.str.contains('clay'))] = 'clay'
    DF['OWN'][DF.MajorLithCode == '01'] = 'coal'
    DF['OWN'][(DF.MajorLithCode == '01') &
              (DF.Description.str.contains('iltstone'))] = 'siltstone'
    DF['OWN'][(DF.MajorLithCode == '01') &
              (DF.Description.str.contains('udstone'))] = 'mudstone'
    DF['OWN'][(DF.MajorLithCode == 'CLRC') &
              (DF.Description.str.contains('schist'))] = 'schist'
    DF['OWN'][(DF.MajorLithCode == 'SDDF') &
              (DF.Description.str.contains('Sand'))] = 'sand'
    DF['OWN'][(DF.MajorLithCode == 'SDDF') &
              ((DF.Description.str.contains('Sand')) &
               (DF.Description.str.contains('silt')))] = 'silty sand'
    DF['OWN'][(DF.MajorLithCode == 'SDDF') &
              ((DF.Description.str.contains('Sand')) &
               (DF.Description.str.contains('clay')))] = 'clay sand'
    DF['OWN'][(DF.MajorLithCode == 'SDDF') &
              ((DF.Description.str.contains('Sand')) &
               (DF.Description.str.contains('gravel')))] = 'sand gravel'
    DF['OWN'][(DF.MajorLithCode == 'SDDF') &
              (DF.Description.str.contains('Carb'))] = 'carbonaceous'
    DF['OWN'][(DF.MajorLithCode == 'SDDF') &
              (DF.Description.str.contains('clay'))] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'CRBC') &
              (DF.Description.str.contains('Carb'))] = 'carbonaceous'
    DF['OWN'][(DF.MajorLithCode == 'STRK') &
              (DF.Description.str.contains('clay'))] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'STRK') &
              (DF.Description.str.contains('sand'))] = 'sand'
    DF['OWN'][DF.MajorLithCode == 'BOTT'] = 'bitumen'
    DF['OWN'][DF.MajorLithCode == 'MXTR'] = 'shale'
    DF['OWN'][DF.MajorLithCode == 'OIL'] = 'shale'
    DF['OWN'][DF.MajorLithCode == 'GRDR'] = 'granodiorite'
    DF['OWN'][(DF.MajorLithCode == 'BOTT') &
              (DF.Description.str.contains('Biotite'))] = 'biotite'
    DF['OWN'][DF.MajorLithCode == 'KLNT'] = 'kaolinite'
    DF['OWN'][DF.MajorLithCode == 'CBSS'] = 'carbonaceous'
    DF['OWN'][DF.MajorLithCode == 'GPSM'] = 'gypsum'
    DF['OWN'][DF.MajorLithCode == 'PBHZ'] = 'pebbles'
    DF['OWN'][DF.MajorLithCode == 'KOLN'] = 'kaolinite'
    DF['OWN'][DF.MajorLithCode == 'IROX'] = 'ironstone'
    DF['OWN'][DF.MajorLithCode == 'ALVL'] = 'drift'
    DF['OWN'][DF.MajorLithCode == 'SCOR'] = 'scoria'
    DF['OWN'][DF.MajorLithCode == 'CHCL'] = 'charcoal'
    DF['OWN'][DF.MajorLithCode == 'GNSS'] = 'gneiss'
    DF['OWN'][DF.MajorLithCode == 'CBLS'] = 'water'
    DF['OWN'][(DF.MajorLithCode == 'GNSS') &
              (DF.Description.str.contains('Green clay'))] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'GNSS') &
              (DF.Description.str.contains('Genise'))] = np.nan
    DF['OWN'][DF.MajorLithCode == 'QRTT'] = 'quartzite'
    DF['OWN'][DF.MajorLithCode == 'BDLR'] = np.nan
    DF['OWN'][DF.MajorLithCode == 'FOSL'] = np.nan
    DF['OWN'][DF.MajorLithCode == 'CORL'] = np.nan
    DF['OWN'][DF.MajorLithCode == 'GRPT'] = np.nan
    DF['OWN'][DF.MajorLithCode == 'CRST'] = np.nan
    DF['OWN'][DF.MajorLithCode == 'GRBL'] = np.nan
    DF['OWN'][DF.MajorLithCode == 'AOIL'] = np.nan
    DF['OWN'][DF.MajorLithCode == 'CLTE'] = np.nan
    DF['OWN'][(DF.MajorLithCode == 'CLTE') &
              (DF.Description.str.contains('Stones'))] = 'stones'
    DF['OWN'][DF.MajorLithCode == 'DPSL'] = np.nan
    DF['OWN'][DF.MajorLithCode == 'BORE'] = np.nan
    DF['OWN'][DF.MajorLithCode == 'PYRT'] = 'Pyrite'
    DF['OWN'][(DF.MajorLithCode == 'PYRT') &
              (DF.Description.str.contains('basalt'))] = 'basalt'
    DF['OWN'][(DF.MajorLithCode == 'PYRT') &
              (DF.Description.str.contains('limestone'))] = 'limestone'
    DF['OWN'][DF.MajorLithCode == 'ZOLT'] = 'zeolite'
    DF['OWN'][(DF.MajorLithCode == 'SHLY')] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'SLLY')] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'SLTE')] = 'slate'
    DF['OWN'][(DF.MajorLithCode == '1')] = 'coal'
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == '1')] = 'shale'
    DF['OWN'][(DF.Description.str.contains('ironstone')) &
              (DF.MajorLithCode == '1')] = 'ironstone'
    DF['OWN'][(DF.Description.str.contains('siltstone')) &
              (DF.MajorLithCode == '1')] = 'siltstone'
    DF['OWN'][(DF.Description.str.contains('tuff')) &
              (DF.MajorLithCode == '1')] = 'tuff'
    DF['OWN'][(DF.MajorLithCode == 'COAL')] = 'coal'
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == 'COAL')] = 'shale'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'COAL')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'COAL')] = 'clay'
    DF['OWN'][(DF.Description.str.contains('basalt')) &
              (DF.MajorLithCode == 'COAL')] = 'basalt'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'COAL')] = 'gravel'
    DF['OWN'][(DF.Description.str.contains('sandstone')) &
              (DF.MajorLithCode == 'COAL')] = 'sandstone'
    DF['OWN'][(DF.Description.str.contains('silty')) &
              (DF.MajorLithCode == 'COAL')] = 'silty'
    DF['OWN'][((DF.Description.str.contains('siltstone')) |
               (DF.Description.str.contains('Siltstone'))) &
              (DF.MajorLithCode == 'COAL')] = 'siltstone'
    DF['OWN'][(DF.Description.str.contains('claystone')) &
              (DF.MajorLithCode == 'COAL')] = 'claystone'
    DF['OWN'][(DF.Description.str.contains('mudstone')) &
              (DF.MajorLithCode == 'COAL')] = 'mudstone'
    DF['OWN'][(DF.MajorLithCode == 'CMNT')] = 'cement'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'CMNT')] = 'gravel'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'CMNT')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'CMNT')] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'SDMN')] = 'sedimentary'
    DF['OWN'][(DF.MajorLithCode == 'DLMT')] = 'dolomite'
    DF['OWN'][(DF.MajorLithCode == 'AGLM')] = 'agglomerate'
    DF['OWN'][(DF.MajorLithCode == 'CRBN')] = 'carbonaceous'
    DF['OWN'][(DF.MajorLithCode == 'BNTN')] = 'bentonite'
    DF['OWN'][DF.MajorLithCode == 'IRNS'] = 'sand'
    DF['OWN'][DF.MajorLithCode == 'WODY'] = 'sand'
    DF['OWN'][DF.MajorLithCode == 'IGRK'] = 'igneous'
    DF['OWN'][DF.MajorLithCode == 'RHLT'] = 'rhyolite'
    DF['OWN'][DF.MajorLithCode == 'DLRT'] = 'dolerite'
    DF['OWN'][DF.MajorLithCode == 'SLND'] = 'silty sand'
    DF['OWN'][(DF.MajorLithCode == '8')] = 'limestone'
    DF['OWN'][DF.MajorLithCode == 'TUFF'] = 'tuff'
    DF['OWN'][DF.MajorLithCode == 'BLML'] = 'blue metal'
    DF['OWN'][DF.MajorLithCode == 'SRPN'] = 'serpentine'
    DF['OWN'][DF.MajorLithCode == 'DORT'] = 'diorite'
    DF['OWN'][DF.MajorLithCode == 'SRFC'] = 'soil'
    DF['OWN'][(DF.MajorLithCode == 'SOIL')] = 'soil'
    DF['OWN'][(DF.Description.str.contains('None')) &
              (DF.MajorLithCode == 'SOIL')] = np.nan
    DF['OWN'][(DF.MajorLithCode == 'TPSL')] = 'topsoil'
    DF['OWN'][((DF.Description.str.contains(' soil')) |
               (DF.Description.str.contains('Soil'))) &
              (DF.MajorLithCode == 'TPSL')] = 'soil'
    DF['OWN'][(DF.Description.str.contains('None')) &
              (DF.MajorLithCode == 'TPSL')] = np.nan
    DF['OWN'][DF.MajorLithCode == 'SBSL'] = 'subsoil'
    DF['OWN'][DF.MajorLithCode == 'VLCC'] = 'volcanic'
    DF['OWN'][DF.MajorLithCode == 'DRFT'] = 'drift'
    DF['OWN'][DF.MajorLithCode == 'CBSD'] = 'claystone'
    DF['OWN'][DF.MajorLithCode == 'SDRC'] = 'siderite'
    DF['OWN'][DF.MajorLithCode == 'CNSD'] = 'shale'
    DF['OWN'][DF.MajorLithCode == 'SASH'] = 'shale'
    DF['OWN'][DF.MajorLithCode == 'CHLK'] = 'chalk'
    DF['OWN'][DF.MajorLithCode == 'JSPR'] = 'jasper'
    DF['OWN'][DF.MajorLithCode == '15'] = 'quartz'
    DF['OWN'][DF.MajorLithCode == 'IGVL'] = 'ironstone'
    DF['OWN'][DF.MajorLithCode == 'LTRT'] = 'laterite'
    DF['OWN'][DF.MajorLithCode == 'FMSR'] = 'sandstone'
    DF['OWN'][DF.MajorLithCode == 'NORT'] = 'sandstone'
    DF['OWN'][DF.MajorLithCode == 'PRUS'] = 'sandstone'
    DF['OWN'][DF.MajorLithCode == 'RDDS'] = 'sandstone'
    DF['OWN'][DF.MajorLithCode == 'SLSN'] = 'siltstone'
    DF['OWN'][DF.MajorLithCode == 'CLRD'] = 'clay'
    DF['OWN'][DF.MajorLithCode == 'SOLD'] = 'clay'
    DF['OWN'][DF.MajorLithCode == 'TUGH'] = 'clay'
    DF['OWN'][DF.MajorLithCode == 'STNY'] = 'stones clay'
    DF['OWN'][DF.MajorLithCode == 'PUG'] = 'pug'
    DF['OWN'][DF.MajorLithCode == 'YWBN'] = 'clay'
    DF['OWN'][DF.MajorLithCode == '22'] = 'clay'
    DF['OWN'][DF.MajorLithCode == 'STCK'] = 'clay'
    DF['OWN'][DF.MajorLithCode == 'TNLR'] = 'clay'
    DF['OWN'][DF.MajorLithCode == 'DBLU'] = 'clay'
    DF['OWN'][DF.MajorLithCode == 'CLLM'] = 'clay loam'
    DF['OWN'][DF.MajorLithCode == 'SPBK'] = 'limestone'
    DF['OWN'][DF.MajorLithCode == 'SPSN'] = 'soapstone'
    DF['OWN'][DF.MajorLithCode == 'LGNT'] = 'lignite'
    DF['OWN'][DF.MajorLithCode == 'BNDS'] = 'sand'
    DF['OWN'][DF.MajorLithCode == 'VSND'] = 'sand'
    DF['OWN'][DF.MajorLithCode == 'MMCR'] = 'gravel'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'MMCR')] = 'sand gravel'
    DF['OWN'][DF.MajorLithCode == 'FNCR'] = 'gravel'
    DF['OWN'][DF.MajorLithCode == 'RBBL'] = 'gravel'
    DF['OWN'][DF.MajorLithCode == 'TGHT'] = 'gravel'
    DF['OWN'][DF.MajorLithCode == 'DRTY'] = 'gravel'
    DF['OWN'][DF.MajorLithCode == 'SOPY'] = 'gravel'
    DF['OWN'][DF.MajorLithCode == 'RSTY'] = 'gravel'
    DF['OWN'][DF.MajorLithCode == 'PEA'] = 'gravel'
    DF['OWN'][DF.MajorLithCode == 'LAVA'] = 'lava'
    DF['OWN'][DF.MajorLithCode == 'CLEN'] = 'sandy clay'
    DF['OWN'][DF.MajorLithCode == 'MOST'] = 'sandy clay'
    DF['OWN'][DF.MajorLithCode == 'LBLU'] = 'sandy clay'
    DF['OWN'][DF.MajorLithCode == 'GRTT'] = 'gritty clay'
    DF['OWN'][DF.MajorLithCode == 'SEMS'] = 'sandy clay'
    DF['OWN'][DF.MajorLithCode == 'MARL'] = 'marl'
    DF['OWN'][DF.MajorLithCode == 'FLVL'] = 'volcanic'
    DF['OWN'][DF.MajorLithCode == 'FLSC'] = 'volcanic'
    DF['OWN'][DF.MajorLithCode == 'GRSN'] = np.nan
    DF['OWN'][DF.MajorLithCode == 'FPPP'] = 'porphyry'
    DF['OWN'][DF.MajorLithCode == 'CGLD'] = 'conglomerate'
    DF['OWN'][DF.MajorLithCode == 'RFLT'] = 'conglomerate'
    DF['OWN'][DF.MajorLithCode == 'CGLC'] = 'conglomerate'
    DF['OWN'][DF.MajorLithCode == 'SEMI'] = 'conglomerate'
    DF['OWN'][(DF.MajorLithCode == 'CGLM')] = 'conglomerate'
    DF['OWN'][DF.MajorLithCode == 'SWRX'] = 'granite'
    DF['OWN'][DF.MajorLithCode == 'GRCK'] = 'greywacke'
    DF['OWN'][DF.MajorLithCode == 'GRIT'] = 'sand'
    DF['OWN'][DF.MajorLithCode == 'FRMN'] = 'basalt'
    DF['OWN'][DF.MajorLithCode == 'RSTN'] = 'basalt'
    DF['OWN'][DF.MajorLithCode == 'BSLC'] = 'sand gravel'
    DF['OWN'][DF.MajorLithCode == 'LIME'] = 'clay'
    DF['OWN'][DF.MajorLithCode == 'PRPR'] = 'porphyry'
    DF['OWN'][DF.MajorLithCode == 'GBBR'] = 'conglomerate'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'GBBR')] = 'sand gravel'
    DF['OWN'][(DF.MajorLithCode == 'DENS')] = 'sand gravel'
    DF['OWN'][DF.MajorLithCode == 'BRCC'] = 'breccia'
    DF['OWN'][DF.MajorLithCode == 'MICA'] = 'mica'
    DF['OWN'][DF.MajorLithCode == 'BCVC'] = 'volcanic'
    DF['OWN'][DF.MajorLithCode == 'SLRR'] = 'sand'
    DF['OWN'][DF.MajorLithCode == 'ASHV'] = 'volcanic'
    DF['OWN'][DF.MajorLithCode == 'CVTY'] = 'cavity'
    DF['OWN'][DF.MajorLithCode == 'CLGR'] = 'clay sand gravel'
    DF['OWN'][DF.MajorLithCode == 'GRDL'] = 'clay gravel'
    DF['OWN'][DF.MajorLithCode == 'PHLT'] = 'phyllite'
    DF['OWN'][DF.MajorLithCode == 'SDLM'] = 'sandy loam'
    DF['OWN'][DF.MajorLithCode == 'SLBD'] = 'sandy loam'
    DF['OWN'][DF.MajorLithCode == 'CLCR'] = 'calcrete'
    DF['OWN'][DF.MajorLithCode == 'GRLT'] = 'gravel'
    DF['OWN'][DF.MajorLithCode == 'QZPP'] = 'porphyry'
    DF['OWN'][((DF.Description.str.contains('sandstone')) |
               (DF.Description.str.contains('bands'))) &
              (DF.MajorLithCode == 'QZPP')] = 'sandstone'
    DF['OWN'][DF.MajorLithCode == 'HWRX'] = 'conglomerate'
    DF['OWN'][DF.MajorLithCode == 'ARKS'] = 'arkose'
    DF['OWN'][DF.MajorLithCode == 'SCST'] = 'schist'
    DF['OWN'][DF.MajorLithCode == 'VCRK'] = 'volcanic'
    DF['OWN'][DF.MajorLithCode == 'FSND'] = 'sandy clay'
    DF['OWN'][DF.MajorLithCode == 'ANDS'] = 'andesite'
    DF['OWN'][DF.MajorLithCode == 'SLCR'] = 'silcrete'
    DF['OWN'][(DF.Description.str.contains('Silstone')) &
              (DF.MajorLithCode == 'SLCR')] = 'siltstone'
    DF['OWN'][(~DF.Description.str.contains('Silstone')) &
              (~DF.Description.str.contains('Silcrete')) &
              (DF.MajorLithCode == 'SLCR')] = 'silty clay'
    DF['OWN'][DF.MajorLithCode == 'FLDP'] = 'feldspar'
    DF['OWN'][DF.MajorLithCode == 'CLCT'] = 'calcite'
    DF['OWN'][(DF.Description.str.contains('basalt')) &
              (DF.MajorLithCode == 'FLOT')] = 'basalt'
    DF['OWN'][(~DF.Description.str.contains('basalt')) &
              (DF.MajorLithCode == 'FLOT')] = 'water'
    DF['OWN'][(DF.Description.str.contains('Acid')) &
              (DF.MajorLithCode == 'ACVC')] = 'volcanic'
    DF['OWN'][DF.MajorLithCode == 'SGCY'] = 'sand gravel'
    DF['OWN'][(DF.Description.str.contains('granite')) &
              (DF.MajorLithCode == 'SGCY')] = 'granite'
    DF['OWN'][DF.MajorLithCode == 'ALRD'] = 'clay'
    DF['OWN'][DF.MajorLithCode == 'ALWD'] = 'wood'
    DF['OWN'][DF.MajorLithCode == 'PFWD'] = 'wood'
    DF['OWN'][DF.MajorLithCode == 'SSLS'] = 'siltstone'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'SSLS')] = 'sandy clay'
    DF['OWN'][DF.MajorLithCode == 'LBIL'] = 'shale'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'LBIL')] = 'clay'
    DF['OWN'][DF.MajorLithCode == 'CRKD'] = 'slate'
    DF['OWN'][DF.MajorLithCode == 'SHFT'] = 'shale'
    DF['OWN'][DF.MajorLithCode == 'CNZC'] = 'clay sand'
    DF['OWN'][(DF.Description.str.contains('coal')) &
              (DF.MajorLithCode == 'CNZC')] = 'coal'
    DF['OWN'][(DF.Description.str.contains('sandstone')) &
              (DF.MajorLithCode == 'BCPD')] = 'sandstone'
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == 'BCPD')] = 'shale'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'WTST')] = 'clay'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'WTST')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('sandstone')) &
              (DF.MajorLithCode == 'WTST')] = 'sandstone'
    DF['OWN'][DF.MajorLithCode == 'GNBN'] = 'granite'
    DF['OWN'][DF.MajorLithCode == 'RED'] = 'soil'
    DF['OWN'][DF.MajorLithCode == 'RODN'] = 'soil'
    DF['OWN'][DF.MajorLithCode == 'TRCN'] = 'soil'
    DF['OWN'][DF.MajorLithCode == 'SBGL'] = 'soil'
    DF['OWN'][DF.MajorLithCode == 'BLCK'] = 'soil'
    DF['OWN'][DF.MajorLithCode == 'LGRY'] = 'clay'
    DF['OWN'][DF.MajorLithCode == 'VSLT'] = 'silty clay'
    DF['OWN'][(DF.MajorLithCode == 'SLCY')] = 'silty clay'
    DF['OWN'][(DF.Description.str.contains('silty clay')) &
              (DF.MajorLithCode == 'RDST')] = 'silty clay'
    DF['OWN'][(DF.Description.str.contains('sandy clay')) &
              (DF.MajorLithCode == 'RDST')] = 'sandy clay'
    DF['OWN'][(DF.Description.str.contains('sandstone')) &
              (DF.MajorLithCode == 'RDST')] = 'sandstone'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'BRWN')] = 'clay'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'BRWN')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('sandy clay')) &
              (DF.MajorLithCode == 'BRWN')] = 'sandy clay'
    DF['OWN'][(DF.Description == 'Brown') &
              (DF.MajorLithCode == 'BRWN')] = np.nan
    DF['OWN'][DF.MajorLithCode == 'DRED'] = 'sandy clay'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'VFIN')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'VFIN')] = 'clay gravel'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'DBRN')] = 'clay'
    DF['OWN'][(DF.Description.str.contains('soil')) &
              (DF.MajorLithCode == 'DBRN')] = 'soil'
    DF['OWN'][(DF.Description.str.contains('sandy clay')) &
              (DF.MajorLithCode == 'DBRN')] = 'sandy clay'
    DF['OWN'][(DF.Description.str.contains('sandy loam')) &
              (DF.MajorLithCode == 'DBRN')] = 'sandy loam'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'DBRN')] = 'gravel'
    DF['OWN'][(DF.Description.str.contains('sand and gravel')) &
              (DF.MajorLithCode == 'DBRN')] = 'sand gravel'
    DF['OWN'][DF.MajorLithCode == 'DGRY'] = 'clay'
    DF['OWN'][DF.MajorLithCode == 'BLUE'] = 'sand'
    DF['OWN'][(DF.Description.str.contains('soil')) &
              (DF.MajorLithCode == 'LOMY')] = 'soil'
    DF['OWN'][(~DF.Description.str.contains('soil')) &
              (DF.MajorLithCode == 'LOMY')] = 'clay loam'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'DRY')] = 'gravel'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'DRY')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('gravel and clay')) &
              (DF.MajorLithCode == 'DRY')] = 'clay gravel'
    DF['OWN'][DF.MajorLithCode == 'WET'] = 'gravel'
    DF['OWN'][DF.MajorLithCode == 'BCKS'] = 'basalt'
    DF['OWN'][DF.MajorLithCode == 'LOOS'] = 'boulders'
    DF['OWN'][DF.MajorLithCode == 'RIVR'] = 'gravel'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'WHBN')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('silt')) &
              (DF.MajorLithCode == 'WHBN')] = 'silty'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'WHBN')] = 'clay'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'LGHT')] = 'clay'
    DF['OWN'][(~DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'LGHT')] = np.nan
    DF['OWN'][(DF.Description.str.contains('siltstone')) &
              (DF.MajorLithCode == 'KHKI')] = 'siltstone'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'KHKI')] = 'clay'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'LRGE')] = 'gravel'
    DF['OWN'][(DF.Description.str.contains('stone')) &
              (DF.MajorLithCode == 'LRGE')] = 'stones'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'SMLL')] = 'gravel'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'SMLL')] = 'clay gravel'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'SMLL')] = 'sand gravel'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'CMPC')] = 'gravel'
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == 'CMPC')] = 'shale'
    DF['OWN'][(DF.Description == 'Compacted') &
              (DF.MajorLithCode == 'CMPC')] = np.nan
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'PRPL')] = 'clay'
    DF['OWN'][(~DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'PRPL')] = np.nan
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'HARD')] = 'clay'
    DF['OWN'][(~DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'HARD')] = np.nan
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'SCLY')] = 'clay gravel'
    DF['OWN'][(~DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'SCLY')] = 'gritty clay'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'CMND')] = 'gravel'
    DF['OWN'][(~DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'CMND')] = np.nan
    DF['OWN'][(DF.Description.str.contains('Wood')) &
              (DF.MajorLithCode == 'WOOD')] = 'wood'
    DF['OWN'][(~DF.Description.str.contains('Wood')) &
              (DF.MajorLithCode == 'WOOD')] = 'clay'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'WOOD')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('Sand')) &
              (DF.MajorLithCode == 'SCBN')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'SCBN')] = 'sand gravel'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'SCBN')] = 'clay sand'
    DF['OWN'][(DF.Description.str.contains('sandstone')) &
              (DF.MajorLithCode == 'SSDS')] = 'sandstone'
    DF['OWN'][(~DF.Description.str.contains('sandstone')) &
              (DF.MajorLithCode == 'SSDS')] = 'conglomerate'
    DF['OWN'][(DF.MajorLithCode == 'ERTH')] = 'earth'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'ERTH')] = 'gravel'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'ERTH')] = 'clay'
    DF['OWN'][(DF.Description.str.contains('boulder')) &
              (DF.MajorLithCode == 'ERTH')] = 'boulders'
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == 'ERTH')] = 'shale'
    DF['OWN'][(DF.Description.str.contains('loam')) &
              (DF.MajorLithCode == 'ERTH')] = 'loam'
    DF['OWN'][(DF.MajorLithCode == 'SLTY')] = 'silty'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'SLTY')] = 'silty sand'
    DF['OWN'][((DF.Description.str.contains('Silty/clay')) |
               (DF.Description.str.contains('Silty clay'))) &
              (DF.MajorLithCode == 'SLTY')] = 'silty sand'
    DF['OWN'][(DF.Description.str.contains('loam')) &
              (DF.MajorLithCode == 'SLTY')] = 'silty loam'
    DF['OWN'][(DF.MajorLithCode == 'SDLC')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'SDLC')] = 'sand gravel'
    DF['OWN'][(DF.Description.str.contains('Sand clay')) &
              (DF.MajorLithCode == 'SDLC')] = 'clay sand'
    DF['OWN'][(DF.MajorLithCode == 'CLYY')] = 'clay'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'CLYY')] = 'clay gravel'
    DF['OWN'][((DF.Description.str.contains('sand')) &
               (~DF.Description.str.contains('gravel'))) &
              (DF.MajorLithCode == 'CLYY')] = 'clay sand'
    DF['OWN'][(DF.MajorLithCode == 'FRCD')] = np.nan
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == 'FRCD')] = 'shale'
    DF['OWN'][(DF.Description.str.contains('sandstone')) &
              (DF.MajorLithCode == 'FRCD')] = 'sandstone'
    DF['OWN'][(DF.Description.str.contains('basalt')) &
              (DF.MajorLithCode == 'FRCD')] = 'basalt'
    DF['OWN'][(DF.Description.str.contains('granite')) &
              (DF.MajorLithCode == 'FRCD')] = 'granite'
    DF['OWN'][(DF.MajorLithCode == 'WRCK')] = np.nan
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == 'WRCK')] = 'shale'
    DF['OWN'][(DF.Description.str.contains('sandstone')) &
              (DF.MajorLithCode == 'WRCK')] = 'sandstone'
    DF['OWN'][(DF.Description.str.contains('volcanic')) &
              (DF.MajorLithCode == 'WRCK')] = 'volcanic'
    DF['OWN'][(DF.Description.str.contains('granite')) &
              (DF.MajorLithCode == 'WRCK')] = 'granite'
    DF['OWN'][(DF.MajorLithCode == 'MLCD')] = np.nan
    DF['OWN'][((DF.Description.str.contains('clay')) |
               (DF.Description.str.contains('Clay'))) &
              (DF.MajorLithCode == 'MLCD')] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'GRBN')] = 'clay'
    DF['OWN'][(DF.Description.str.contains('basalt')) &
              (DF.MajorLithCode == 'GRBN')] = 'basalt'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'GRBN')] = 'clay sand'
    DF['OWN'][(DF.MajorLithCode == 'ORNG')] = 'clay'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'ORNG')] = 'gravel'
    DF['OWN'][(DF.Description.str.contains('silty clay')) &
              (DF.MajorLithCode == 'ORNG')] = 'silty clay'
    DF['OWN'][(DF.Description.str.contains('silt')) &
              (DF.MajorLithCode == 'ORNG')] = 'silty'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'ORNG')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('sandy clay')) &
              (DF.MajorLithCode == 'ORNG')] = 'sandy clay'
    DF['OWN'][(DF.MajorLithCode == 'FINE')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'FINE')] = 'gravel'
    DF['OWN'][(DF.Description.str.contains('sandstone')) &
              (DF.MajorLithCode == 'FINE')] = 'sandstone'
    DF['OWN'][((DF.Description.str.contains('gravel')) &
               (DF.Description.str.contains('sand'))) &
              (DF.MajorLithCode == 'FINE')] = 'sand gravel'
    DF['OWN'][((DF.Description.str.contains('gravel')) &
               (DF.Description.str.contains('clay'))) &
              (DF.MajorLithCode == 'FINE')] = 'clay gravel'
    DF['OWN'][(DF.MajorLithCode == 'LBRN')] = 'clay'
    DF['OWN'][(DF.Description.str.contains('soil')) &
              (DF.MajorLithCode == 'LBRN')] = 'soil'
    DF['OWN'][((DF.Description.str.contains('gravel')) &
               (DF.Description.str.contains('sand'))) &
              (DF.MajorLithCode == 'LBRN')] = 'sand gravel'
    DF['OWN'][((DF.Description.str.contains('sand')) &
               (DF.Description.str.contains('clay'))) &
              (DF.MajorLithCode == 'LBRN')] = 'sandy clay'
    DF['OWN'][((DF.Description.str.contains('silt')) &
               (DF.Description.str.contains('clay'))) &
              (DF.MajorLithCode == 'LBRN')] = 'silty clay'
    DF['OWN'][(DF.MajorLithCode == 'MDUM')] = 'gravel'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'MDUM')] = 'clay'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'MDUM')] = 'sand'
    DF['OWN'][((DF.Description.str.contains('gravel')) &
               (DF.Description.str.contains('sand'))) &
              (DF.MajorLithCode == 'MDUM')] = 'sand gravel'
    DF['OWN'][(DF.MajorLithCode == 'CRSE')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'CRSE')] = 'gravel'
    DF['OWN'][((DF.Description.str.contains('gravel')) &
               (DF.Description.str.contains('sand'))) &
              (DF.MajorLithCode == 'CRSE')] = 'sand gravel'
    DF['OWN'][((DF.Description.str.contains('gravel')) &
               (DF.Description.str.contains('clay'))) &
              (DF.MajorLithCode == 'CRSE')] = 'clay gravel'
    DF['OWN'][(DF.MajorLithCode == 'BRKN')] = np.nan
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == 'BRKN')] = 'shale'
    DF['OWN'][(DF.Description.str.contains('sandstone')) &
              (DF.MajorLithCode == 'BRKN')] = 'sandstone'
    DF['OWN'][(DF.Description.str.contains('basalt')) &
              (DF.MajorLithCode == 'BRKN')] = 'basalt'
    DF['OWN'][(DF.Description.str.contains('granite')) &
              (DF.MajorLithCode == 'BRKN')] = 'granite'
    DF['OWN'][(DF.Description.str.contains('mudstone')) &
              (DF.MajorLithCode == 'BRKN')] = 'mudstone'
    DF['OWN'][(DF.MajorLithCode == 'HDBD')] = np.nan
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == 'HDBD')] = 'shale'
    DF['OWN'][(DF.Description.str.contains('conglomerate')) &
              (DF.MajorLithCode == 'HDBD')] = 'conglomerate'
    DF['OWN'][(DF.Description.str.contains('basalt')) &
              (DF.MajorLithCode == 'HDBD')] = 'basalt'
    DF['OWN'][(DF.Description.str.contains('granite')) &
              (DF.MajorLithCode == 'HDBD')] = 'granite'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'HDBD')] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'SFBD')] = np.nan
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == 'SFBD')] = 'shale'
    DF['OWN'][(DF.Description.str.contains('basalt')) &
              (DF.MajorLithCode == 'SFBD')] = 'basalt'
    DF['OWN'][(DF.Description.str.contains('granite')) &
              (DF.MajorLithCode == 'SFBD')] = 'granite'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'SFBD')] = 'clay'
    DF['OWN'][((DF.Description.str.contains('clay')) &
               (DF.Description.str.contains('sand'))) &
              (DF.MajorLithCode == 'SFBD')] = 'sandy clay'
    DF['OWN'][(DF.MajorLithCode == 'YWST')] = 'shale'
    DF['OWN'][(DF.Description.str.contains('sandstone')) &
              (DF.MajorLithCode == 'YWST')] = 'sandstone'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'YWST')] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'WDDY')] = np.nan
    DF['OWN'][(DF.Description.str.contains('sandstone')) &
              (DF.MajorLithCode == 'WDDY')] = 'sandstone'
    DF['OWN'][(DF.Description.str.contains('basalt')) &
              (DF.MajorLithCode == 'WDDY')] = 'basalt'
    DF['OWN'][(DF.Description.str.contains('granite')) &
              (DF.MajorLithCode == 'WDDY')] = 'granite'
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == 'WDDY')] = 'shale'
    DF['OWN'][(DF.MajorLithCode == 'BLBN')] = np.nan
    DF['OWN'][(DF.Description.str.contains('basalt')) &
              (DF.MajorLithCode == 'BLBN')] = 'basalt'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'BLBN')] = 'clay'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'BLBN')] = 'gravel'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'BLBN')] = 'sand'
    DF['OWN'][((DF.Description.str.contains('gravel')) &
               (DF.Description.str.contains('sand'))) &
              (DF.MajorLithCode == 'BLBN')] = 'sand gravel'
    DF['OWN'][((DF.Description.str.contains('silt')) &
               (DF.Description.str.contains('sand'))) &
              (DF.MajorLithCode == 'BLBN')] = 'silty sand'
    DF['OWN'][(DF.MajorLithCode == 'WTCB')] = 'clay'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'WTCB')] = 'clay gravel'
    DF['OWN'][((DF.Description.str.contains('gravel')) |
               (DF.Description.str.contains('sand'))) &
              (DF.MajorLithCode == 'WTCB')] = 'clay sand gravel'
    DF['OWN'][(DF.MajorLithCode == 'GYST')] = np.nan
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'GYST')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('sandstone')) &
              (DF.MajorLithCode == 'GYST')] = 'sandstone'
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == 'GYST')] = 'shale'
    DF['OWN'][(DF.Description.str.contains('siltstone')) &
              (DF.MajorLithCode == 'GYST')] = 'siltstone'
    DF['OWN'][((DF.Description.str.contains('gravel')) &
               (DF.Description.str.contains('sand'))) &
              (DF.MajorLithCode == 'GYST')] = 'sand gravel'
    DF['OWN'][((DF.Description.str.contains('clay')) &
               (DF.Description.str.contains('sand'))) &
              (DF.MajorLithCode == 'GYST')] = 'sandy clay'
    DF['OWN'][(DF.Description.str.contains('soil')) &
              (DF.MajorLithCode == 'GYST')] = 'topsoil'
    DF['OWN'][(DF.MajorLithCode == 'BKBN')] = 'clay'
    DF['OWN'][(DF.Description.str.contains('soil')) &
              (DF.MajorLithCode == 'BKBN')] = 'soil'
    DF['OWN'][(DF.Description.str.contains('topsoil')) &
              (DF.MajorLithCode == 'BKBN')] = 'topsoil'
    DF['OWN'][(DF.Description.str.contains('basalt')) &
              (DF.MajorLithCode == 'BKBN')] = 'basalt'
    DF['OWN'][(DF.Description.str.contains('volcanic')) &
              (DF.MajorLithCode == 'BKBN')] = 'volcanic'
    DF['OWN'][(DF.Description.str.contains('granite')) &
              (DF.MajorLithCode == 'BKBN')] = 'granite'
    DF['OWN'][(DF.Description.str.contains('rock')) &
              (DF.MajorLithCode == 'BKBN')] = np.nan
    DF['OWN'][((DF.Description.str.contains('clay')) &
               (DF.Description.str.contains('silt'))) &
              (DF.MajorLithCode == 'BKBN')] = 'silty clay'
    DF['OWN'][(DF.MajorLithCode == 'BKST')] = 'slate'
    DF['OWN'][((DF.Description.str.contains('soil')) &
               (DF.Description.str.contains('Soil'))) &
              (DF.MajorLithCode == 'BKST')] = 'soil'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'BKST')] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'DCMP')] = np.nan
    DF['OWN'][(DF.Description.str.contains('basalt')) &
              (DF.MajorLithCode == 'DCMP')] = 'basalt'
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == 'DCMP')] = 'shale'
    DF['OWN'][(DF.Description.str.contains('granite')) &
              (DF.MajorLithCode == 'DCMP')] = 'granite'
    DF['OWN'][(DF.MajorLithCode == 'BLST')] = np.nan
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'BLST')] = 'sand gravel'
    DF['OWN'][(DF.Description.str.contains('sandstone')) &
              (DF.MajorLithCode == 'BLST')] = 'sandstone'
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == 'BLST')] = 'shale'
    DF['OWN'][(DF.MajorLithCode == 'WTRD')] = np.nan
    DF['OWN'][(DF.Description.str.contains('sandstone')) &
              (DF.MajorLithCode == 'WTRD')] = 'sandstone'
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == 'WTRD')] = 'shale'
    DF['OWN'][(DF.Description.str.contains('basalt')) &
              (DF.MajorLithCode == 'WTRD')] = 'basalt'
    DF['OWN'][(DF.MajorLithCode == '21')] = 'sandy clay'
    DF['OWN'][((DF.Description.str.contains('gravel')) &
               (~DF.Description.str.contains('clay'))) &
              (DF.MajorLithCode == '21')] = 'sand gravel'
    DF['OWN'][(DF.Description.str.contains('loam')) &
              (DF.MajorLithCode == '21')] = 'sandy loam'
    DF['OWN'][(DF.Description.str.contains('Loam')) &
              (DF.MajorLithCode == '21')] = 'loam'
    DF['OWN'][(DF.MajorLithCode == 'SCLM')] = 'sandy clay loam'
    DF['OWN'][((DF.Description.str.contains('Clay sandy')) |
               (~DF.Description.str.contains('loam'))) &
              (DF.MajorLithCode == 'SCLM')] = 'clay sand'
    DF['OWN'][(DF.MajorLithCode == 'CHRT')] = 'chert'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'CHRT')] = 'stones clay'
    DF['OWN'][(DF.Description.str.contains('Clay')) &
              (DF.MajorLithCode == 'CHRT')] = 'clay sand'
    DF['OWN'][(DF.Description.str.contains('None')) &
              (DF.MajorLithCode == 'CHRT')] = np.nan
    DF['OWN'][(DF.MajorLithCode == 'SNDY')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('soil')) &
              (DF.MajorLithCode == 'SNDY')] = 'soil'
    DF['OWN'][(DF.Description.str.contains('topsoil')) &
              (DF.MajorLithCode == 'SNDY')] = 'topsoil'
    DF['OWN'][(DF.Description.str.contains('loam')) &
              (DF.MajorLithCode == 'SNDY')] = 'sandy loam'
    DF['OWN'][(DF.Description.str.contains('Clay')) &
              (DF.MajorLithCode == 'SNDY')] = 'sandy clay'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'SNDY')] = 'sandy clay'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'SNDY')] = 'sand gravel'
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == 'SNDY')] = 'shale'
    DF['OWN'][(DF.MajorLithCode == 'FILL')] = np.nan
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'FILL')] = 'gravel'
    DF['OWN'][((DF.Description.str.contains('gravelly sand')) |
               (DF.Description.str.contains('sandy gravel')) |
               DF.Description.str.contains('silt')) &
              (DF.MajorLithCode == 'FILL')] = 'sand gravel'
    DF['OWN'][((DF.Description.str.contains('ground')) |
               (DF.Description.str.contains('soil'))) &
              (DF.MajorLithCode == 'FILL')] = 'soil'
    DF['OWN'][(DF.Description.str.contains('topsoil')) &
              (DF.MajorLithCode == 'FILL')] = 'topsoil'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'FILL')] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'MUD')] = 'mud'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'MUD')] = 'mud gravel'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'MUD')] = 'mud sand'
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == 'MUD')] = 'shale'
    DF['OWN'][(DF.MajorLithCode == 'STON')] = 'stones'
    DF['OWN'][((DF.Description.str.contains('clay')) |
               (DF.Description.str.contains('Clay'))) &
              (DF.MajorLithCode == 'STON')] = 'stones clay'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'STON')] = 'stones gravel'
    DF['OWN'][(DF.MajorLithCode == 'WB')] = 'water'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'WB')] = 'gravel'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'WB')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'WB')] = 'clay'
    DF['OWN'][((DF.Description.str.contains('gravel')) &
               (DF.Description.str.contains('sand'))) &
              (DF.MajorLithCode == 'WB')] = 'sand gravel'
    DF['OWN'][(DF.Description.str.contains('basalt')) &
              (DF.MajorLithCode == 'WB')] = 'basalt'
    DF['OWN'][(DF.Description.str.contains('sandstone')) &
              (DF.MajorLithCode == 'WB')] = 'sandstone'
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == 'WB')] = 'shale'
    DF['OWN'][(DF.Description.str.contains('granite')) &
              (DF.MajorLithCode == 'WB')] = 'granite'
    DF['OWN'][(DF.Description.str.contains('rock')) &
              (DF.MajorLithCode == 'WB')] = np.nan
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'WB')] = 'clay gravel'
    DF['OWN'][(DF.MajorLithCode == 'BRBN')] = 'clay'
    DF['OWN'][(DF.Description.str.contains('soil')) &
              (DF.MajorLithCode == 'BRBN')] = 'soil'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'BRBN')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'BRBN')] = 'gravel'
    DF['OWN'][((DF.Description.str.contains('gravel')) &
               (DF.Description.str.contains('sand'))) &
              (DF.MajorLithCode == 'BRBN')] = 'sand gravel'
    DF['OWN'][((DF.Description.str.contains('clay')) &
               (DF.Description.str.contains('sand'))) &
              (DF.MajorLithCode == 'BRBN')] = 'sandy clay'
    DF['OWN'][(DF.Description.str.contains('basalt')) &
              (DF.MajorLithCode == 'BRBN')] = 'basalt'
    DF['OWN'][(DF.Description.str.contains('sandstone')) &
              (DF.MajorLithCode == 'BRBN')] = 'sandstone'
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == 'BRBN')] = 'shale'
    DF['OWN'][(DF.Description.str.contains('rock')) &
              (DF.MajorLithCode == 'BRBN')] = np.nan
    DF['OWN'][(DF.MajorLithCode == '99')] = 'clay'
    DF['OWN'][((DF.Description.str.contains('None')) |
               (DF.Description.str.contains('unknown')) |
               (DF.Description == '(')) &
              (DF.MajorLithCode == '99')] = np.nan
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == '99')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == '99')] = 'gravel'
    DF['OWN'][((DF.Description.str.contains('gravel')) &
               (DF.Description.str.contains('sand'))) &
              (DF.MajorLithCode == '99')] = 'sand gravel'
    DF['OWN'][((DF.Description.str.contains('gravel')) &
               (DF.Description.str.contains('clay'))) &
              (DF.MajorLithCode == '99')] = 'clay gravel'
    DF['OWN'][((DF.Description.str.contains('clay')) &
               (DF.Description.str.contains('sand'))) &
              (DF.MajorLithCode == '99')] = 'sandy clay'
    DF['OWN'][(DF.Description.str.contains('channel')) &
              (DF.MajorLithCode == '99')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('sandstone')) &
              (DF.MajorLithCode == '99')] = 'sandstone'
    DF['OWN'][(DF.Description.str.contains('soil')) &
              (DF.MajorLithCode == '99')] = 'soil'
    DF['OWN'][(DF.Description.str.contains('opsoil')) &
              (DF.MajorLithCode == '99')] = 'topsoil'
    DF['OWN'][(DF.MajorLithCode == 'BNST')] = 'shale'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'BNST')] = 'clay'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'BNST')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'BNST')] = 'gravel'
    DF['OWN'][(DF.Description.str.contains('s&g')) &
              (DF.MajorLithCode == 'BNST')] = 'sand gravel'
    DF['OWN'][((DF.Description.str.contains('gravel')) &
               (DF.Description.str.contains('sand'))) &
              (DF.MajorLithCode == 'BNST')] = 'sand gravel'
    DF['OWN'][((DF.Description.str.contains('gravel')) &
               (DF.Description.str.contains('clay'))) &
              (DF.MajorLithCode == 'BNST')] = 'clay gravel'
    DF['OWN'][((DF.Description.str.contains('clay')) &
               (DF.Description.str.contains('sand'))) &
              (DF.MajorLithCode == 'BNST')] = 'sandy clay'
    DF['OWN'][(DF.Description.str.contains('sandstone')) &
              (DF.MajorLithCode == 'BNST')] = 'sandstone'
    DF['OWN'][(DF.MajorLithCode == 'GRCL')] = 'gravel'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'GRCL')] = 'clay gravel'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'GRCL')] = 'sand gravel'
    DF['OWN'][((DF.Description.str.contains('clay')) &
               (DF.Description.str.contains('sand'))) &
              (DF.MajorLithCode == 'GRCL')] = 'clay sand gravel'
    DF['OWN'][(DF.MajorLithCode == '23')] = 'clay sand'
    DF['OWN'][(DF.Description.str.contains('sandy')) &
              (DF.MajorLithCode == '23')] = 'sandy clay'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == '23')] = 'clay sand gravel'
    DF['OWN'][(DF.MajorLithCode == '19')] = 'silty clay'
    DF['OWN'][(~DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == '19')] = 'silty sand'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == '19')] = 'silty clay sand'
    DF['OWN'][(DF.MajorLithCode == 'CLSD')] = 'clay sand'
    DF['OWN'][(DF.Description.str.contains('silt')) &
              (DF.MajorLithCode == 'CLSD')] = 'silty clay sand'
    DF['OWN'][(DF.MajorLithCode == 'CLSN')] = 'claystone'
    DF['OWN'][(~DF.Description.str.contains('claystone')) &
              (~DF.Description.str.contains('Claystone')) &
              (DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'CLSN')] = 'clay gravel'
    DF['OWN'][(~DF.Description.str.contains('claystone')) &
              (~DF.Description.str.contains('Claystone')) &
              (DF.Description.str.contains('stone')) &
              (DF.MajorLithCode == 'CLSN')] = 'stones clay'
    DF['OWN'][(DF.Description.str.contains('limestone')) &
              (DF.MajorLithCode == 'CLSN')] = 'clay'
    DF['OWN'][(DF.MajorLithCode == 'CLBD')] = 'clay gravel'
    DF['OWN'][(DF.Description.str.contains('boulder')) &
              (DF.MajorLithCode == 'CLBD')] = 'clay boulders'
    DF['OWN'][(DF.MajorLithCode == 'ALVM')] = 'alluvium'
    DF['OWN'][(DF.Description.str.contains('soil')) &
              (DF.MajorLithCode == 'ALVM')] = 'soil'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'ALVM')] = 'clay'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'ALVM')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'ALVM')] = 'gravel'
    DF['OWN'][(DF.Description.str.contains('basalt')) &
              (DF.MajorLithCode == 'ALVM')] = 'basalt'
    DF['OWN'][(DF.Description.str.contains('drift')) &
              (DF.MajorLithCode == 'ALVM')] = 'drift'
    DF['OWN'][(DF.Description.str.contains('conglomerate')) &
              (DF.MajorLithCode == 'ALVM')] = 'conglomerate'
    DF['OWN'][(DF.Description.str.contains('rock')) &
              (DF.MajorLithCode == 'ALVM')] = 'alluvium'
    DF['OWN'][((DF.Description.str.contains('sand')) &
               (DF.Description.str.contains('gravel'))) &
              (DF.MajorLithCode == 'ALVM')] = 'sand gravel'
    DF['OWN'][((DF.Description.str.contains('clay')) &
               (DF.Description.str.contains('gravel'))) &
              (DF.MajorLithCode == 'ALVM')] = 'clay gravel'
    DF['OWN'][((DF.Description.str.contains('clay')) &
               (DF.Description.str.contains('sand'))) &
              (DF.MajorLithCode == 'ALVM')] = 'clay sand'
    DF['OWN'][(DF.MajorLithCode == 'MDSN')] = 'mudstone'
    DF['OWN'][(DF.Description.str.contains('None')) &
              (DF.MajorLithCode == 'MDSN')] = np.nan
    DF['OWN'][(DF.MajorLithCode == 'BDRK')] = 'bedrock'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'BDRK')] = 'sandstone'
    DF['OWN'][(DF.Description.str.contains('granite')) &
              (DF.MajorLithCode == 'BDRK')] = 'granite'
    DF['OWN'][(DF.Description.str.contains('basalt')) &
              (DF.MajorLithCode == 'BDRK')] = 'basalt'
    DF['OWN'][(DF.Description.str.contains('volcanic')) &
              (DF.MajorLithCode == 'BDRK')] = 'volcanic'
    DF['OWN'][(DF.Description.str.contains('siltstone')) &
              (DF.MajorLithCode == 'BDRK')] = 'siltstone'
    DF['OWN'][(DF.Description.str.contains('mudstone')) &
              (DF.MajorLithCode == 'BDRK')] = 'mudstone'
    DF['OWN'][(DF.Description.str.contains('dolerite')) &
              (DF.MajorLithCode == 'BDRK')] = 'dolerite'
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == 'BDRK')] = 'shale'
    DF['OWN'][(DF.Description.str.contains('arkose')) &
              (DF.MajorLithCode == 'BDRK')] = 'arkose'
    DF['OWN'][(DF.Description.str.contains('porphyry')) &
              (DF.MajorLithCode == 'BDRK')] = 'porphyry'
    DF['OWN'][(DF.Description.str.contains('ignimbrite')) &
              (DF.MajorLithCode == 'BDRK')] = 'ignimbrite'
    DF['OWN'][((DF.Description.str.contains('Rhyolite')) |
               (DF.Description.str.contains('rhyolite'))) &
              (DF.MajorLithCode == 'BDRK')] = 'rhyolite'
    DF['OWN'][(DF.Description.str.contains('diorite')) &
              (DF.MajorLithCode == 'BDRK')] = 'diorite'
    DF['OWN'][(DF.MajorLithCode == '20')] = 'clay sand'
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == '20')] = 'shale'
    DF['OWN'][((DF.Description.str.contains('Sandy')) |
               (DF.Description.str.contains('sandy clay'))) &
              (DF.MajorLithCode == '20')] = 'sandy clay'
    DF['OWN'][((~DF.Description.str.contains('clay')) |
               (~DF.Description.str.contains('Clay'))) &
              (DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == '20')] = 'sand gravel'
    DF['OWN'][((~DF.Description.str.contains('clay')) |
               (~DF.Description.str.contains('Clay'))) &
              (DF.Description.str.contains('loam')) &
              (DF.MajorLithCode == '20')] = 'sandy loam'
    DF['OWN'][(DF.MajorLithCode == 'IRSN')] = 'ironstone'
    DF['OWN'][(DF.Description.str.contains('None')) &
              (DF.MajorLithCode == 'IRSN')] = np.nan
    DF['OWN'][(DF.MajorLithCode == 'SILT')] = 'silty'
    DF['OWN'][(DF.Description.str.contains('soil')) &
              (DF.MajorLithCode == 'SILT')] = 'soil'
    DF['OWN'][(DF.Description.str.contains('topsoil')) &
              (DF.MajorLithCode == 'SILT')] = 'topsoil'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'SILT')] = 'silty gravel'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'SILT')] = 'silty clay'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'SILT')] = 'sandy silt'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'SILT')] = 'silty clay sand'
    DF['OWN'][(DF.MajorLithCode == 'LOAM')] = 'loam'
    DF['OWN'][(DF.Description.str.contains('soil')) &
              (DF.MajorLithCode == 'LOAM')] = 'soil'
    DF['OWN'][(DF.Description.str.contains('topsoil')) &
              (DF.MajorLithCode == 'LOAM')] = 'topsoil'
    DF['OWN'][(DF.Description.str.contains('None')) &
              (DF.MajorLithCode == 'LOAM')] = np.nan
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'LOAM')] = 'silty gravel'
    DF['OWN'][((DF.Description.str.contains('silt')) |
               (DF.Description.str.contains('Silt'))) &
              (DF.MajorLithCode == 'LOAM')] = 'silty loam'
    DF['OWN'][((DF.Description.str.contains('clay')) |
               (DF.Description.str.contains('Clay')))
              & (DF.MajorLithCode == 'LOAM')] = 'clay loam'
    DF['OWN'][((DF.Description.str.contains('sand')) |
               (DF.Description.str.contains('Sand'))) &
              (DF.MajorLithCode == 'LOAM')] = 'sandy loam'
    DF['OWN'][(DF.MajorLithCode == 'LMSN')] = 'limestone'
    DF['OWN'][(DF.Description.str.contains('None')) &
              (DF.MajorLithCode == 'LMSN')] = np.nan
    DF['OWN'][(DF.MajorLithCode == 'SDCY')] = 'sandy clay'
    DF['OWN'][((DF.Description.str.contains('silt')) |
               (DF.Description.str.contains('Silt'))) &
              (DF.MajorLithCode == 'SDCY')] = 'silty sandy clay'
    DF['OWN'][((DF.Description.str.contains('gravel')) |
               (DF.Description.str.contains('Gravelly'))) &
              (DF.MajorLithCode == 'SDCY')] = 'clay sand gravel'
    DF['OWN'][(DF.MajorLithCode == 'GRNT')] = 'granite'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'GRNT')] = 'clay'
    DF['OWN'][(DF.Description.str.contains('soil')) &
              (DF.MajorLithCode == 'GRNT')] = 'soil'
    DF['OWN'][(DF.Description.str.contains('topsoil')) &
              (DF.MajorLithCode == 'GRNT')] = 'topsoil'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'GRNT')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'GRNT')] = 'gravel'
    DF['OWN'][((DF.Description.str.contains('boulder')) |
               (DF.Description.str.contains('Boulder'))) &
              (DF.MajorLithCode == 'GRNT')] = 'boulders'
    DF['OWN'][(DF.MajorLithCode == 'BSLT')] = 'basalt'
    DF['OWN'][(DF.Description == 'None') &
              (DF.MajorLithCode == 'BSLT')] = np.nan
    DF['OWN'][(DF.Description.str.contains('soil')) &
              (DF.MajorLithCode == 'BSLT')] = 'soil'
    DF['OWN'][(DF.Description.str.contains('topsoil')) &
              (DF.MajorLithCode == 'BSLT')] = 'topsoil'
    DF['OWN'][(DF.MajorLithCode == 'ROCK')] = np.nan
    DF['OWN'][((DF.Description == 'granit') |
               (DF.Description == 'Granit')) &
              (DF.MajorLithCode == 'ROCK')] = 'granite'
    DF['OWN'][(DF.Description.str.contains('basalt')) &
              (DF.MajorLithCode == 'ROCK')] = 'basalt'
    DF['OWN'][((DF.Description.str.contains('clay')) |
               (DF.Description.str.contains('Clay'))) &
              (DF.MajorLithCode == 'ROCK')] = 'clay'
    DF['OWN'][((DF.Description.str.contains('boulder')) |
               (DF.Description.str.contains('Boulder'))) &
              (DF.MajorLithCode == 'ROCK')] = 'boulders'
    DF['OWN'][((DF.Description.str.contains('sand')) |
               (DF.Description.str.contains('Sand'))) &
              (DF.MajorLithCode == 'ROCK')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'ROCK')] = 'gravel'
    DF['OWN'][(DF.Description.str.contains('sandstone')) &
              (DF.MajorLithCode == 'ROCK')] = 'sandstone'
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == 'ROCK')] = 'shale'
    DF['OWN'][(DF.Description.str.contains('slate')) &
              (DF.MajorLithCode == 'ROCK')] = 'slate'
    DF['OWN'][(DF.Description.str.contains('conglomerate')) &
              (DF.MajorLithCode == 'ROCK')] = 'conglomerate'
    DF['OWN'][((DF.Description.str.contains('volcanic')) |
               (DF.Description.str.contains('Volcanic'))) &
              (DF.MajorLithCode == 'ROCK')] = 'volcanic'
    DF['OWN'][(DF.Description.str.contains('limestone')) &
              (DF.MajorLithCode == 'ROCK')] = 'limestone'
    DF['OWN'][((DF.Description.str.contains('mudstone')) |
               (DF.Description.str.contains('Mudstone'))) &
              (DF.MajorLithCode == 'ROCK')] = 'mudstone'
    DF['OWN'][(DF.MajorLithCode == 'SHLE')] = 'shale'
    DF['OWN'][((DF.Description == 'Slippery back') |
               (DF.Description == 'slippery back')) &
              (DF.MajorLithCode == 'SHLE')] = np.nan
    DF['OWN'][(DF.MajorLithCode == 'GRVL')] = 'gravel'
    DF['OWN'][((DF.Description.str.contains('Sand')) |
               (DF.Description.str.contains('sand'))) &
              (DF.MajorLithCode == 'GRVL')] = 'sand gravel'
    DF['OWN'][((DF.Description.str.contains('clay')) |
               (DF.Description.str.contains('Clay'))) &
              (DF.MajorLithCode == 'GRVL')] = 'clay gravel'
    DF['OWN'][(~DF.Description.str.contains('Gravel')) &
              (~DF.Description.str.contains('gravel')) &
              ((DF.Description.str.contains('Stone')) |
               (DF.Description.str.contains('stones'))) &
              (DF.MajorLithCode == 'GRVL')] = 'stones'
    DF['OWN'][(~DF.Description.str.contains('Gravel')) &
              (~DF.Description.str.contains('gravel')) &
              ((DF.Description.str.contains('Pebble')) |
               (DF.Description.str.contains('pebbles'))) &
              (DF.MajorLithCode == 'GRVL')] = 'pebbles'
    DF['OWN'][(DF.MajorLithCode == 'SDSN')] = 'sandstone'
    DF['OWN'][(DF.Description == 'None') &
              (DF.MajorLithCode == 'SDSN')] = np.nan
    DF['OWN'][(~DF.Description.str.contains('andstone')) &
              (~DF.Description.str.contains('and rock')) &
              ((DF.Description.str.contains('Shale')) |
               (DF.Description.str.contains('shale'))) &
              (DF.MajorLithCode == 'SDSN')] = 'shale'
    DF['OWN'][(~DF.Description.str.contains('andstone')) &
              (~DF.Description.str.contains('and rock')) &
              ((DF.Description.str.contains('Sand')) |
               (DF.Description.str.contains('sand'))) &
              (DF.MajorLithCode == 'SDSN')] = 'sand'
    DF['OWN'][(DF.MajorLithCode == 'UNKN')] = np.nan
    DF['OWN'][((DF.Description.str.contains('granit')) |
               (DF.Description.str.contains('Granit'))) &
              (DF.MajorLithCode == 'UNKN')] = 'granite'
    DF['OWN'][((DF.Description.str.contains('Drift')) |
               (DF.Description.str.contains('drift'))) &
              (DF.MajorLithCode == 'UNKN')] = 'drift'
    DF['OWN'][((DF.Description.str.contains('shale')) |
               (DF.Description.str.contains('Shale'))) &
              (DF.MajorLithCode == 'UNKN')] = 'shale'
    DF['OWN'][((DF.Description.str.contains('conglomerate')) |
               (DF.Description.str.contains('Conglomerate'))) &
              (DF.MajorLithCode == 'UNKN')] = 'conglomerate'
    DF['OWN'][((DF.Description.str.contains('basalt')) |
               (DF.Description.str.contains('Basalt'))) &
              (DF.MajorLithCode == 'UNKN')] = 'basalt'
    DF['OWN'][((DF.Description.str.contains('wood')) |
               (DF.Description.str.contains('Wood'))) &
              (DF.MajorLithCode == 'UNKN')] = 'wood'
    DF['OWN'][((DF.Description.str.contains('coal')) |
               (DF.Description.str.contains('Coal'))) &
              (DF.MajorLithCode == 'UNKN')] = 'coal'
    DF['OWN'][((DF.Description.str.contains('clay')) |
               (DF.Description.str.contains('Clay'))) &
              (DF.MajorLithCode == 'UNKN')] = 'clay'
    DF['OWN'][((DF.Description.str.contains('silt')) |
               (DF.Description.str.contains('Silt'))) &
              (DF.MajorLithCode == 'UNKN')] = 'silty'
    DF['OWN'][((DF.Description.str.contains('sand')) |
               (DF.Description.str.contains('Sand'))) &
              (DF.MajorLithCode == 'UNKN')] = 'sand'
    DF['OWN'][((DF.Description.str.contains('pebble')) |
               (DF.Description.str.contains('Pebble'))) &
              (DF.MajorLithCode == 'UNKN')] = 'pebbles'
    DF['OWN'][((DF.Description.str.contains('gravel')) |
               (DF.Description.str.contains('Gravel'))) &
              (DF.MajorLithCode == 'UNKN')] = 'gravel'
    DF['OWN'][((DF.Description.str.contains('boulder')) |
               (DF.Description.str.contains('Boulder'))) &
              (DF.MajorLithCode == 'UNKN')] = 'boulders'
    DF['OWN'][((DF.Description.str.contains('limestone')) |
               (DF.Description.str.contains('Limestone'))) &
              (DF.MajorLithCode == 'UNKN')] = 'limestone'
    DF['OWN'][((DF.Description.str.contains('wacke')) |
               (DF.Description.str.contains('Wacke'))) &
              (DF.MajorLithCode == 'UNKN')] = 'greywacke'
    DF['OWN'][((DF.Description.str.contains('stones')) |
               (DF.Description.str.contains('Stones'))) &
              (DF.MajorLithCode == 'UNKN')] = 'stones'
    DF['OWN'][((DF.Description.str.contains('soil')) |
               (DF.Description.str.contains('Soil'))) &
              (DF.MajorLithCode == 'UNKN')] = 'soil'
    DF['OWN'][((DF.Description.str.contains('topsoil')) |
               (DF.Description.str.contains('Topsoil'))) &
              (DF.MajorLithCode == 'UNKN')] = 'topsoil'
    DF['OWN'][((DF.Description.str.contains('sand')) |
               (DF.Description.str.contains('Sand'))) &
              ((DF.Description.str.contains('gravel')) |
               (DF.Description.str.contains('Gravel'))) &
              (DF.MajorLithCode == 'UNKN')] = 'sand gravel'
    DF['OWN'][((DF.Description.str.contains('clay')) |
               (DF.Description.str.contains('Clay'))) &
              ((DF.Description.str.contains('gravel')) |
               (DF.Description.str.contains('Gravel'))) &
              (DF.MajorLithCode == 'UNKN')] = 'clay gravel'
    DF['OWN'][((DF.Description.str.contains('clay')) |
               (DF.Description.str.contains('Clay'))) &
              ((DF.Description.str.contains('sandy')) |
               (DF.Description.str.contains('Gravel'))) &
              (DF.MajorLithCode == 'UNKN')] = 'sandy clay'
    DF['OWN'][((DF.Description.str.contains('mudstone')) |
               (DF.Description.str.contains('Mudstone'))) &
              (DF.MajorLithCode == 'UNKN')] = 'mudstone'
    DF['OWN'][((DF.Description.str.contains('sandstone')) |
               (DF.Description.str.contains('Sandstone'))) &
              (DF.MajorLithCode == 'UNKN')] = 'sandstone'
    DF['OWN'][((DF.Description.str.contains('Rhyolite')) |
               (DF.Description.str.contains('rhyolite'))) &
              (DF.MajorLithCode == 'UNKN')] = 'rhyolite'
    DF['OWN'][((DF.Description.str.contains('Diorite')) |
               (DF.Description.str.contains('diorite'))) &
              (DF.MajorLithCode == 'UNKN')] = 'diorite'
    DF['OWN'][((DF.Description.str.contains('Andesite')) |
               (DF.Description.str.contains('andesite'))) &
              (DF.MajorLithCode == 'UNKN')] = 'andesite'
    DF['OWN'][((DF.Description.str.contains('silty clay')) |
               (DF.Description.str.contains('Silty clay'))) &
              (DF.MajorLithCode == 'UNKN')] = 'silty clay'
    DF['OWN'][((DF.Description.str.contains('Volcanic')) |
               (DF.Description.str.contains('volcanic'))) &
              (DF.MajorLithCode == 'UNKN')] = 'volcanic'
    DF['OWN'][(DF.MajorLithCode == 'CLAY')] = 'clay'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'CLAY')] = 'sandy clay'
    DF['OWN'][(DF.Description.str.contains('silt')) &
              (DF.MajorLithCode == 'CLAY')] = 'silty clay'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'CLAY')] = 'clay gravel'
    DF['OWN'][(DF.Description.str.contains('grit')) &
              (DF.MajorLithCode == 'CLAY')] = 'gritty clay'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'CLAY')] = 'clay sand gravel'
    DF['OWN'][((DF.Description.str.contains('stones')) |
               (DF.Description.str.contains('pebbles')) |
               (DF.Description.str.contains('boulder'))) &
              (DF.MajorLithCode == 'CLAY')] = 'stones clay'
    DF['OWN'][(DF.MajorLithCode == 'SAND')] = 'sand'
    DF['OWN'][(DF.Description.str.contains('and clay')) &
              (DF.MajorLithCode == 'SAND')] = 'clay sand'
    DF['OWN'][(DF.Description.str.contains('silt')) &
              (DF.MajorLithCode == 'SAND')] = 'silty sand'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'SAND')] = 'sand gravel'
    DF['OWN'][((DF.Description.str.contains('stones')) |
               (DF.Description.str.contains('pebbles'))) &
              (DF.MajorLithCode == 'SAND')] = 'stones sand'
    DF['OWN'][(DF.MajorLithCode == 'BLDR')] = 'boulders'
    DF['OWN'][(DF.Description.str.contains('clay')) &
              (DF.MajorLithCode == 'BLDR')] = 'clay boulders'
    DF['OWN'][(DF.Description.str.contains('sand')) &
              (DF.MajorLithCode == 'BLDR')] = 'sand boulders'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'SBLDR')] = 'gravel boulders'
    DF['OWN'][DF.MajorLithCode == 'CLYS'] = 'clay'
    DF['OWN'][(DF.Description.str.contains('shale')) &
              (DF.MajorLithCode == 'CLYS')] = 'shale'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'CLYS')] = 'clay gravel'
    DF['OWN'][(DF.Description.str.contains('stone')) &
              (DF.MajorLithCode == 'CLYS')] = 'claystone'
    DF['OWN'][DF.MajorLithCode == 'ALUM'] = np.nan
    DF['OWN'][(DF.Description.str.contains('water')) &
              (DF.MajorLithCode == 'ALUM')] = 'water'
    DF['OWN'][DF.MajorLithCode == 'QRTZ'] = 'quartz'
    DF['OWN'][(~DF.Description.str.contains('quartz')) &
              (~DF.Description.str.contains('Quartz')) &
              ((DF.Description.str.contains('jasper')) |
               (DF.Description.str.contains('Jasper'))) &
              (DF.MajorLithCode == 'QRTZ')] = 'jasper'
    DF['OWN'][(DF.Description.str.contains('sandstone')) &
              (DF.MajorLithCode == 'QRTZ')] = 'sandstone'
    DF['OWN'][(DF.Description.str.contains('soil')) &
              (DF.MajorLithCode == 'QRTZ')] = 'soil'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'QRTZ')] = 'gravel'
    DF['OWN'][((DF.Description.str.contains('gravel')) |
               (DF.Description.str.contains('sand'))) &
              (DF.MajorLithCode == 'QRTZ')] = 'sand gravel'
    DF['OWN'][(DF.Description.str.contains('conglomerate')) &
              (DF.MajorLithCode == 'QRTZ')] = 'conglomerate'
    DF['OWN'][DF.MajorLithCode == 'RIDG'] = 'clay'
    DF['OWN'][(DF.Description.str.contains('gravel')) &
              (DF.MajorLithCode == 'RIDG')] = 'gravel'
    DF['OWN'][((DF.Description.str.contains('gravel')) |
               (DF.Description.str.contains('clay'))) &
              (DF.MajorLithCode == 'RIDG')] = 'clay gravel'
    DF['OWN'][((DF.Description.str.contains('boulder')) |
               (DF.Description.str.contains('clay'))) &
              (DF.MajorLithCode == 'RIDG')] = 'clay boulders'


    # aggregation of litho classes into 18 major classes
    DFint = DF.dropna(subset=['OWN'])
    DFint1 = DFint.copy()
    DFint1['reclass'] = np.nan

    DFint1['reclass'][(DFint1.OWN == 'basalt') |
                      (DFint1.OWN == 'volcanic') |
                      (DFint1.OWN == 'lava') |
                      (DFint1.OWN == 'tuff') |
                      (DFint1.OWN == 'breccia') |
                      (DFint1.OWN == 'rhyolite') |
                      (DFint1.OWN == 'agglomerate') |
                      (DFint1.OWN == 'ignimbrite') |
                      (DFint1.OWN == 'zeolite') |
                      (DFint1.OWN == 'andesite') |
                      (DFint1.OWN == 'latite') |
                      (DFint1.OWN == 'trachyte') |
                      (DFint1.OWN == 'scoria') |
                      (DFint1.OWN == 'dacite') |
                      (DFint1.OWN == 'pyroclastic')] = 'volcanic'

    DFint1['reclass'][(DFint1.OWN == 'diorite') |
                      (DFint1.OWN == 'granite') |
                      (DFint1.OWN == 'porphyry') |
                      (DFint1.OWN == 'dolerite') |
                      (DFint1.OWN == 'igneous') |
                      (DFint1.OWN == 'feldspar') |
                      (DFint1.OWN == 'granodiorite') |
                      (DFint1.OWN == 'syenite') |
                      (DFint1.OWN == 'monzonite') |
                      (DFint1.OWN == 'pyroxenite') |
                      (DFint1.OWN == 'quartz')] = 'intrusive'

    DFint1['reclass'][(DFint1.OWN == 'sandstone') |
                      (DFint1.OWN == 'greywacke') |
                      (DFint1.OWN == 'arkose') |
                      (DFint1.OWN == 'wacke')] = 'sandstone'

    DFint1['reclass'][(DFint1.OWN == 'shale') |
                      (DFint1.OWN == 'mudstone') |
                      (DFint1.OWN == 'claystone') |
                      (DFint1.OWN == 'siltstone') |
                      (DFint1.OWN == 'argillite')] = 'shale'

    DFint1['reclass'][(DFint1.OWN == 'limestone') |
                      (DFint1.OWN == 'dolomite') |
                      (DFint1.OWN == 'calcrete') |
                      (DFint1.OWN == 'siderite') |
                      (DFint1.OWN == 'chalk') |
                      (DFint1.OWN == 'marl') |
                      (DFint1.OWN == 'calcite')] = 'limestone'

    DFint1['reclass'][(DFint1.OWN == 'mica') |
                      (DFint1.OWN == 'schist') |
                      (DFint1.OWN == 'serpentine') |
                      (DFint1.OWN == 'gneiss') |
                      (DFint1.OWN == 'soapstone') |
                      (DFint1.OWN == 'slate') |
                      (DFint1.OWN == 'phyllite') |
                      (DFint1.OWN == 'amphibolite') |
                      (DFint1.OWN == 'hornfels') |
                      (DFint1.OWN == 'pegmatite') |
                      (DFint1.OWN == 'metamorphic') |
                      (DFint1.OWN == 'marble') |
                      (DFint1.OWN == 'quartzite') |
                      (DFint1.OWN == 'biotite')] = 'metamorphic'

    DFint1['reclass'][(DFint1.OWN == 'carbonaceous') |
                      (DFint1.OWN == 'coal') |
                      (DFint1.OWN == 'lignite') |
                      (DFint1.OWN == 'wood') |
                      (DFint1.OWN == 'bitumen') |
                      (DFint1.OWN == 'charcoal')] = 'carbonaceous'

    DFint1['reclass'][(DFint1.OWN == 'jasper') |
                      (DFint1.OWN == 'chert') |
                      (DFint1.OWN == 'silcrete') |
                      (DFint1.OWN == 'laterite') |
                      (DFint1.OWN == 'ironstone') |
                      (DFint1.OWN == 'cement') |
                      (DFint1.OWN == 'pyrite') |
                      (DFint1.OWN == 'Pyrite') |
                      (DFint1.OWN == 'opal') |
                      (DFint1.OWN == 'gypsum') |
                      (DFint1.OWN == 'bauxite') |
                      (DFint1.OWN == 'apatite')] = 'chemical'

    DFint1['reclass'][(DFint1.OWN == 'soil') |
                      (DFint1.OWN == 'sandy loam') |
                      (DFint1.OWN == 'silty loam') |
                      (DFint1.OWN == 'loam') |
                      (DFint1.OWN == 'clay loam') |
                      (DFint1.OWN == 'sandy clay loam') |
                      (DFint1.OWN == 'topsoil') |
                      (DFint1.OWN == 'subsoil') |
                      (DFint1.OWN == 'earth')] = 'soil'

    DFint1['reclass'][(DFint1.OWN == 'soil') |
                      (DFint1.OWN == 'topsoil') |
                      (DFint1.OWN == 'subsoil') |
                      (DFint1.OWN == 'earth')] = 'soil'

    DFint1['reclass'][(DFint1.OWN == 'sandy loam') |
                      (DFint1.OWN == 'silty sandy clay') |
                      (DFint1.OWN == 'silty loam') |
                      (DFint1.OWN == 'loam') |
                      (DFint1.OWN == 'clay loam') |
                      (DFint1.OWN == 'sandy clay loam') |
                      (DFint1.OWN == 'clay') |
                      (DFint1.OWN == 'mud') |
                      (DFint1.OWN == 'pug') |
                      (DFint1.OWN == 'silty clay') |
                      (DFint1.OWN == 'bentonite') |
                      (DFint1.OWN == 'kaolinite') |
                      (DFint1.OWN == 'gritty clay') |
                      (DFint1.OWN == 'sandy clay') |
                      (DFint1.OWN == 'mud sand') |
                      (DFint1.OWN == 'clay sand') |
                      (DFint1.OWN == 'silty clay sand') |
                      (DFint1.OWN == 'silty gravel') |
                      (DFint1.OWN == 'stones clay') |
                      (DFint1.OWN == 'clay gravel') |
                      (DFint1.OWN == 'mud gravel') |
                      (DFint1.OWN == 'clay boulders') |
                      (DFint1.OWN == 'silty') |
                      (DFint1.OWN == 'sandy silt') |
                      (DFint1.OWN == 'drift')] = 'fine_sediments'

    DFint1['reclass'][(DFint1.OWN == 'stones sand') |
                      (DFint1.OWN == 'sand gravel') |
                      (DFint1.OWN == 'sand boulders') |
                      (DFint1.OWN == 'clay sand gravel') |
                      (DFint1.OWN == 'gravel') |
                      (DFint1.OWN == 'stones gravel') |
                      (DFint1.OWN == 'sand') |
                      (DFint1.OWN == 'silty sand') |
                      (DFint1.OWN == 'stones') |
                      (DFint1.OWN == 'pebbles') |
                      (DFint1.OWN == 'boulders') |
                      (DFint1.OWN == 'blue metal')] = 'coarse_sediments'

    DFint1['reclass'][(DFint1.OWN == 'conglomerate')] = 'conglomerate'
    DFint1['reclass'][(DFint1.OWN == 'bedrock')] = 'bedrock'
    DFint1['reclass'][(DFint1.OWN == 'alluvium')] = 'alluvium'
    DFint1['reclass'][(DFint1.OWN == 'water')] = 'water'
    DFint1['reclass'][(DFint1.OWN == 'cavity')] = 'cavity'
    DFint1['reclass'][(DFint1.OWN == 'sedimentary')] = 'sedimentary'
    DFint1['reclass'][(DFint1.OWN == 'peat')] = 'peat'

    DFint1['x'] = DFint1['geometry'].apply(lambda x: x.centroid.x)
    DFint1['y'] = DFint1['geometry'].apply(lambda x: x.centroid.y)
    print('number of litho classes :',
          len(DFint1['reclass'].unique()))
    print('unclassified descriptions:',
          len(DFint1[DFint1['reclass'].isnull()]))
    return DFint1


def save_file(DF, name):
    '''Function to save manually reclassified dataframe
    Inputs:
        -DF: reclassified pandas dataframe
        -name: name (string) to save dataframe file
    '''
    DF.to_pickle('{}.pkl'.format(name))


# creating lithoDataframe from files in groundwaterExplorer
Dataframe = litho_Dataframe(Dir)
# reclassifying lithological descriptions
resultingDF = manual_reclass(Dataframe)
# saving manually reclassified dataframe
save_file(resultingDF, 'manualTest')
