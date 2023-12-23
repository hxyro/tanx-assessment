import unittest
import pandas as pd
import os
from task import read_csv, validate_data, process_data

class TestCSVProcessing(unittest.TestCase):
    """
    A test class for testing CSV processing functions.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up class method to initialize test data before all tests.
        """
        ## Create a test file with valid data.
        cls.valid_data = {
            'order_id': [1, 2, 3],
            'customer_id': [101, 102, 103],
            'order_date': ['01/01/2023 10:00', '02/01/2023 12:00', '03/01/2023 15:30'],
            'product_id': [1001, 1002, 1003],
            'product_name': ['Product A', 'Product B', 'Product C'],
            'product_price': [10.0, 20.0, 30.0],
            'quantity': [5, 3, 2]
        }
        cls.valid_df = pd.DataFrame(cls.valid_data)
        cls.valid_test_file = 'valid_test_data.csv'
        cls.valid_df.to_csv(cls.valid_test_file, index=False)

        ## Create a test file with invalid data.
        cls.invalid_data = {
            'order_id': [1, 2, 3],
            'customer_id': [101, 102, 103],
            'order_date': ['01/01/2023 10:00', '02/01/2023 12:00', '03/01/2023 15:30'],
            'product_id': [1001, 1002, 1003],
            'product_name': ['Product A', 'Product B', 'Product C'],
            'product_price': [10.0, 20.0, 30.0],
            'quantity': [5, 3, 'A'] # <-- invalid data
        }
        cls.invalid_df = pd.DataFrame(cls.invalid_data)
        cls.invalid_test_file = 'invalid_test_data.csv'
        cls.invalid_df.to_csv(cls.invalid_test_file, index=False)

        ## Create a test file with invalid data(missing columns).
        cls.missing_columns_invelid_data = {
            'order_id': [1, 2, 3],
            'customer_id': [101, 102, 103],
            'order_date': ['01/01/2023 10:00', '02/01/2023 12:00', '03/01/2023 15:30'],
            'product_id': [1001, 1002, 1003],
            'product_name': ['Product A', 'Product B', 'Product C'],
            'product_price': [10.0, 20.0, 30.0]
        }
        cls.missing_columns_df = pd.DataFrame(cls.missing_columns_invelid_data)
        cls.missing_columns_test_file = 'missing_columns_invalid_test_data.csv'
        cls.missing_columns_df.to_csv(cls.missing_columns_test_file, index=False)

        ## Create an empty test file.
        cls.empty_file = 'empty.csv'
        with open(cls.empty_file, "w") as file:
            pass

    @classmethod 
    def tearDownClass(cls):
        """
        Clean up the temporary files after all tests are completed.
        """
        os.remove(cls.valid_test_file)
        os.remove(cls.invalid_test_file)
        os.remove(cls.missing_columns_test_file)
        os.remove(cls.empty_file)

    def test_read_csv_valid(self):
        """
        Test reading a valid CSV file. It should return a DataFrame and no error.
        """
        df, error = read_csv(self.valid_test_file)
        self.assertIsNotNone(df)
        self.assertIsNone(error)

    def test_read_csv_file_not_found(self):
        """
        Test reading a non-existing CSV file. It should return None and an error.
        """
        df, error = read_csv("non_existing_file.csv")
        self.assertIsNone(df)
        self.assertIsNotNone(error)

    def test_read_csv_empty_file(self):
        """
        Test reading an empty CSV file. It should return None and an error.
        """
        df, error = read_csv(self.empty_file)
        self.assertIsNone(df)
        self.assertIsNotNone(error)

    def test_validate_data_valid_data(self):
        """
        Test validating valid data. It should return True and no error.
        """
        valid, error = validate_data(self.valid_df)
        self.assertTrue(valid)
        self.assertIsNone(error)

    def test_validate_data_invalid_data(self):
        """
        Test validating data with an invalid value. It should return False and an error.
        """
        valid, error = validate_data(self.invalid_df)
        self.assertFalse(valid)
        self.assertIsNotNone(error)

    def test_validate_data_missing_columns(self):
        """
        Test validating data with missing columns. It should return False and an error.
        """
        valid, error = validate_data(self.missing_columns_df)
        self.assertFalse(valid)
        self.assertIsNotNone(error)

    def test_process_data(self):
        """
        Test processing valid data. The processed DataFrame should have 'total_value' and 'month' columns.
        """
        processed_df = process_data(self.valid_df)
        self.assertIn('total_value', processed_df.columns)
        self.assertIn('month', processed_df.columns)

if __name__ == "__main__":
    unittest.main()
