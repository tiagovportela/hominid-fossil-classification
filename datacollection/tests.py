import unittest
import pandas as pd
import numpy as np
import utilities as utils

class TestUtilities(unittest.TestCase):

    def setUp(self):
        # Create a csv file for testing
        self.path = 'test.csv'
        self.data = pd.DataFrame({
            'ID': ['A', 'B', 'C'],
            'Value': [1, 2, 3]
        })
        self.data.to_csv(self.path, index=False)

    def test_read_csv_file(self):
        # Test that the function can read a csv file and return a DataFrame
        df = utils.read_csv_file('test.csv')
        pd.testing.assert_frame_equal(df, self.data)

    def test_to_numeric_values(self):
        # Test that the function can convert a column of a DataFrame to numeric values
        data = pd.DataFrame({'col1': ['1,23', 'abc'], 'col2': ['4,56', 'def']})
        result = utils.to_numeric_values(data, 'col1')
        expected = pd.DataFrame({'col1': [1.23, 'abc'], 'col2': ['4,56', 'def']})
        pd.testing.assert_frame_equal(result, expected)

    def test_aggregate_by_specimen(self):
        # Test that the function can aggregate a DataFrame by 'ID'
        data = pd.DataFrame({'ID': [1, 1, 2, 2], 'col1': [1.0, 2.0, 3.0, 4.0], 'col2': ['a', 'b', 'b', 'c']})
        result = utils.aggregate_by_specimen(data)
        expected = pd.DataFrame({'ID':[1, 2], 'col1': [1.5, 3.5], 'col2': ['a', 'b']})
        pd.testing.assert_frame_equal(result, expected)

    def test_remove_reference_from_column(self):
        # Test that the function can remove '[s<number>]' from a column of a DataFrame
        data = pd.DataFrame({'col1': ['abc[s123]', 'def[s456]', 'ghi']})
        result = utils.remove_reference_from_column(data, 'col1')
        expected = pd.DataFrame({'col1': ['abc', 'def', 'ghi']})
        pd.testing.assert_frame_equal(result, expected)

    def test_convert_age(self):
        self.assertEqual(utils.convert_age('2'), 2000)
        self.assertEqual(utils.convert_age('2.5'), 2500)
        self.assertEqual(utils.convert_age('abc'), 'ERROR')

    def test_convert_taxon_to_species(self):
        data = pd.DataFrame(
            {'Taxon': ['taxon1', 'taxon2']})
        
        expected = pd.DataFrame(
            {'Taxon': ['taxon1', 'taxon2'], 'Specie': ['species1', 'species2']})

        taxon_specie_map = pd.DataFrame({'abreviation': ['taxon1', 'taxon2'], 'name': ['species1', 'species2']})
        taxon_specie_map = taxon_specie_map.set_index('abreviation')

        data['Specie'] = data['Taxon'].apply(
                            lambda x: utils.convert_taxon_to_species(x, 'name', taxon_specie_map)
                                    )
        
        result = data.copy()
        pd.testing.assert_frame_equal(result, expected)
            

    def test_replace_taxon_used(self):
        data = pd.DataFrame({'Taxon used': [0, 'early h', 'taxon1'], 'Taxon2': ['taxon2.1', 'taxon3.1', 'taxon4.1'], 'Taxon': ['taxon5.1', 'taxon6.1', 'taxon7.1']})
        expected_result = pd.DataFrame({'Taxon used': ['taxon2', 'taxon6', 'taxon1'], 'Taxon2': ['taxon2.1', 'taxon3.1', 'taxon4.1'], 'Taxon': ['taxon5.1', 'taxon6.1', 'taxon7.1']})
        result = utils.replace_taxon_used(data)
        pd.testing.assert_frame_equal(result, expected_result)
    
    def test_handle_nan_with_date_range(self):
        data = pd.DataFrame({
            'date': [1000, 1050, 1100, 1300, 1900, 2300, 2500],
            'value': ['A', np.nan, 'A', 'B', 'C', 'D', 'E']
        })
        
        fill_columns = ['value']
        result = utils.handle_nan_with_date_range(data, 'date', fill_columns)
        
        expected = pd.DataFrame({
            'date': [1000, 1050, 1100, 1300, 1900, 2300, 2500],
            'value': ['A', 'A', 'A', 'B', 'C', 'D', 'E']
        })
        
        pd.testing.assert_frame_equal(result, expected)

    def test_fill_nan_values_with_groups(self):
        data = pd.DataFrame({
            'date': [1000, 1050, 1100, 1300, 1900, 2300, 2500],
            'value': ['A', np.nan, 'A', 'B', 'C', 'D', 'E']
        })
        fill_columns = ['value']
        result_date = utils.fill_nan_values_with_groups(data, 'date', True, fill_columns)
        expected_date = pd.DataFrame({
            'date': [1000, 1050, 1100, 1300, 1900, 2300, 2500],
            'value': ['A', 'A', 'A', 'B', 'C', 'D', 'E']
        })
        data = pd.DataFrame({
            'date': [1000, 1000, 1100, 1300, 1900, 2300, 2500],
            'value': ['A', np.nan, 'A', 'B', 'C', 'D', 'E']
        })
        result = utils.fill_nan_values_with_groups(data, 'date', False, fill_columns)
        expected = pd.DataFrame({
            'date': [1000, 1000, 1100, 1300, 1900, 2300, 2500],
            'value': ['A', 'A', 'A', 'B', 'C', 'D', 'E']
        }) 

        pd.testing.assert_frame_equal(result_date, expected_date)
        pd.testing.assert_frame_equal(result, expected)

    def tearDown(self):
        import os
        os.remove(self.path)
    
if __name__ == '__main__':
    unittest.main()