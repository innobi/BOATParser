import unittest

import pandas as pd
from pandas.util.testing import assert_frame_equal, assert_series_equal

from BOATParser import BOAdminToolsParser

class ParserTests(unittest.TestCase):

    def setUp(self):
        self.bp = BOAdminToolsParser()

    def test_returns_correct_dataframe(self):
        expected_df = pd.DataFrame.from_dict({
            0 : {
                'SI_NAME' : 'baz',
                'SI_ID' : '999999',
                'SI_CUID' : 'ACUID_FOR_BAZ',
                'SI_PATH' : {
                    'SI_FOLDER_ID2' : '888888',
                    'SI_FOLDER_ID1' : '777777',
                    'SI_NUM_FOLDERS' : '2',
                    'SI_FOLDER_NAME1' : 'bar',
                    'SI_FOLDER_OBTYPE2' : '1',
                    'SI_FOLDER_OBTYPE1' : '1',
                    'SI_FOLDER_NAME2' : 'foo',
                    },
                },
            1 : {
                'SI_NAME' : 'bar',
                'SI_ID' : '888888',
                'SI_CUID' : 'ACUID_FOR_BAR',
                'SI_PATH' : {
                    'SI_FOLDER_ID1' : '777777',
                    'SI_NUM_FOLDERS' : '1',
                    'SI_FOLDER_NAME1' : 'foo',
                    'SI_FOLDER_OBTYPE1' : '1',
                    },
                },
            2 : {
                'SI_NAME' : 'foo',
                'SI_ID' : '777777',
                'SI_CUID' : 'ACUID_FOR_FOO',
                'SI_PATH' : {
                    'SI_NUM_FOLDERS' : '0',
                    },
                },
            }, orient='index')

        df = self.bp.frame_from_file('test.html')

        assert_frame_equal(expected_df, df)

    def test_expand_paths(self):
        expected_series = pd.Series([
            '/foo/bar/baz',
            '/foo/bar',
            '/foo',
            ])
        
        df = self.bp.frame_from_file('test.html')
        paths = self.bp.expand_paths(df)

        assert_series_equal(paths, expected_series)

if __name__=='__main__':
    unittest.main()
            
