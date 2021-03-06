import pandas as pd


def geoSurvey(Dataframe, cols_in, cols_out, Imax=0.2):
    # Imax = intervale depth
    bue = []
    # loop over all the data (pick each row)
    for index, row in Dataframe.iterrows():
        if 0 < Dataframe[cols_in[2]][index]-Dataframe[cols_in[3]][index] < 1.5*Imax:
            # first condition: if thickness is very low
            a = [Dataframe[cols_in[0]][index],
                 Dataframe[cols_in[1]][index],
                 (Dataframe[cols_in[2]][index]+Dataframe[cols_in[3]][index])/2,
                 Dataframe[cols_in[4]][index],
                 Dataframe[cols_in[5]][index],
                 Dataframe[cols_in[6]][index]]
            bue.append(a)
        elif 1.5*Imax <= Dataframe[cols_in[2]][index]-Dataframe[cols_in[3]][index] <= 2.5*Imax:
            # second way, if thicknes is between two intemediate values
            a1 = [Dataframe[cols_in[0]][index],
                  Dataframe[cols_in[1]][index],
                  Dataframe[cols_in[2]][index]-Imax/2,
                  Dataframe[cols_in[4]][index],
                  Dataframe[cols_in[5]][index],
                  Dataframe[cols_in[6]][index]]

            a2 = [Dataframe[cols_in[0]][index],
                  Dataframe[cols_in[1]][index],
                  Dataframe[cols_in[3]][index]+Imax/2,
                  Dataframe[cols_in[4]][index],
                  Dataframe[cols_in[5]][index],
                  Dataframe[cols_in[6]][index]]
            bue.append(a1)
            bue.append(a2)
            # it pick two points from strata and add it to the list
        elif Dataframe[cols_in[2]][index]-Dataframe[cols_in[3]][index] > 2.5*Imax:
            # third way, if thicknes is higher than 2.5 Imax
            X = int(round(((Dataframe[cols_in[2]][index]-Imax/2)-(Dataframe[cols_in[3]][index]+Imax/2))/Imax))+1
            N = range(1, X)
            # N number of intermediate point extractions in the strata
            Ic = ((Dataframe[cols_in[2]][index]-Imax/2)-(Dataframe[cols_in[3]][index]+Imax/2))/X
            # top extraction point
            zini = [Dataframe[cols_in[0]][index],
                    Dataframe[cols_in[1]][index],
                    Dataframe[cols_in[2]][index]-Imax/2,
                    Dataframe[cols_in[4]][index],
                    Dataframe[cols_in[5]][index],
                    Dataframe[cols_in[6]][index]]

            # bottom extraction point
            zfin = [Dataframe[cols_in[0]][index],
                    Dataframe[cols_in[1]][index],
                    Dataframe[cols_in[3]][index]+Imax/2,
                    Dataframe[cols_in[4]][index],
                    Dataframe[cols_in[5]][index],
                    Dataframe[cols_in[6]][index]]

            bue.append(zini)
            bue.append(zfin)
            for n in N:
                bue.append([Dataframe[cols_in[0]][index],
                            Dataframe[cols_in[1]][index],
                            Dataframe[cols_in[2]][index]-Imax/2-(Ic*n),
                            Dataframe[cols_in[4]][index],
                            Dataframe[cols_in[5]][index],
                            Dataframe[cols_in[6]][index]])
            # loop over each of the intermediate points to extract,
            # defining x,y,z and litho in each, and finally adding to the list
        else:
            continue

    geo = pd.DataFrame(bue)
    geo.columns = cols_out
    return geo
