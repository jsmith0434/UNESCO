# -*- coding: utf-8 -*-

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

def addMetadata(dataSub, metaDataSub, metadataType='Source:Data sources'):
    """
    Merges the metadata to the data

    Parameters
    ----------
    dataSub: DataFrame
        a DataFrame receiving the metadata from another DataFrame
    metaDataSub: DataFrame
        a DataFrame giving metadata to another DataFrame
    metadataType: str {'Source:Data sources','Under Coverage:Students or individuals'}
        a string for specifying the type of metadata merged to the dataset (note
        that the number of metadata type will vary across datasets and over time)

    Returns
    -------
        DataFrame
            a DataFrame with an extra column of metadata
    """
    #Subsetting the metadataset by metadata type
    metadataSubByType = metaDataSub[metaDataSub['TYPE'] == metadataType]
    #Joining metadata texts with the same YEAR/COUNTRY_ID/INDICATOR_ID/TYPE combination
    metaDataSubJoined = metadataSubByType.groupby(['YEAR', 'COUNTRY_ID', 'INDICATOR_ID', 'TYPE'])\
                        ['METADATA'].apply(' | '.join).reset_index()
    dataSubsetWithMeta = pd.merge(dataSub, metaDataSubJoined, how ='left', \
                         on = ['YEAR', 'COUNTRY_ID', 'INDICATOR_ID'])
    return dataSubsetWithMeta

def addLabels(dataSetNoLabel, labelSet, keyVariable):
    """
    Adds labels to a dataset
    Adds an additional column with the country or indicators name.

    Parameters
    ----------
    dataSetNoLabel: DataFrame
        the DataFrame containing the data
    labelSet: DataFrame
        the DataFrame containing the labels
    keyVariable: str {'INDICATOR_ID', 'COUNTRY_ID'}
        a string specifying the key variable for the merge

    Returns
    -------
        DataFrame
            a DataFrame with extra columns for labels
    """
    dataSetWithLabels = pd.merge(dataSetNoLabel, labelSet, how='left', on=[keyVariable])
    return dataSetWithLabels

def get_opri():
    """
    Unpacks and cleans up the opri data set
    Saves the results to a file

    Returns
    -------
     DataFrame
            a DataFrame with the cleaned and processed OPRI data for Tanzania

    """

    # Read in the data
    path = 'data\\OPRI\\'

    eduDataSet = pd.read_csv(path+'OPRI_DATA_NATIONAL.csv')     #Data file
    metadataSet = pd.read_csv(path + 'OPRI_METADATA.csv')       #Metadata file
    countryLabels = pd.read_csv(path+'OPRI_COUNTRY.csv')        #Country code/labels file
    eduLabels = pd.read_csv(path+'OPRI_LABEL.csv')              #Indicator code/labels file
    eduDataSet.columns = eduDataSet.columns.str.upper()
    metadataSet.columns = metadataSet.columns.str.upper()
    countryLabels.columns = countryLabels.columns.str.upper()
    eduLabels.columns = eduLabels.columns.str.upper()

    # Change numeral indicators to string and extract unique values
    eduDataSet["INDICATOR_ID"] = eduDataSet["INDICATOR_ID"].astype(str)

    # Get Tanzania subset
    countryList = ['TZA']
    aSubset = eduDataSet[(eduDataSet['COUNTRY_ID'].isin(countryList))]
    meta = metadataSet[(metadataSet['COUNTRY_ID'].isin(countryList))]

    # Add metadata
    TZA_pre = addMetadata(aSubset, meta)

    # Add labels
    mySubetWith_Meta_countryLabel = addLabels(TZA_pre, countryLabels, 'COUNTRY_ID')
    TZA_data = addLabels(mySubetWith_Meta_countryLabel, eduLabels, 'INDICATOR_ID')

    # Get the most recent data for each indicator
    TZA_data = TZA_data.loc[TZA_data.reset_index().groupby(['INDICATOR_ID'])['YEAR'].idxmax()]

    ###### Export to CSV ##########################################################
    TZA_data.to_csv(path+'TZA_OPRI.csv')

    return TZA_data

def get_sdg():
    """
    Gets the SDG data for Tanzania and saves it to a file.

    Returns
    -------
     DataFrame
            a DataFrame with the cleaned and processed SDG data for Tanzania
    """

    # Read in the data
    path = 'data\\SDG\\'
    eduDataSet = pd.read_csv(path + 'SDG_DATA_NATIONAL.csv')  # Data file
    countryLabels = pd.read_csv(path + 'SDG_COUNTRY.csv')  # Country code/labels file
    metadataSet = pd.read_csv(path + 'SDG_METADATA.csv')  # Metadata file
    eduLabels = pd.read_csv(path + 'SDG_LABEL.csv')  # Indicator code/labels file
    eduDataSet.columns = eduDataSet.columns.str.upper()
    metadataSet.columns = metadataSet.columns.str.upper()
    countryLabels.columns = countryLabels.columns.str.upper()
    eduLabels.columns = eduLabels.columns.str.upper()


    # Change numeral indicators to string and extract unique values
    eduDataSet["INDICATOR_ID"] = eduDataSet["INDICATOR_ID"].astype(str)

    # Get Tanzania subset
    countryList = ['TZA']
    aSubset = eduDataSet[(eduDataSet['COUNTRY_ID'].isin(countryList))]
    meta = metadataSet[(metadataSet['COUNTRY_ID'].isin(countryList))]

    # Add labels
    TZA_SDG_pre = addMetadata(aSubset, meta)
    With_countryLabel = addLabels(TZA_SDG_pre, countryLabels, 'COUNTRY_ID')
    TZA_SDG = addLabels(With_countryLabel, eduLabels, 'INDICATOR_ID')

    # Get most recent year
    TZA_SDG = TZA_SDG.loc[TZA_SDG.reset_index().groupby(['INDICATOR_ID'])['YEAR'].idxmax()]

    # save the data set as a csv
    TZA_SDG.to_csv(path+'TZA_SDG.csv', index = False)

    return TZA_SDG

opri = get_opri()
sdg = get_sdg()


