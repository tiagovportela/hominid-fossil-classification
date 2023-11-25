import utilities as util

cranial_metrics_raw_data = util.read_csv_file('data/s1.csv')
cranial_metrics = cranial_metrics_raw_data.copy()



#conver numeric columns to float
for col in cranial_metrics.columns:
    cranial_metrics = util.to_numeric_values(cranial_metrics, col)



#aggregate by specimen
cranial_metrics = util.aggregate_by_specimen(cranial_metrics)
print(f"aggregated data len: {cranial_metrics.shape[0]}")
print(f"Raw data len: {cranial_metrics_raw_data.shape[0]}")

# set ID as index
cranial_metrics = cranial_metrics.set_index('ID')


age_bm_ecv_raw = util.read_csv_file('data/s2.csv')
age_bm_ecv = age_bm_ecv_raw.copy()
    


# remove reference from BM (kg) / Reference and ECV (cc) / Reference
columns_to_remove_reference = ['BM (kg) / Reference', 'ECV (cc) / Reference']
for col in columns_to_remove_reference:
    age_bm_ecv = util.remove_reference_from_column(age_bm_ecv, col)
    

#convert age from kyr to yr
age_bm_ecv['Age'] = age_bm_ecv['Age (kyr)'].apply(lambda x: util.convert_age(x))
age_bm_ecv = age_bm_ecv.drop('Age (kyr)', axis=1)


for col in age_bm_ecv.columns:
    age_bm_ecv = util.to_numeric_values(age_bm_ecv, 'Age')

age_bm_ecv['ID'] = age_bm_ecv['Specimen']
age_bm_ecv = age_bm_ecv.drop('Specimen', axis=1)

age_bm_ecv = util.aggregate_by_specimen(age_bm_ecv)
print(f"aggregated data len: {age_bm_ecv.shape[0]}")
print(f"Raw data len: {age_bm_ecv_raw.shape[0]}")
age_bm_ecv = age_bm_ecv.set_index('ID')


age_bm_raw = util.read_csv_file('data/De_Miguel_Henneberg_2001_BodySize.csv')
age_bm = age_bm_raw.copy()

# drop Age max and Age min columns
age_bm = age_bm.drop(['Age max', 'Age min', '"median" age'], axis=1)
age_bm = age_bm.rename(columns={'Age (~0.025 My accuracy)': 'Age'})
for col in age_bm.columns:
    age_bm = util.to_numeric_values(age_bm, col)
age_bm['Age'] = age_bm['Age'] * 1_000_000
age_bm = age_bm.rename(columns={'SPECIMENS': 'ID'})

age_bm = util.aggregate_by_specimen(age_bm)
print(f"aggregated data len: {age_bm.shape[0]}")
print(f"Raw data len: {age_bm_raw.shape[0]}")
age_bm = age_bm.set_index('ID')

cranial_capacity_raw = util.read_csv_file('data/De_Miguel_Henneberg_2001_CC.csv')
cranial_capacity = cranial_capacity_raw.copy()

cranial_capacity = cranial_capacity.drop(
                        ['u? (Taxon used?)', '1st taxon', 'multiple taxa?', 'CC (ml)'],
                        axis=1)

for col in cranial_capacity.columns:
    cranial_capacity = util.to_numeric_values(cranial_capacity, col)

cranial_capacity = util.aggregate_by_specimen(cranial_capacity)
print(f"aggregated data len: {cranial_capacity.shape[0]}")
print(f"Raw data len: {cranial_capacity_raw.shape[0]}")


cranial_capacity['Taxon2'] = cranial_capacity['Taxon'].str.split('/').str[0]
cranial_capacity.loc[
    cranial_capacity['Taxon2'] == 'early h', 'Taxon'
    ] = cranial_capacity['Taxon'].str.split('.').str[1]
# if Taxon used  equal to 0 replace with Taxon splited by . and take the first element
cranial_capacity = util.replace_taxon_used(cranial_capacity)
cranial_capacity['Taxon used'] = cranial_capacity['Taxon used'].str.split('-').str[0]




taxon_specie_map = util.read_csv_file('data/map_taxon.csv')
taxon_specie_map = taxon_specie_map.set_index('abreviation')

cranial_capacity['Specie1'] = cranial_capacity['Taxon used'].apply(
                            lambda x: util.convert_taxon_to_species(x, 'name1', taxon_specie_map)
                            )
cranial_capacity['Specie2'] = cranial_capacity['Taxon used'].apply(
                            lambda x: util.convert_taxon_to_species(x, 'name2', taxon_specie_map)
                            )

cranial_capacity = util.fill_nan_values_with_groups(
                            cranial_capacity, 'Date', True, ['Specie1', 'Specie2']
                            )
cranial_capacity = cranial_capacity.set_index('ID')


# Build the final data frame

#rename columns that have the same name
age_bm_ecv = age_bm_ecv.rename(columns={'Age': 'AgeECV'})
age_bm_ecv = age_bm_ecv.rename(columns={'Species': 'SpeciesECV'})
age_bm = age_bm.rename(columns={'Age': 'AgeBM'})
cranial_metrics  = cranial_metrics.rename(columns={'Species': 'SpeciesCM'})
cranial_capacity = cranial_capacity.rename(columns={
                                            'Date': 'AgeCC',
                                            'min': 'minCC',
                                            'max': 'maxCC',
                                            'mean': 'meanCC'
                                            })
data_frames = [cranial_metrics, age_bm_ecv, age_bm, cranial_capacity]

# set all index as string
for data_frame in data_frames:
    data_frame.index = data_frame.index.astype(str)


final_columns = [
                'SpeciesECV', 'BM (kg)', 'ECV (cc)', 'AgeECV',
                'Body mass (kg)', 'AgeBM',
                'SpeciesCM', 'Group', 'GOL', 'BBH', 'XCB', 'NPH', 'BPL', 'ZYB',
                'Taxon used', 'Taxon', 'Taxon2', 'Specie1', 'Specie2', 'AgeCC', 'minCC', 'maxCC', 'meanCC'
                ]


import pandas as pd

#save all dataframes in csv
cranial_capacity.reset_index().sort_values(by='ID').to_csv('data/clean/cranial_capacity.csv', index=False)
cranial_metrics.reset_index().sort_values(by='ID').to_csv('data/clean/cranial_metrics.csv', index=False)
age_bm.reset_index().sort_values(by='ID').to_csv('data/clean/age_bm.csv', index=False)
age_bm_ecv.reset_index().sort_values(by='ID').to_csv('data/clean/age_bm_ecv.csv', index=False)

data = pd.merge(cranial_metrics, age_bm_ecv, on='ID', how='outer')
data = pd.merge(data, age_bm, on='ID', how='outer')
data = pd.merge(data, cranial_capacity, on='ID', how='outer')

data = data[final_columns]

print(f"final data len: {data.shape[0]}")
print(f"Nulls Percentage:\n {data.isna().sum() / data.shape[0] * 100}%")

#save data
data.reset_index().sort_values(by='ID').to_csv('data/clean/data.csv', index=False)


