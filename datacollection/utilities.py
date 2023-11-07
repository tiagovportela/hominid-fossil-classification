import pandas as pd
import numpy as np
import math

from statistics import mode


# function read data from csv file
def read_csv_file(file_name):
    return pd.read_csv(file_name)

def conver_to_numeric(string):
    try:
        string = string.replace('*', '').replace(',', '.')
        return float(string)
    except (ValueError, AttributeError) as error:
        return string

# create a new column with  converted numeric values from string 
def to_numeric_values(data_frame, column_name):
    data = data_frame.copy()
    data[column_name] = data[column_name].apply(lambda x: conver_to_numeric(x))
    return data


# agregate by Specimen column data based on column type
# if numeric then return mean
# if string then return most frequent value mode
def aggregate_by_specimen(data_frame):
    grouped = data_frame.groupby('ID')

    agg_dict = {}
    for col in data_frame.columns:
        if data_frame[col].dtype == 'float64':
            agg_dict[col] = 'mean'
        else:
            agg_dict[col] = lambda x: mode(x)

    result = grouped.agg(agg_dict).reset_index(drop=True)
    return result.copy()


# remove [s<number>] from 'BM (kg) / Reference' create new column BM(kg) and remove [s<number>] from 'ECV (cc) / Reference' create new column ECV(cc)
# use regex to remove the [s<number>] from the column, s followed by any number of digits between [ and ]
def remove_reference_from_column(data_frame, column_name):
    data = data_frame.copy()
    try:
        new_column_name = column_name.split('/')[0].strip()
        data[new_column_name] = data[column_name].str.replace(r'\[s\d+\]', '', regex=True)
        if new_column_name != column_name:
            data = data.drop(column_name, axis=1)
        return data
    except AttributeError:
        return data

# convert age from kyr to yr
def convert_age(age):
    try:
        return float(age) * 1000
    except ValueError:
        return 'ERROR'
    
# convert_taxon_to_species
def convert_taxon_to_species(taxon, name, taxon_specie_map):
    taxon_specie_map = taxon_specie_map.to_dict()[name]
    return taxon_specie_map.get(taxon)

# if column Taxon used  equal to 0 replace with value in column Taxon splited by . and take the first element
def replace_taxon_used(data_frame):
    data = data_frame.copy()
    data.loc[data['Taxon used'] == 0, 'Taxon used'] = data['Taxon2'].str.split('.').str[0]
    data.loc[data['Taxon used'] == 'early h', 'Taxon used'] = data['Taxon'].str.split('.').str[0]
    return data

#custom mode function that ignores nan values
def custom_mode(arr):
    non_nan_values = arr.dropna()
    if non_nan_values.empty:
        return np.nan
    return non_nan_values.mode().iloc[0]

#hangle nan date
def handle_nan_with_date_range(data_frame, agg_column, fill_columns):
    data = data_frame.copy()
    max_date = data[agg_column].max()
    min_date = data[agg_column].min()
    # create bins with 175 kyears interval
    intervale = 175
    num_bins = math.ceil((max_date - min_date) / intervale)
    bins = np.linspace(min_date, max_date, num=num_bins) 

    data['value_range'] = pd.cut(data[agg_column], bins, labels=False)
    for col in fill_columns:
        map_dic = data.groupby('value_range')[col].apply(lambda x: custom_mode(x)).to_dict()
        data[col] = data[col].fillna(data['value_range'].map(map_dic))
    data = data.drop('value_range', axis=1)
    return data

def fill_nan_values_with_groups(data_frame, agg_column, is_date, fill_columns):
    data = data_frame.copy()

    if is_date:
        data = handle_nan_with_date_range(data, agg_column, fill_columns)
        return data
    
    for col in fill_columns:
        map_dic = data.groupby(agg_column)[col].apply(lambda x: custom_mode(x)).to_dict()
        data[col] = data[col].fillna(data[agg_column].map(map_dic))
    return data


# get  unique index values from list of data frames
def get_unique_index_values(data_frames):
    index_values = []
    for data_frame in data_frames:
        index_values.extend(data_frame.index.values)
    return set(index_values)

# # query dataframe by index
# def query_dataframe(data_frame, ID, column_name):
#     data = data_frame.copy()
#     data = data.reset_index()
#     mapper = data[data['ID'] == ID].set_index('ID').to_dict().get(column_name)
#     if mapper is None:
#         return None
#     return mapper.get(ID)
def query_dataframe(data_frame, ID, column_name):
    data = data_frame.copy().reset_index()
    data = data[data['ID'] == ID]
    if data.empty:
        return None
    try: 
        return data.iloc[0][column_name]
    except KeyError:
        return None