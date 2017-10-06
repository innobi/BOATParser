import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer

class BOAdminToolsParser():
    '''
    Class to help parse the HTML output provided by the AdminTools in Business
    Objects into a pandas DataFrame.

    For more information on how to use AdminTools, reference the following link:
    https://blogs.sap.com/2013/06/17/businessobjects-query-builder-basics/
    '''

    def _dict_from_table(self, table):
        '''
        Parameters:
        -----------
        table : BeautifulSoup tag; should be a table

        Returns:
        --------
        parsed_dict : representation of table object in dict form

        Converts an HTML table into a dict, with the first column mapping to
        the key and the second column mapping to the value. In cases where the
        second column contains an HTML table, this function will call itself
        recursively, providing a dict inside of a dict
        '''
        if table.name != 'table': # Sanity check
            raise Exception

        parsed_dict = dict()
        for tr in table.find_all('tr', recursive=False):
            # Ignore header rows
            if 'header' in tr.get_attribute_list('class'):
                continue

            # Map first two columns to key / value
            col1, col2 = tr.find_all('td', recursive=False, limit=2)

            # If the second column contains a table, call recursively
            val = self._dict_from_table(col2.table) if col2.table else col2.text

            parsed_dict[col1.text] = val

        return parsed_dict

    def expand_paths(self, fold_df):
        '''
        Parameters:
        -----------
        fold_df : DataFrame parsed from Business Objects containing folder
                information (SI_KIND='Folder'). Note that the 'SI_PATH' and
                'SI_NAME' need to be a part of the DataFrame, or else a KeyError
                will be raised

        Returns:
        --------
        fold_paths : Series of str representations of the absolute paths of
                each record in fold_df
        '''

        if not set(['SI_PATH', 'SI_NAME']).issubset(set(fold_df.columns)):
            raise KeyError('The expand_paths function requires a DataFrame '
                           'with SI_PATH and SI_NAME columns!!!')

        def _build_folder_path(rec):
            path_dict = rec['SI_PATH']
            nm = rec['SI_NAME']
            num_folders = int(path_dict['SI_NUM_FOLDERS'])
            fps = []
            # Walk backwards to build absolute folder paths
            for i in range(num_folders, 0, -1):
                key = 'SI_FOLDER_NAME{}'.format(i)
                fps.append(path_dict[key])

            # Add in name of current folder object
            fps.append(nm)

            # Add in blank entry at beginning, so join returns leading slash
            fps.insert(0, '')
            
            return '/'.join(fps)
        
        return fold_df.apply(_build_folder_path, axis=1)

    def frame_from_file(self, fn, **fopen_args):
        '''
        Parameters:
        -----------
        fn : filename to be parsed
        **fopen_args : keyword arguments to be passed to the open
                built-in function along with the filename

        Returns:
        --------
        df : pandas DataFrame object, representing the HTML content from fn
        '''

        # Speed up processing by only looking at tables, trs, tds
        only_boe_tags = SoupStrainer(['table', 'td', 'tr'])
        with open(fn, **fopen_args) as infile:
            soup = BeautifulSoup(infile, 'lxml', parse_only=only_boe_tags)

        # Filter on border attr to strip out tables that aren't report entries
        tables = soup.find_all('table', recursive=False, attrs={
            'border' : '1'
            })

        parsed = dict()
        for index, table in enumerate(tables):
            parsed[index] = self._dict_from_table(table)

        df = pd.DataFrame.from_dict(parsed, orient='index')

        return df
