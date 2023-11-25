import pandas as pd
import numpy as np
import utilities as utils
import vizualizations as viz

# unsderstanging age_bm_ecv data
age_bm_ecv_raw = utils.read_csv_file('data/clean/age_bm_ecv.csv')
age_bm_ecv = age_bm_ecv_raw.copy()

# percentage missing data
print(f"Percentage missing data: {age_bm_ecv.isnull().sum().sum() / (age_bm_ecv.shape[0]) * 100}%")

# therein'st any missing data

# data types
print(age_bm_ecv.dtypes)

agg_age_bm_ecv_data = utils.aggregate_data(age_bm_ecv, 'SpeciesECV')

viz.plot_bar(agg_age_bm_ecv_data['BM (kg)'], 'Species', 'Body Mass', 'BM (Kg)')
viz.plot_bar(agg_age_bm_ecv_data['AgeECV'], 'Species', 'Age', 'Age')

# unsderstanging age_bm data
age_bm_raw = utils.read_csv_file('data/clean/age_bm.csv')
age_bm = age_bm_raw.copy()

# percentage missing age_bm
print(f"Percentage missing data: {age_bm.isnull().sum().sum() / (age_bm.shape[0]) * 100}%")


# data types
print(age_bm.dtypes)


#lowercase ID and remove spaces and special characters like (, . / -)
age_bm['shortID'] = age_bm['ID'].str.lower().str.replace(r'[\s\(\)\.\-\/]', '', regex=True)
age_bm_ecv['shortID']  = age_bm_ecv['ID'].str.lower().str.replace(r'[\s\(\)\.\-\/]', '', regex=True)

age_bm = age_bm.set_index('shortID')
age_bm_ecv = age_bm_ecv.set_index('shortID')

print(f"age_bm: {age_bm.size}")
print(f"age_bm_ecv: {age_bm_ecv.size}")
# merge age_bm_ecv and age_bm keep all rows from both dataframes
body_mass_ecv = pd.merge(age_bm_ecv, age_bm, on='shortID', how='outer')

print(f"body_mass_ecv: {body_mass_ecv.size}")
print(f"Sum: {age_bm_ecv.size + age_bm.size}")

print("END")